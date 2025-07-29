# Utiliser l'image officielle légère de Python.

FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement requirements.txt d'abord (pour optimiser le cache Docker)
COPY requirements.txt ./

# Mettre à jour pip et installer les dépendances  # find / -name "libgomp.so.1"
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# # Installation de libgomp1
RUN apt-get update && apt-get install -y libgomp1

# Copier tout le reste après installation des dépendances
COPY . .

# Exposer le port Flask
EXPOSE 8080

# Lancer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]