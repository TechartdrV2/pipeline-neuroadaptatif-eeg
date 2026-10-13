import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats as scipy_stats

def charger_derniere_session():
    """Recherche le fichier de session CSV le plus récent dans le dossier"""
    fichiers = glob.glob("session_*.csv")
    if not fichiers:
        print("❌ Aucun fichier de session 'session_*.csv' trouvé dans ce dossier.")
        print("Veuillez d'abord exécuter 'experiment_lab.py' pour générer des données.")
        return None
    
    dernier_fichier = max(fichiers, key=os.path.getctime)
    print(f"📊 Fichier détecté pour l'analyse : {os.path.abspath(dernier_fichier)}")
    return dernier_fichier

def analyser_donnees(chemin_fichier):
    # Lecture sûre du Data Lake local
    df = pd.read_csv(chemin_fichier)
    
    # CORRECTION : Calcul rigoureux du temps écoulé basé sur les Nanosecondes réelles
    df['Temps_S'] = (df['Timestamp_NS'] - df['Timestamp_NS'].iloc[0]) / 1e9
    
    print("\n--- 📑 RAPPORT STATISTIQUE PAR PHASE ---")
    stats_df = df.groupby('Phase').agg({
        'Asymetrie_FAA': ['mean', 'std'],
        'Vigilance_Beta': ['mean', 'std']
    })
    print(stats_df.round(4))
    
    # --- AJOUT FONCTIONNALITÉ 1 : INTERFÉRENCE STATISTIQUE (T-TEST) ---
    print("\n--- 🔬 VALIDATION SCIENTIFIQUE DE L'HYPOTHÈSE ---")
    baseline_faa = df[df['Phase'] == '1_BASELINE']['Asymetrie_FAA']
    stress_faa = df[df['Phase'] == '3_STRESS_REACTIF']['Asymetrie_FAA']
    
    if not baseline_faa.empty and not stress_faa.empty:
        t_stat, p_val = scipy_stats.ttest_ind(baseline_faa, stress_faa, equal_var=False)
        print(f"Test T de Student (FAA Baseline vs Stress Réactif) :")
        print(f"  - Statistique T : {t_stat:.4f}")
        print(f"  - P-Value       : {p_val:.6e}")
        if p_val < 0.05:
            print("  ✅ RÉSULTAT SIGNIFICATIF : L'hypothèse de dissociation émotionnelle est validée.")
        else:
            print("  ❌ RÉSULTAT NON SIGNIFICATIF : Écart insuffisant ou niveau de bruit trop élevé.")
            
    # --- AJOUT FONCTIONNALITÉ 2 : SCORE DE RÉSILIENCE ---
    recovery_faa = df[df['Phase'] == '4_RECOVERY']['Asymetrie_FAA']
    if not baseline_faa.empty and not recovery_faa.empty:
        score_resilience = (recovery_faa.mean() / baseline_faa.mean()) * 100 if baseline_faa.mean() != 0 else 0
        print(f"Indicateur de Résilience Affective : {score_resilience:.2f}% de retour à la Baseline hémisphérique.")

    # Configuration esthétique universitaire du graphique
    sns.set_theme(style="white")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True)
    fig.suptitle(f"Rapport d'Informatique Affective - {os.path.basename(chemin_fichier)}", 
                 fontsize=14, fontweight='bold', y=0.98)

    couleurs_phases = {
        "1_BASELINE": "#34495e",       # Gris foncé
        "2_CHARGE_MENTALE": "#3498db",  # Bleu
        "3_STRESS_REACTIF": "#e74c3c",  # Rouge
        "4_RECOVERY": "#2ecc71"         # Vert
    }

    # --- GRAPHIQUE 1 : ASYMÉTRIE FRONTALE ALPHA (FAA) ---
    ax1.plot(df['Temps_S'], df['Asymetrie_FAA'], color='#8e44ad', linewidth=2.5, label='Index FAA')
    ax1.axhline(0, color='black', linestyle='-', alpha=0.3, linewidth=1)
    ax1.set_ylabel("Index Asymétrie FAA\n[ln(Droit) - ln(Gauche)]", fontsize=11, fontweight='bold')
    ax1.set_title("Évolution de l'Asymétrie Inter-Hémisphérique (FAA)", fontsize=12, loc='left', fontweight='bold')
    
    # --- GRAPHIQUE 2 : VIGILANCE BETA ---
    ax2.plot(df['Temps_S'], df['Vigilance_Beta'], color='#d35400', linewidth=2.5, label='Attention Beta')
    ax2.set_ylabel("Puissance Vigilance Beta\n[Microvolts²]", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Temps de l'expérience (secondes)", fontsize=11, fontweight='bold')
    ax2.set_title("Évolution de la Charge Cognitive (Vigilance Beta)", fontsize=12, loc='left', fontweight='bold')

    # Coloration et segmentation temporelle des phases
    phases_presentes = df['Phase'].unique()
    for phase in phases_presentes:
        donnees_phase = df[df['Phase'] == phase]
        debut = donnees_phase['Temps_S'].min()
        fin = donnees_phase['Temps_S'].max()
        couleur = couleurs_phases.get(phase, "#7f8c8d")
        
        # Superposition des zones de couleurs transparentes
        ax1.axvspan(debut, fin, color=couleur, alpha=0.12)
        ax2.axvspan(debut, fin, color=couleur, alpha=0.12)
        
        # AJOUT FONCTIONNALITÉ 3 : Barres de transition nettes
        ax1.axvline(fin, color='#7f8c8d', linestyle=':', alpha=0.6)
        ax2.axvline(fin, color='#7f8c8d', linestyle=':', alpha=0.6)

    # CORRECTION BUG DE POSITIONNEMENT : Placement des textes après finalisation des échelles
    plt.draw() # Force le calcul des limites géométriques des axes
    ylim_ax1 = ax1.get_ylim()
    
    for phase in phases_presentes:
        donnees_phase = df[df['Phase'] == phase]
        debut = donnees_phase['Temps_S'].min()
        fin = donnees_phase['Temps_S'].max()
        milieu = debut + (fin - debut) / 2
        couleur = couleurs_phases.get(phase, "#7f8c8d")
        
        # Positionnement horizontal centré et calé en hauteur à 85% du graphique supérieur
        y_pos = ylim_ax1[0] + (ylim_ax1[1] - ylim_ax1[0]) * 0.88
        ax1.text(milieu, y_pos, phase.replace("_", "\n"), 
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=10, fontweight='bold', color=couleur,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

    sns.despine(left=False, bottom=False)
    plt.tight_layout()
    
    # Sauvegarde haute définition
    nom_image = chemin_fichier.replace(".csv", "_graphique.png")
    plt.savefig(nom_image, dpi=300)
    print(f"🎨 Graphique scientifique sauvegardé avec succès : {nom_image}")
    plt.show()

if __name__ == "__main__":
    fichier_cible = charger_derniere_session()
    if fichier_cible:
        analyser_donnees(fichier_cible)