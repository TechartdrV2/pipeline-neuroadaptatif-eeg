# Manuel d'analyse statistique : Indice "synchro-affect"
**Laboratoire d'EEG Quantitatif & Informatique Affective**

Ce manuel sert de guide d'interprétation pour le script `analyse_stats.py` mis à jour. Il détaille comment lire le rapport statistique de la console, valider les métriques mathématiques avancées, et identifier les biais expérimentaux.

---

## 1. Rappel de l'hypothèse scientifique à valider

L'objectif de ce pipeline d'analyse est de démontrer graphiquement et statistiquement une double dissociation :
1. La Charge Mentale (Phase 2) active le cerveau (hausse de la vigilance corticale Beta) mais maintient l'équilibre émotionnel (Asymétrie FAA stable près de 0).
2. Le Stress Réactif (Phase 3) rompt l'équilibre inter-hémisphérique (chute brutale de la FAA vers le négatif) en raison de l'activation du système de retrait/évitement préfrontal droit.

---

## 2. Décoder le rapport statistique & indicateurs avancés

Lorsque vous lancez le script, le terminal extrait automatiquement la dernière session et affiche :

### A. Statistiques de dispersion basiques
* **mean (Moyenne)** : Point central de stabilisation de la phase. Une FAA saine au repos se situe entre `-0.05` et `+0.10`. Une chute sous `-0.25` valide l'état de détresse psychologique.
* **std (Écart-type)** : Reflet de la réactivité. Un `std` élevé en Phase 3 indique une forte variabilité dynamique induite par l'effet de surprise du stimulus.

### B. Métriques critiques
* **Test T de Student (P-Value)** : Détermine si l'écart entre la Baseline et le Stress est le fruit du hasard ou d'une authentique modification neurophysiologique. La valeur cible doit être strictement inférieure à **0.05** (\(p < 0.05\)) pour publier les résultats.
* **Indicateur de Résilience Affective** : Exprimé en %, il évalue la vitesse à laquelle le cortex préfrontal gauche reprend le dessus durant la phase de récupération (*Recovery*). Un score proche de 100% indique un sujet hautement résilient.

---

## 3. Guide d'interprétation du graphique Bi-Volet (300 DPI)

Le graphique généré superpose l'évolution temporelle brute corrigée avec des lignes pointillées de transition de phase précises.

### Étape A : Analyser le volet supérieur – L'index d'asymétrie FAA (Courbe Violette)
* **En zone 1 (Gris - Baseline)** : Point d'étalonnage. La courbe doit fluctuer de façon stationnaire autour de 0.
* **En zone 2 (Bleu - Charge Mentale)** : Malgré l'effort de calcul, la courbe reste stable près du zéro. Le sujet est concentré mais ne se sent pas agressé.
* **En zone 3 (Rouge - Stress Réactif)** : Chute libre immédiate sous la ligne de symétrie. C'est la signature de l'activation préfrontale droite d'évitement.
* **En zone 4 (Vert - Recovery)** : Remontée graduelle de la courbe violette, validant l'efficacité de la cohérence cardiaque.

### Étape B : Analyser le volet inférieur – La vigilance Beta (Courbe Orange)
* **En zone 1** : Plancher d'activité.
* **En zone 2** : Profil en marche d'escalier ascendante franche. La puissance spectrale Beta confirme l'engagement cognitif.
* **En zone 3** : Maintien à un niveau haut avec pics oscillatoires majeurs provoqués par les sursauts musculaires et micro-mouvements de surprise.

---

## 4. Diagnostics : Comment repérer les anomalies ?

* **Anomalie 1 : La P-Value renvoie `NaN` ou est supérieure à 0.05 alors que le graphique montre une baisse.**
    * *Cause* : Échantillonnage corrompu ou trop d'artéfacts oculaires (clignements répétés) ayant lissé artificiellement la moyenne du signal.
* **Anomalie 2 : La ligne temporelle s'arrête avant 300 secondes sur le graphique.**
    * *Cause* : Le script d'acquisition a subi des déconnexions Bluetooth (Paquets BLE rejetés). La synchronisation par Nanosecondes du nouveau script met en lumière ces pertes de paquets sans distordre l'échelle réelle.

---

## 5. Procédure d'exécution du pipeline d'analyse

Suivez ces instructions pour traiter les données du participant et générer les rapports visuels de l'étude.

### Prérequis techniques
L'analyse statistique s'appuie sur les bibliothèques scientifiques `pandas`, `scipy` et `seaborn`. Assurez-vous que votre environnement virtuel est actif :
```bash
source .venv/bin/activate  # Sur Linux / macOS
.venv\Scripts\activate     # Sur Windows
```

### Lancement du traitement statistique
1. Placez-vous dans le dossier racine contenant vos scripts et vos fichiers de sessions :
   ```bash
   cd path/to/experience_eeg
   ```
2. Lancez le script d'analyse statistique :
   ```bash
   python analyse_stats.py
   ```

### Comportement du script
* **Détection Automatique** : Le programme scanne votre répertoire, identifie le fichier de données `session_*.csv` possédant la date de modification **la plus récente** et l'ouvre.
* **Calculs & Console** : Les moyennes par phase, l'indicateur de résilience et la valeur p du Test T de Student s'affichent instantanément dans le terminal.
* **Rendu Graphique** : Une fenêtre d'affichage s'ouvre à l'écran (via `matplotlib`). Parallèlement, le graphique bi-volet haute définition est automatiquement enregistré au format PNG dans le même dossier sous le nom `session_[SUJET]_[TIMESTAMP]_graphique.png`. Vous pouvez déplacer ce fichier dans votre dossier `img/` pour mettre à jour votre documentation.
