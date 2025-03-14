from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import re

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

    def do_GET(self):
        if self.path == '/':
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remplacer la variable d'environnement
                api_url = os.getenv('API_URL', 'http://localhost:8080')
                content = content.replace('${API_URL}', api_url)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Erreur lors du chargement de la page: {str(e)}")
        else:
            super().do_GET()

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