# =====================
# IMAGE DE BASE
# =====================
FROM python:3.11-slim

# =====================
# VARIABLES D'ENVIRONNEMENT
# =====================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =====================
# DOSSIER DE TRAVAIL
# =====================
WORKDIR /app

# =====================
# INSTALLATION DES DÉPENDANCES
# =====================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =====================
# COPIE DU CODE SOURCE
# =====================
COPY . .

# =====================
# PORT À EXPOSER
# =====================
EXPOSE 8000

# =====================
# COMMANDE DE LANCEMENT
# =====================
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
