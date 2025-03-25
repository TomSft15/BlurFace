"""
Point d'entrée principal pour l'application Blur Face.
"""
import os
import argparse
import time
import logging
from flask import Flask, send_from_directory
from flask_restx import Api
from flask_cors import CORS

import config
from api.routes import configure_routes

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(config.BASE_DIR, 'blur_face.log'))
    ]
)
logger = logging.getLogger('blur_face')

def parse_arguments():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(description="Blur Face - Application de floutage de visages vidéo")
    parser.add_argument("--debug", action="store_true", help="Exécuter en mode debug")
    parser.add_argument("--port", type=int, default=5000, help="Port pour le serveur web")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Hôte pour le serveur web")
    return parser.parse_args()

def create_app():
    """Crée et configure l'application Flask."""
    app = Flask(__name__, static_folder='frontend/dist')
    
    # Configuration de l'application
    app.config['UPLOAD_FOLDER'] = config.TEMP_DIR
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max upload
    
    # Activer CORS
    CORS(app)
    
    # Initialiser l'API Flask-RESTX
    api = Api(
        app,
        version='1.0.0',
        title='BlurFace API',
        description='API pour l\'application de floutage de visages dans les vidéos',
        doc='/api/docs',
        validate=True
    )
    
    # Configurer les routes
    configure_routes(app, api)
    
    # Route pour la page d'accueil (frontend)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    # Route pour les téléchargements
    @app.route('/downloads/<path:filename>')
    def download_file(filename):
        return send_from_directory(config.OUTPUT_DIR, filename, as_attachment=True)
    
    return app

if __name__ == "__main__":
    args = parse_arguments()
    app = create_app()
    
    logger.info(f"Démarrage du serveur Blur Face sur {args.host}:{args.port}")
    app.run(debug=args.debug, host=args.host, port=args.port)