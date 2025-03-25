"""
Routes API pour l'application Blur Face utilisant Flask-RESTX.
"""

import os
import time
import json
import uuid
from typing import Dict, List, Any, Optional
import cv2
import numpy as np
from flask import Flask, request, Response, send_from_directory, jsonify
from flask_restx import Api, Resource, fields, Namespace
import base64
from copy import deepcopy


from core.face_detector import FaceDetector
from core.blur_processor import BlurProcessor
from utils.video_utils import get_available_webcams, get_video_info
import config

# Dictionnaire pour stocker les sessions actives
ACTIVE_SESSIONS = {}

class VideoSession:
    """Classe pour gérer une session vidéo."""
    
    def __init__(self, session_id: str, source_type: str, device_id: int = 0, file_path: str = ""):
        self.session_id = session_id
        self.source_type = source_type
        self.device_id = device_id
        self.file_path = file_path
        self.cap = None
        self.face_detector = FaceDetector(
            min_detection_confidence=config.FACE_DETECTION_CONFIDENCE,
            model_selection=1
        )
        self.blur_processor = BlurProcessor(
            blur_method=config.DEFAULT_BLUR_METHOD,
            blur_intensity=config.DEFAULT_BLUR_INTENSITY
        )
        self.is_running = False
        self.frame_count = 0
        self.selected_faces = None
        self.last_frame = None
        
    def start(self) -> bool:
        """Démarre la session vidéo."""
        try:
            if self.source_type == "webcam":
                self.cap = cv2.VideoCapture(self.device_id)
            elif self.source_type == "file" and os.path.exists(self.file_path):
                self.cap = cv2.VideoCapture(self.file_path)
            else:
                return False
            
            if not self.cap.isOpened():
                return False
                
            self.is_running = True
            return True
        except Exception as e:
            print(f"Erreur lors du démarrage de la session: {e}")
            return False
            
    def stop(self):
        """Arrête la session vidéo."""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        self.face_detector.release()
            
    def get_frame(self) -> Optional[np.ndarray]:
        """Récupère une image de la source vidéo."""
        try:
            if not self.is_running or self.cap is None:
                print("Session not running or capture not initialized")
                return None
                
            ret, frame = self.cap.read()
            if not ret or frame is None or frame.size == 0:
                print("Failed to read frame or empty frame")
                # Réinitialiser la capture si possible
                if self.source_type == "webcam":
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.device_id)
                elif self.source_type == "file":
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.file_path)
                
                # Vérifier à nouveau après réinitialisation
                ret, frame = self.cap.read()
                if not ret or frame is None or frame.size == 0:
                    print("Capture still unable to read frame")
                    self.is_running = False
                    return None
                
            self.frame_count += 1
            self.last_frame = frame
            return frame
        except Exception as e:
            print(f"Error in get_frame: {e}")
            self.is_running = False
            return None
        
    def process_frame(self, frame: np.ndarray, draw_detections: bool = False, apply_blur: bool = True) -> Dict[str, Any]:
        """Traite une image pour détecter et flouter les visages."""
        try:
            # Vérifier que le frame n'est pas vide
            if frame is None or frame.size == 0:
                print("Empty frame received in process_frame")
                return {
                    "frame": np.zeros((480, 640, 3), dtype=np.uint8),  # Default blank frame
                    "detection_data": {
                        "faces": [],
                        "frame_id": self.frame_count,
                        "timestamp": time.time(),
                        "width": 640,
                        "height": 480
                    }
                }
            
            # Détecter les visages
            _, faces_data = self.face_detector.detect_faces(frame)
            
            result_frame = frame.copy()
            
            # Appliquer le floutage si demandé
            if apply_blur and faces_data:
                # Ajouter une vérification supplémentaire
                if result_frame.size > 0:
                    result_frame = self.blur_processor.blur_faces(result_frame, faces_data, self.selected_faces)
                else:
                    print("Cannot apply blur to empty frame")
            
            # Dessiner les rectangles de détection si demandé
            if draw_detections:
                result_frame = self.face_detector.draw_detections(result_frame, faces_data)
            
            # Préparer la réponse
            height, width = frame.shape[:2]
            
            response = {
                "faces": [
                    {
                        "bbox": face.get("bbox", {}),
                        "keypoints": face.get("keypoints", {}),
                        "score": face.get("score", 0.0),
                        "face_id": idx
                    }
                    for idx, face in enumerate(faces_data)
                ],
                "frame_id": self.frame_count,
                "timestamp": time.time(),
                "width": width,
                "height": height
            }
            
            return {"frame": result_frame, "detection_data": response}
        except Exception as e:
            print(f"Erreur détaillée lors du traitement de l'image : {e}")
            # Retourner un frame vide en cas d'erreur
            return {
                "frame": np.zeros((480, 640, 3), dtype=np.uint8),
                "detection_data": {
                    "faces": [],
                    "frame_id": self.frame_count,
                    "timestamp": time.time(),
                    "width": 640,
                    "height": 480
                }
            }

