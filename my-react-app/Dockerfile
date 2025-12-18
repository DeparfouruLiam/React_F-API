# =====================
# Étape 1 : build React
# =====================
FROM node:20-alpine AS build

# Dossier de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY package*.json ./

# Installation des dépendances
RUN npm install

# Copie du code source
COPY . .

# Build de l'application Vite
RUN npm run build

# =====================
# Étape 2 : serveur nginx
# =====================
FROM nginx:alpine

# Suppression de la configuration par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Copie des fichiers buildés vers nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Exposition du port HTTP
EXPOSE 80

# Démarrage de nginx
CMD ["nginx", "-g", "daemon off;"]
