# Utilise la version 3.8 de l'image de python slim
# On exécute sur une plateforme amd64 pour une compatibilité avec GCP
FROM --platform=linux/amd64 python:3.8-slim as build

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copy le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installe les dépendances définient dans le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy le fichier de notre application(scrape.py) dans le répertoire de travail
COPY scrape.py .

# Exécute notre application au démarrage du conteneur
CMD ["python", "scrape.py"]
