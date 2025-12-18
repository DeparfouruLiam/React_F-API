# =====================
# ÉTAPE 1 : BUILD REACT
# =====================
FROM node:20-alpine AS build

WORKDIR /app

# Copier et installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le code source
COPY . .

# Définir la variable d'environnement pour le backend
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build pour production
RUN npm run build

# =====================
# ÉTAPE 2 : SERVEUR NGINX
# =====================
FROM nginx:alpine

# Copier le build React
COPY --from=build /app/dist /usr/share/nginx/html

# Copier la configuration nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port HTTP
EXPOSE 80

# Démarrer nginx
CMD ["nginx", "-g", "daemon off;"]
