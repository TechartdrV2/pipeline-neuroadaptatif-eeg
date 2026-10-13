# Manuel d'expérimentation neuroscientifique : Protocole "Synchro-Affect"
**Laboratoire d'EEG Quantitatif & Informatique Affective**

Ce manuel détaille la procédure standardisée pour déployer, animer et exploiter l'expérience de stress réactif à l'aide du bandeau **Muse S Athena** et du script `experiment_lab.py`.

---

## 1. Fondements théoriques & objectifs

L'objectif de cette expérience est de valider scientifiquement la pertinence de l'**Asymétrie Frontale Alpha (FAA)** comme marqueur biologique du stress psychologique, en la distinguant de la simple charge mentale (attention focalisée).

### Les indicateurs mesurés
*   **L'Index FAA (Asymétrie Frontale Alpha)** : Calculé via la formule ln(Alpha Droit) - ln(Alpha Gauche). Un état calme ou de concentration normale maintient cet index proche de 0.0. Une réaction de stress aigu ou de peur provoque une activation préfrontale droite, faisant chuter l'index profondément sous la barre des -0.25.
*   **La Vigilance Beta** : Mesure l'activation cognitive globale. Elle augmente lors d'un calcul mental ou d'une lecture, sans pour autant être synonyme de stress.

---

## 2. Configuration de l'environnement de test

Pour garantir la pureté des signaux EEG (éviter les artéfacts environnementaux), respectez les consignes suivantes :

1.  **Luminosité** : Tamisée et constante. Évitez les néons ou les lumières oscillantes qui induisent des fréquences parasites.
2.  **Positionnement** : Le participant doit être assis sur une chaise confortable, non pivotante, face à l'écran d'affichage des stimuli. Ses bras doivent reposer sur la table ou les accoudoirs pour éviter les tensions musculaires des épaules.
3.  **Matériel** : Le Muse S Athena doit être ajusté de manière à ce que les deux capteurs en silicone sur le front (FPN1/FPN2) soient bien en contact avec la peau, juste au-dessus des sourcils. Nettoyez le front du participant avec une lingette légèrement humide si la peau est grasse.

---

## 3. Déroulement chronologique du protocole (5 Minutes)

L'expérience est entièrement automatisée par le script et dure **300 secondes**. Le chercheur doit préparer les stimuli externes (sur un écran secondaire ou via un casque audio) et suivre le chronomètre affiché dans la console VS Code.

- Phase 1 : Baseline (60s)
- Phase 2 : Charge Mentale (90s)
- Phase 3 : Stress Réactif (60s)
- Phase 4 : Recovery (90s)

### Phase 1 : BASELINE (0 à 60 secondes)
*   **Objectif** : Enregistrer l'activité cérébrale de référence au repos.
*   **Stimulus** : Écran noir ou image de nature. Audio de vagues calmes dans le casque.
*   **Consigne au participant** : "Restez immobile, fermez les yeux ou fixez le centre de l'écran. Laissez vos pensées filer sans vous concentrer sur rien en particulier."

### Phase 2 : CHARGE MENTALE (60 à 150 secondes)
*   **Objectif** : Stimuler une forte activité cognitive (Beta) sans déclencher de stress de menace.
*   **Stimulus** : Présentez une série de calculs mentaux complexes à haute fréquence (ex: soustraire 7 de manière itérative à partir de 1000 : 993, 986, 979...) ou un test de Stroop.
*   **Consigne au participant** : "Vous allez voir des calculs apparaître. Résolvez-les mentalement le plus rapidement possible. Restez concentré."

### Phase 3 : STRESS RÉACTIF (150 à 210 secondes)
*   **Objectif** : Provoquer une rupture brutale de l'équilibre inter-hémisphérique (chute de la FAA).
*   **Stimulus** : Vers 150e seconde, déclenchez un stimulus perturbateur. Variantes efficaces : Une alarme stridente surprise dans le casque (85 dB), une vidéo de menace imminente (ex: vue subjective d'une chute ou d'une phobie), ou un compte à rebours visuel ultra-rapide avec un bruit de détonation à la fin.
*   **Consigne au participant** (Ne pas prévenir le participant de la nature exacte du stimulus) : "Continuez à fixer l'écran et regardez attentivement ce qui s'affiche."

