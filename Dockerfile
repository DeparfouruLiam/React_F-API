# Image Python officielle légère
FROM python:3.11-slim

# Empêche Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Force l'affichage immédiat des logs
ENV PYTHONUNBUFFERED=1

# Dossier de travail dans le container
WORKDIR /app

# Copie des dépendances Python
# Permet d'optimiser le cache Docker
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code backend
COPY *.py ./
COPY database.db ./

# Exposition du port de l'API
EXPOSE 8000

# Commande de démarrage (FastAPI avec Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
