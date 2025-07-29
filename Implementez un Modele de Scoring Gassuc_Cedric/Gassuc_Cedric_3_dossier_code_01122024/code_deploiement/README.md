# PROJET 7 : Implémentez un modèle de scoring

## Dashboard

### Objectif 
La société financière *Prêt à dépenser* propose des crédits à la consommation pour des personnes ayant peu ou pas du tout d'historique de prêt.

#### Implémentation
L’entreprise ambitionne d’instaurer un dispositif de scoring crédit destiné à évaluer avec précision la probabilité qu’un client honore le remboursement de son emprunt. Ce mécanisme permettra ensuite de statuer sur l’octroi ou le rejet de la demande de crédit. À cette fin, elle aspire à concevoir un algorithme de classification fondé sur l’exploitation de sources de données diversifiées, incluant notamment des informations comportementales ainsi que des données en provenance d’autres institutions financières.

### 1. Construire le modèle de machine Learning
- Le code pour construire, entraîner et sauvegarder le modèle se trouve dans le dossier `modele`.

### 2. Créer une API pour le modèle (Flask)
- Implémenter l'application dans `main.py`

### 3. Configurer Google Cloud 
- Créer un nouveau projet
- Activer l'API Cloud Run et l'API Cloud Build

### Installer et initialiser Google Cloud SDK
- [Installer Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- Initialiser avec gcloud init

### 4 Créer le fichier requirements.txt
pip freeze > requirements.txt

### 5. Conteneurisation:  Dockerfile, requirements.txt, .dockerignore
Créer les fichier Dockerfile, et .dockerignore

# 6. Construction et déploiement dans le Cloud

## Créer un dossier dans l'artefact registry et activer le service sur GCP

### Définir les variables
PROJECT_ID="your-project-id"      # Remplacez par votre ID de projet GCP
REGION="europe-west9"             # Remplacez par la région GCP
REPO_NAME="your-repo-name"        # Remplacez par le nom de votre dépôt dans Artifact Registry
IMAGE_NAME="your-image-name"      # Remplacez par le nom de votre image Docker
IMAGE_TAG="your-tag"              # Remplacez par le tag que vous souhaitez utiliser

### Soumettre le build de l'image Docker à Google Container Registry
gcloud builds submit --tag gcr.io/${PROJECT_ID}/${IMAGE_NAME}

### Déployer l'image sur Google Cloud Run
gcloud run deploy --image gcr.io/${PROJECT_ID}/${IMAGE_NAME} --platform managed --region ${REGION}
