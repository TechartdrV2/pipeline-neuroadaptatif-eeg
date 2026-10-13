import sys
import time
import os
import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, WindowOperations

class MITExperiment:
    def __init__(self, user_id, mac_address):
        self.user_id = user_id
        # Génération d'un nom de fichier unique horodaté pour le Data Lake
        self.filename = f"session_{user_id}_{int(time.time())}.csv"
        
        # Configuration basse tension de BrainFlow
        BoardShim.set_log_level(3)
        params = BrainFlowInputParams()
        params.mac_address = mac_address
        params.other_info = "preset=p21;low_latency=true"
        params.timeout = 15
        
        # CORRECTION : Utilisation du nom officiel de la constante (Athena)
        self.board_id = BoardIds.MUSE_S_ATHENA_BOARD.value
        self.board = BoardShim(self.board_id, params)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.eeg_channels = BoardShim.get_eeg_channels(self.board_id)
        
        # Structure du fichier CSV adaptée à la nomenclature internationale (AF7, AF8 au lieu de FPN)
        self.columns = [
            'Timestamp_NS', 'Phase', 'Asymetrie_FAA', 'Vigilance_Beta',
            'Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8',
            'Alpha_TP9', 'Alpha_TP10', 'Beta_TP9', 'Beta_TP10'
        ]
        self.data_log = []

    def determiner_phase(self, elapsed_time):
        """Chronomètre automatique du protocole expérimental"""
        if elapsed_time < 60:
            return "1_BASELINE"
        elif elapsed_time < 150:
            return "2_CHARGE_MENTALE"
        elif elapsed_time < 210:
            return "3_STRESS_REACTIF"
        elif elapsed_time < 300:
            return "4_RECOVERY"
        else:
            return "FINISHED"

    def collecter_seconde(self, phase):
        # 512 points à 256Hz = Fenêtre glissante de 2 secondes
        data = self.board.get_current_board_data(512)
        if data.shape[1] < 512:
            return

        # CORRECTION : Extraction rigoureuse et indépendante de chaque canal EEG
        # Index officiels Muse S via BrainFlow : 0=TP9 (Gauche), 1=AF7 (Gauche), 2=AF8 (Droit), 3=TP10 (Droit)
        ch_tp9 = np.copy(data[self.eeg_channels[0]])
        ch_af7 = np.copy(data[self.eeg_channels[1]])
        ch_af8 = np.copy(data[self.eeg_channels[2]])
        ch_tp10 = np.copy(data[self.eeg_channels[3]])

        channels = {'TP9': ch_tp9, 'AF7': ch_af7, 'AF8': ch_af8, 'TP10': ch_tp10}
        powers = {}

        nfft = DataFilter.get_nearest_power_of_two(self.sampling_rate)
        
        for name, ch_data in channels.items():
            # 1. Detrend pour supprimer la dérive de la composante continue (DC Offset)
            DataFilter.detrend(ch_data, DetrendOperations.LINEAR.value)
            # 2. Filtre Coupe-bande (Notch à 50 Hz pour le réseau électrique européen)
            DataFilter.perform_bandstop(ch_data, self.sampling_rate, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH.value, 0)
            # 3. Filtre Passe-bande physiologique (2.0 - 35.0 Hz)
            DataFilter.perform_bandpass(ch_data, self.sampling_rate, 2.0, 35.0, 3, FilterTypes.BUTTERWORTH.value, 0)
            
            # Transformation de Fourier (PSD) via la méthode de Welch
            psd = DataFilter.get_psd_welch(ch_data, nfft, nfft // 2, self.sampling_rate, WindowOperations.HANNING.value)
            powers[f'Alpha_{name}'] = DataFilter.get_band_power(psd, 8.0, 13.0)
            powers[f'Beta_{name}'] = DataFilter.get_band_power(psd, 13.0, 30.0)

        # Calcul des indices d'Asymétrie Frontale Alpha (FAA) et de Vigilance Beta
        faa = np.log(powers['Alpha_AF8'] + 1e-6) - np.log(powers['Alpha_AF7'] + 1e-6)
        vigilance = (powers['Beta_AF7'] + powers['Beta_AF8']) / 2.0

        # Enregistrement de la ligne de télémétrie complète
        row = [
            time.time_ns(), phase, faa, vigilance,
            powers['Alpha_AF7'], powers['Alpha_AF8'], powers['Beta_AF7'], powers['Beta_AF8'],
            powers['Alpha_TP9'], powers['Alpha_TP10'], powers['Beta_TP9'], powers['Beta_TP10']
        ]
        self.data_log.append(row)
        
        # Log de suivi en temps réel pour le chercheur
        print(f"[{phase:<17}] Index FAA: {faa:+.3f} | Attention Beta: {vigilance:.2f}")

    def run(self):
        try:
            self.board.prepare_session()
            self.board.start_stream()
            print(f"\n🔬 Expérience initialisée pour le sujet : {self.user_id}")
            print(f"📁 Fichier de sauvegarde créé : {self.filename}")
            print("Début du protocole dans 3 secondes...")
            time.sleep(3)

            start_time = time.time()
            while True:
                elapsed = time.time() - start_time
                phase = self.determiner_phase(elapsed)
                
                if phase == "FINISHED":
                    break
                    
                self.collecter_seconde(phase)
                time.sleep(1.0)  # Intervalle de traitement d'une seconde

            print("\n🏁 Expérience arrivée à son terme.")

        except Exception as e:
            print(f"Erreur en cours de protocole : {e}")
        finally:
            # Fermeture propre des flux de streaming Bluetooth
            if self.board.is_prepared():
                try:
                    self.board.stop_stream()
                    self.board.release_session()
                except Exception:
                    pass  # Ignore les erreurs d'un-subscribe Bluetooth si la Muse s'éteint brutalement
            
            # Sauvegarde finale des données dans le Data Lake local
            if self.data_log:
                df = pd.DataFrame(self.data_log, columns=self.columns)
                df.to_csv(self.filename, index=False)
                print(f"💾 Données enregistrées avec succès : {os.path.abspath(self.filename)}")
            
            # CORRECTION BUG PYTHON 3.14 : Forcer la destruction de l'objet Ctypes avant l'arrêt de l'interpréteur
            if hasattr(self, 'board'):
                del self.board

if __name__ == "__main__":
    # Configuration pour le sujet actuel
    LAB_SESSION = MITExperiment(user_id="SUJET_02", mac_address="...")
    LAB_SESSION.run()