### Phase 4 : RECOVERY / RETOUR AU CALME (210 à 300 secondes)
*   **Objectif** : Observer la résilience neuronale et la vitesse de reconnexion de l'hémisphère gauche.
*   **Stimulus** : Écran blanc ou bleu ciel doux. Audio de cohérence cardiaque (guide respiratoire visuel : 5s d'inspiration, 5s d'expiration).
*   **Consigne au participant** : "Le test est terminé. Suivez le rythme de la respiration affiché à l'écran pour vous détendre complètement."

---

## 4. Guide de l'animateur (Script de parole)

Pour standardiser l'expérience et éviter les biais d'un participant à l'autre, lisez ce texte exact avant de lancer le script Python :

"Bonjour et merci de participer à cette étude d'informatique affective. Nous allons enregistrer votre activité cérébrale pendant 5 minutes. Pendant toute la durée du test, il est capital de limiter au maximum les mouvements physiques. Ne parlez pas, ne serrez pas les dents et essayez de ne pas froncer les sourcils, car les muscles de votre visage masquent les signaux de votre cerveau.

Le test va s'enchaîner tout seul. Vous aurez une phase de repos, une phase d'exercice mental, une phase de sollicitation visuelle, et une phase de récupération. Contentez-vous de suivre les instructions sur l'écran des stimuli. Avez-vous des questions ? [...] Très bien, nous commençons dans 3 secondes."

---

## 5. Structure du Data Lake (Fichier CSV généré)

À la fin des 300 secondes, le programme exporte un fichier nommé session_[SUJET]_[TIMESTAMP].csv. Chaque ligne correspond à 1 seconde d'enregistrement :

*   Timestamp_NS : Temps universel Unix en nanosecondes (Clé de synchronisation).
*   Phase : Phase active (1_BASELINE, 2_CHARGE_MENTALE, etc.).
*   Asymetrie_FAA : Valeur mathématique de la FAA. (Cible principale de l'étude).
*   Vigilance_Beta : Niveau d'attention globale mesuré sur le front.
*   Alpha_FPN1 / FPN2 : Puissance brute de la bande Alpha sur le front Gauche / Droit.
*   Beta_FPN1 / FPN2 : Puissance brute de la bande Beta sur le front Gauche / Droit.
*   Alpha_TP9 / TP10 : Puissance Alpha mesurée derrière les oreilles.

---

## 6. Analyse des résultats & critères de validation

Pour valider le succès de votre expérience, ouvrez le fichier CSV à la fin du test. Vos graphiques doivent valider les hypothèses suivantes :
1.  Vigilance Beta : Doit être basse en Phase 1, monter en flèche en Phase 2 (travail) et rester haute ou osciller en Phase 3 (stress), avant de chuter en Phase 4.
2.  Index FAA : Doit rester stable et proche de 0.0 (symétrie) pendant les Phases 1 et 2. Il doit plonger profondément dans les valeurs négatives (ex: -0.45) pendant la Phase 3. Une remontée vers le positif doit être observée en Phase 4.

---

## 7. Procédure d'exécution du script d'acquisition

Suivez scrupuleusement ces étapes pour lancer l'acquisition de données EEG en temps réel.

### Prérequis techniques
1. Assurez-vous que le bandeau **Muse S Athena** est allumé (diode clignotante bleue ou blanche).
2. Vérifiez que le Bluetooth de votre ordinateur de test est activé.
3. Activez votre environnement virtuel Python à la racine de votre dossier :
   ```bash
   source .venv/bin/activate  # Sur Linux / macOS
   .venv\Scripts\activate     # Sur Windows
   ```

### Lancement de la session de test
1. Ouvrez le fichier `experiment_lab.py` et modifiez si nécessaire la configuration du bloc principal tout en bas du script avec l'identifiant du participant et l'adresse MAC du bandeau :
   ```python
   LAB_SESSION = MITExperiment(user_id="SUJET_01", mac_address="...")
   ```
2. Exécutez le script depuis votre terminal :
   ```bash
   python experiment_lab.py
   ```
3. Suivez les instructions de la console : le script observe une pause de **3 secondes** pour vous laisser le temps d'ajuster les stimuli, puis lance automatiquement le chronomètre de **300 secondes**.
4. À la fin du protocole, un message confirme la fermeture propre des flux Bluetooth et indique le chemin absolu du fichier `.csv` généré.
