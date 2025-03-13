# Étape 1 : Builder avec outils de compilation
FROM python:3.8-slim as builder

WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Installer les dépendances avec PyTorch CPU
RUN pip install --no-cache-dir -r requirements.txt

# Télécharger les modèles pendant le build
#RUN pip install --no-cache-dir huggingface_hub
#RUN pip install --no-cache-dir --upgrade huggingface_hub
#RUN python3 -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='distilbert-base-uncased', local_dir='models/distilbert-base-uncased')"
#RUN python3 -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='MrNWARMeilleur/sms_fraud_detection', local_dir='models/sms_fraud_detection')"

# Étape 2 : Image finale
FROM python:3.8-slim

WORKDIR /app

# Installer curl pour le healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python depuis le builder
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier le code applicatif et les requirements
COPY app.py requirements.txt ./

# Créer un utilisateur non-root
RUN useradd -m -U appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/docs || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]