def configure_routes(app: Flask, api: Api):
    """Configure les routes pour l'application Flask avec Flask-RESTX."""
    
    # Création des namespaces
    ns_status = api.namespace('status', description='Vérifier l\'état du service')
    ns_session = api.namespace('session', description='Gestion des sessions vidéo')
    ns_webcams = api.namespace('webcams', description='Gestion des webcams')
    ns_videos = api.namespace('videos', description='Gestion des vidéos')
    
    # Modèles Swagger pour la documentation
    status_model = api.model('Status', {
        'status': fields.String(required=True, description='État du service'),
        'version': fields.String(required=True, description='Version de l\'API'),
        'timestamp': fields.Float(required=True, description='Horodatage de la requête')
    })
    
    video_source_model = api.model('VideoSource', {
        'source_type': fields.String(required=True, description='Type de source (webcam ou file)', enum=['webcam', 'file']),
        'device_id': fields.Integer(description='ID du périphérique pour webcam'),
        'file_path': fields.String(description='Chemin du fichier pour vidéo')
    })
    
    session_response_model = api.model('SessionResponse', {
        'success': fields.Boolean(required=True, default=True),
        'session_id': fields.String(required=True, description='Identifiant de la session')
    })
    
    success_model = api.model('Success', {
        'success': fields.Boolean(required=True, default=True)
    })
    
    error_model = api.model('Error', {
        'success': fields.Boolean(required=True, default=False),
        'error': fields.String(required=True, description='Message d\'erreur')
    })
    
    keypoint_model = api.model('Keypoint', {
        'x': fields.Integer(required=True, description='Coordonnée X du point clé'),
        'y': fields.Integer(required=True, description='Coordonnée Y du point clé')
    })
    
    bbox_model = api.model('BoundingBox', {
        'xmin': fields.Integer(required=True, description='Coordonnée X minimale'),
        'ymin': fields.Integer(required=True, description='Coordonnée Y minimale'),
        'width': fields.Integer(required=True, description='Largeur du rectangle'),
        'height': fields.Integer(required=True, description='Hauteur du rectangle'),
        'xmax': fields.Integer(required=True, description='Coordonnée X maximale'),
        'ymax': fields.Integer(required=True, description='Coordonnée Y maximale'),
        'score': fields.Float(required=True, description='Score de confiance')
    })
    
    face_model = api.model('Face', {
        'bbox': fields.Nested(bbox_model, required=True, description='Rectangle englobant'),
        'keypoints': fields.Raw(description='Points clés du visage'),
        'score': fields.Float(required=True, description='Score de confiance'),
        'face_id': fields.Integer(description='ID du visage pour le suivi')
    })
    
    detection_response_model = api.model('DetectionResponse', {
        'success': fields.Boolean(required=True, default=True),
        'faces': fields.List(fields.Nested(face_model), description='Visages détectés'),
        'frame_id': fields.Integer(required=True, description='ID de l\'image'),
        'timestamp': fields.Float(required=True, description='Horodatage'),
        'width': fields.Integer(required=True, description='Largeur de l\'image'),
        'height': fields.Integer(required=True, description='Hauteur de l\'image')
    })
    
    blur_settings_model = api.model('BlurSettings', {
        'method': fields.String(description='Méthode de floutage', enum=['gaussian', 'pixelate', 'solid']),
        'intensity': fields.Integer(description='Intensité du floutage', min=1, max=100),
        'selected_faces': fields.List(fields.Integer, description='Indices des visages à flouter')
    })
    
    detection_settings_model = api.model('DetectionSettings', {
        'min_confidence': fields.Float(description='Seuil de confiance minimal', min=0.0, max=1.0),
        'model_selection': fields.Integer(description='Sélection du modèle', enum=[0, 1])
    })
    
    webcam_model = api.model('Webcam', {
        'device_id': fields.Integer(required=True, description='ID du périphérique'),
        'name': fields.String(required=True, description='Nom de la webcam'),
        'width': fields.Integer(required=True, description='Largeur de l\'image'),
        'height': fields.Integer(required=True, description='Hauteur de l\'image'),
        'fps': fields.Float(required=True, description='Images par seconde')
    })
    
    webcams_list_model = api.model('WebcamsList', {
        'webcams': fields.List(fields.Nested(webcam_model), description='Liste des webcams disponibles')
    })
    
    video_info_model = api.model('VideoInfo', {
        'success': fields.Boolean(required=True),
        'path': fields.String(description='Chemin du fichier'),
        'filename': fields.String(description='Nom du fichier'),
        'width': fields.Integer(description='Largeur de la vidéo'),
        'height': fields.Integer(description='Hauteur de la vidéo'),
        'fps': fields.Float(description='Images par seconde'),
        'frame_count': fields.Integer(description='Nombre total d\'images'),
        'duration': fields.Integer(description='Durée en secondes'),
        'duration_str': fields.String(description='Durée au format HH:MM:SS'),
        'format': fields.String(description='Format de la vidéo')
    })
    
    # Route pour vérifier que l'API est en ligne
    @ns_status.route('')
    class StatusResource(Resource):
        @ns_status.doc('get_status')
        @ns_status.marshal_with(status_model)
        def get(self):
            """Vérifier que l'API est en ligne"""
            return {
                "status": "online",
                "version": "1.0.0",
                "timestamp": time.time()
            }
    
    # Liste des webcams disponibles
    @ns_webcams.route('')
    class WebcamsResource(Resource):
        @ns_webcams.doc('get_webcams')
        @ns_webcams.marshal_with(webcams_list_model)
        def get(self):
            """Récupérer la liste des webcams disponibles"""
            return {"webcams": get_available_webcams()}
    
    # Créer une nouvelle session vidéo
    @ns_session.route('/create')
    class SessionCreateResource(Resource):
        @ns_session.doc('create_session')
        @ns_session.expect(video_source_model)
        # @ns_session.marshal_with(session_response_model, code=200)
        # @ns_session.marshal_with(error_model, code=400)
        def post(self):
            """Créer une nouvelle session vidéo"""
            try:
                # Ensure JSON data is present
                if not request.json:
                    return {
                        "success": False,
                        "error": "Aucune donnée JSON fournie"
                    }, 400
                
                # Extract data safely
                data = request.json
                source_type = data.get('source_type', 'webcam')
                device_id = data.get('device_id', 0)
                file_path = data.get('file_path', '')
                
                # Validate source type
                if source_type not in ['webcam', 'file']:
                    return {
                        "success": False,
                        "error": "Type de source invalide. Doit être 'webcam' ou 'file'."
                    }, 400
                
                # Generate a more robust session ID
                session_id = str(uuid.uuid4())
                
                # Créer et démarrer la session
                session = VideoSession(session_id, source_type, device_id, file_path)
                
                if not session.start():
                    return {
                        "success": False,
                        "error": "Impossible de démarrer la session vidéo"
                    }, 400
                
                # Stocker la session
                ACTIVE_SESSIONS[session_id] = session
                
                print(f"Session créée avec ID: {session_id}")
                
                print(f"Data type: {type(session_id)}")
                
                # Retourner explicitement un dictionnaire avec les clés attendues
                return {
                    'success': True,
                    'session_id': session_id
                }
            
            except Exception as e:
                # Log any unexpected errors
                print(f"Unexpected error in session creation: {e}")
                return {
                    "success": False,
                    "error": f"Erreur inattendue: {str(e)}"
                }, 500
    
    # Fermer une session vidéo
    @ns_session.route('/<string:session_id>/close')
    @ns_session.param('session_id', 'Identifiant de la session')
    class SessionCloseResource(Resource):
        @ns_session.doc('close_session')
        @ns_session.marshal_with(success_model, code=200)
        @ns_session.marshal_with(error_model, code=404)
        def post(self, session_id):
            """Fermer une session vidéo"""
            if session_id in ACTIVE_SESSIONS:
                ACTIVE_SESSIONS[session_id].stop()
                del ACTIVE_SESSIONS[session_id]
                return {"success": True}
            
            return {
                "success": False,
                "error": "Session non trouvée"
            }, 404
    
    # Mettre à jour les paramètres de floutage
    @ns_session.route('/<string:session_id>/blur-settings')
    @ns_session.param('session_id', 'Identifiant de la session')
    class BlurSettingsResource(Resource):
        @ns_session.doc('update_blur_settings')
        @ns_session.expect(blur_settings_model)
        @ns_session.marshal_with(success_model, code=200)
        @ns_session.marshal_with(error_model, code=404)
        def put(self, session_id):
            """Mettre à jour les paramètres de floutage"""
            if session_id not in ACTIVE_SESSIONS:
                return {
                    "success": False,
                    "error": "Session non trouvée"
                }, 404
            
            data = request.json
            session = ACTIVE_SESSIONS[session_id]
            
            if 'method' in data:
                session.blur_processor.set_blur_method(data['method'])
            
            if 'intensity' in data:
                session.blur_processor.set_blur_intensity(data['intensity'])
            
            if 'selected_faces' in data:
                session.selected_faces = data['selected_faces']
            
            return {"success": True}
    
    # Mettre à jour les paramètres de détection
    @ns_session.route('/<string:session_id>/detection-settings')
    @ns_session.param('session_id', 'Identifiant de la session')
    class DetectionSettingsResource(Resource):
        @ns_session.doc('update_detection_settings')
        @ns_session.expect(detection_settings_model)
        @ns_session.marshal_with(success_model, code=200)
        @ns_session.marshal_with(error_model, code=404)
        def put(self, session_id):
            """Mettre à jour les paramètres de détection des visages"""
            if session_id not in ACTIVE_SESSIONS:
                return {
                    "success": False,
                    "error": "Session non trouvée"
                }, 404
            
            data = request.json
            session = ACTIVE_SESSIONS[session_id]
            
            # Créer un nouveau détecteur avec les nouveaux paramètres
            if 'min_confidence' in data or 'model_selection' in data:
                min_confidence = data.get('min_confidence', config.FACE_DETECTION_CONFIDENCE)
                model_selection = data.get('model_selection', 1)
                
                # Libérer l'ancien détecteur
                session.face_detector.release()
                
                # Créer un nouveau détecteur
                session.face_detector = FaceDetector(
                    min_detection_confidence=min_confidence,
                    model_selection=model_selection
                )
            
            return {"success": True}
    
    # Récupérer une image détectée/floutée
    @ns_session.route('/<string:session_id>/frame')
    @ns_session.param('session_id', 'Identifiant de la session')
    class FrameResource(Resource):
        @ns_session.doc('get_processed_frame')
        def get(self, session_id):
            """Récupérer une image traitée avec détection/floutage"""
            if session_id not in ACTIVE_SESSIONS:
                return {
                    "success": False,
                    "error": "Session non trouvée"
                }, 404
            
            session = ACTIVE_SESSIONS[session_id]
            
            # Obtenir et traiter une nouvelle image
            frame = session.get_frame()
            if frame is None:
                return {
                    "success": False,
                    "error": "Impossible de récupérer une image"
                }, 400
            
            # Options de traitement
            draw_detections = request.args.get('draw_detections', 'false').lower() == 'true'
            apply_blur = request.args.get('apply_blur', 'true').lower() == 'true'
            
            # Traiter l'image
            result = session.process_frame(frame, draw_detections, apply_blur)
            
            # Encoder l'image en base64
            _, buffer = cv2.imencode('.jpg', result["frame"])
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Retourner l'image et les données de détection
            return {
                "success": True,
                "frame": img_base64,
                "detection_data": result["detection_data"]
            }
    
    # Récupérer les données de détection
    @ns_session.route('/<string:session_id>/detections')
    @ns_session.param('session_id', 'Identifiant de la session')
    class DetectionsResource(Resource):
        @ns_session.doc('get_detections')
        @ns_session.marshal_with(detection_response_model)
        def get(self, session_id):
            """Récupérer les données de détection des visages"""
            try:
                if session_id not in ACTIVE_SESSIONS:
                    return {
                        "success": False,
                        "error": "Session non trouvée"
                    }, 404
                
                session = ACTIVE_SESSIONS[session_id]
                
                # Utiliser la dernière image traitée si disponible
                if session.last_frame is None:
                    frame = session.get_frame()
                    if frame is None:
                        return {
                            "success": False,
                            "error": "Impossible de récupérer une image"
                        }, 400
                else:
                    frame = session.last_frame
                
                # Détecter les visages sans appliquer de floutage ni dessiner
                _, faces_data = session.face_detector.detect_faces(frame)
                
                # Préparer la réponse
                height, width = frame.shape[:2]
                
                return {
                    "success": True,
                    "faces": [
                        {
                            "bbox": face.get("bbox", {}),
                            "keypoints": face.get("keypoints", {}),
                            "score": face.get("score", 0.0),
                            "face_id": idx
                        }
                        for idx, face in enumerate(faces_data)
                    ],
                    "frame_id": session.frame_count,
                    "timestamp": time.time(),
                    "width": width,
                    "height": height
                }
            except Exception as e:
                print(f"Erreur lors de la récupération des détections : {e}")
                return {
                    "success": False,
                    "error": f"Erreur inattendue : {str(e)}"
                }, 500
    
    # Obtenir les informations d'une vidéo
    @ns_videos.route('/info')
    class VideoInfoResource(Resource):
        @ns_videos.doc('get_video_info')
        @ns_videos.expect(api.model('VideoInfoRequest', {
            'file_path': fields.String(required=True, description='Chemin du fichier vidéo')
        }))
        @ns_videos.marshal_with(video_info_model)
        def post(self):
            """Récupérer les informations d'un fichier vidéo"""
            data = request.json
            file_path = data.get('file_path')
            
            if not file_path or not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": "Chemin de fichier invalide"
                }, 400
            
            # Utiliser la fonction get_video_info des utilitaires vidéo
            return get_video_info(file_path)
    
    # Stream vidéo (MJPEG)
    @ns_session.route('/<string:session_id>/stream')
    @ns_session.param('session_id', 'Identifiant de la session')
    class VideoStreamResource(Resource):
        def get(self, session_id):
            """Streamer le flux vidéo avec traitement"""
            if session_id not in ACTIVE_SESSIONS:
                return {
                    "success": False,
                    "error": "Session non trouvée"
                }, 404
            
            # Extract parameters before creating the generator
            draw_detections = request.args.get('draw_detections', 'false').lower() == 'true'
            apply_blur = request.args.get('apply_blur', 'true').lower() == 'true'
            
            def generate_frames(draw_detections, apply_blur):
                session = ACTIVE_SESSIONS[session_id]
                error_count = 0
                max_errors = 10  # Nombre maximal d'erreurs avant d'arrêter
                
                while session.is_running and error_count < max_errors:
                    try:
                        frame = session.get_frame()
                        if frame is None:
                            error_count += 1
                            print(f"Frame read failed. Error count: {error_count}")
                            time.sleep(0.1)  # Petit délai pour éviter une boucle trop rapide
                            continue
                        
                        # Réinitialiser le compteur d'erreurs si un frame est lu avec succès
                        error_count = 0
                        
                        # Traiter l'image
                        result = session.process_frame(frame, draw_detections, apply_blur)
                        
                        # Convertir l'image pour le streaming
                        _, buffer = cv2.imencode('.jpg', result["frame"])
                        frame_bytes = buffer.tobytes()
                        
                        # Envoyer l'image au format MJPEG
                        yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                        
                        # Limiter le fps pour économiser les ressources
                        time.sleep(1/30)  # 30 FPS maximum
                    
                    except Exception as e:
                        print(f"Erreur dans generate_frames: {e}")
                        error_count += 1
                        time.sleep(0.1)
                
                # Arrêter la session si trop d'erreurs
                if error_count >= max_errors:
                    print("Trop d'erreurs, arrêt de la session")
                    session.stop()
            
            return Response(
                generate_frames(draw_detections, apply_blur),
                mimetype='multipart/x-mixed-replace; boundary=frame'
            )