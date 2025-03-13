from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Changer le répertoire de travail vers le dossier contenant les fichiers statiques
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Définir le port et l'hôte
host = '0.0.0.0'  # Écouter sur toutes les interfaces
port = 8000

# Créer le serveur avec notre gestionnaire personnalisé
httpd = HTTPServer((host, port), CORSRequestHandler)

print(f"Serveur démarré sur http://{host}:{port}")
print("Appuyez sur Ctrl+C pour arrêter le serveur")

# Démarrer le serveur
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServeur arrêté") 