FROM python:3.9-alpine

# Installer les dépendances système nécessaires
RUN apk add --no-cache \
    curl \
    bash

# Créer un utilisateur non-root
RUN adduser -D webuser

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les fichiers nécessaires
COPY server.py index.html styles.css ./

# Définir les permissions appropriées
RUN chown -R webuser:webuser /app

# Utiliser l'utilisateur non-root
USER webuser

# Exposer le port
EXPOSE 8000

# Configurer les variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000 || exit 1

# Démarrer le serveur
CMD ["python", "server.py"]

# Métadonnées
LABEL maintainer="Votre Nom" \
      version="1.0" \
      description="Interface web pour la détection de fraude SMS" 