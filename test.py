import requests

# URL de l'API en local
url = "http://localhost:8080/predict"

# Préparer les données à envoyer
payload = {
    "message": "For sale - arsenal dartboard. Good condition but no doubles or trebles!"
}

# Envoyer la requête POST à l'API
response = requests.post(url, json=payload)

# Afficher le code de statut et la réponse JSON de l'API
print("Statut :", response.status_code)
print("Réponse :", response.json())
