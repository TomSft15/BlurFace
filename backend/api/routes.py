"""
Routes API pour l'application Blur Face.
"""

import os
import time
import json
import uuid
from typing import Dict, List, Any, Optional
import cv2
import numpy as np
from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS

from core.face_detector import FaceDetector
from core.blur_processor import BlurProcessor
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
        if not self.is_running or self.cap is None:
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        self.frame_count += 1
        self.last_frame = frame
        return frame
        
    def process_frame(self, frame: np.ndarray, draw_detections: bool = False, apply_blur: bool = True) -> Dict[str, Any]:
        """Traite une image pour détecter et flouter les visages."""
        # Détecter les visages
        _, faces_data = self.face_detector.detect_faces(frame)
        
        result_frame = frame.copy()
        
        # Appliquer le floutage si demandé
        if apply_blur and faces_data:
            result_frame = self.blur_processor.blur_faces(result_frame, faces_data, self.selected_faces)
        
        # Dessiner les rectangles de détection si demandé
        if draw_detections:
            result_frame = self.face_detector.draw_detections(result_frame, faces_data)
        
        # Préparer la réponse
        height, width = frame.shape[:2]
        
        response = {
            "faces": [
                {
                    "bbox": face["bbox"],
                    "keypoints": face["keypoints"],
                    "score": face["score"],
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


def configure_routes(app: Flask):
    """Configure les routes pour l'application Flask."""
    
    # Activer CORS pour permettre les requêtes cross-origin
    CORS(app)
    
    # Route pour vérifier que l'API est en ligne
    @app.route('/api/status', methods=['GET'])
    def status():
        return jsonify({
            "status": "online",
            "version": "1.0.0",
            "timestamp": time.time()
        })
    
    # Créer une nouvelle session vidéo
    @app.route('/api/session/create', methods=['POST'])
    def create_session():
        data = request.json
        source_type = data.get('source_type', 'webcam')
        device_id = data.get('device_id', 0)
        file_path = data.get('file_path', '')
        
        session_id = str(uuid.uuid4())
        
        # Créer et démarrer la session
        session = VideoSession(session_id, source_type, device_id, file_path)
        if not session.start():
            return jsonify({
                "success": False,
                "error": "Impossible de démarrer la session vidéo"
            }), 400
        
        # Stocker la session
        ACTIVE_SESSIONS[session_id] = session
        
        return jsonify({
            "success": True,
            "session_id": session_id
        })
    
    # Fermer une session vidéo
    @app.route('/api/session/<session_id>/close', methods=['POST'])
    def close_session(session_id):
        if session_id in ACTIVE_SESSIONS:
            ACTIVE_SESSIONS[session_id].stop()
            del ACTIVE_SESSIONS[session_id]
            return jsonify({"success": True})
        
        return jsonify({
            "success": False,
            "error": "Session non trouvée"
        }), 404
    
    # Mettre à jour les paramètres de floutage
    @app.route('/api/session/<session_id>/blur-settings', methods=['PUT'])
    def update_blur_settings(session_id):
        if session_id not in ACTIVE_SESSIONS:
            return jsonify({
                "success": False,
                "error": "Session non trouvée"
            }), 404
        
        data = request.json
        
        # Mettre à jour les paramètres
        session = ACTIVE_SESSIONS[session_id]
        
        if 'method' in data:
            session.blur_processor.set_blur_method(data['method'])
        
        if 'intensity' in data:
            session.blur_processor.set_blur_intensity(data['intensity'])
        
        if 'selected_faces' in data:
            session.selected_faces = data['selected_faces']
        
        return jsonify({"success": True})
    
    # Mettre à jour les paramètres de détection
    @app.route('/api/session/<session_id>/detection-settings', methods=['PUT'])
    def update_detection_settings(session_id):
        if session_id not in ACTIVE_SESSIONS:
            return jsonify({
                "success": False,
                "error": "Session non trouvée"
            }), 404
        
        data = request.json
        
        # Créer un nouveau détecteur avec les nouveaux paramètres
        if 'min_confidence' in data or 'model_selection' in data:
            session = ACTIVE_SESSIONS[session_id]
            
            min_confidence = data.get('min_confidence', config.FACE_DETECTION_CONFIDENCE)
            model_selection = data.get('model_selection', 1)
            
            # Libérer l'ancien détecteur
            session.face_detector.release()
            
            # Créer un nouveau détecteur
            session.face_detector = FaceDetector(
                min_detection_confidence=min_confidence,
                model_selection=model_selection
            )
        
        return jsonify({"success": True})
    
    # Récupérer une image détectée/floutée
    @app.route('/api/session/<session_id>/frame', methods=['GET'])
    def get_processed_frame(session_id):
        if session_id not in ACTIVE_SESSIONS:
            return jsonify({
                "success": False,
                "error": "Session non trouvée"
            }), 404
        
        session = ACTIVE_SESSIONS[session_id]
        
        # Obtenir et traiter une nouvelle image
        frame = session.get_frame()
        if frame is None:
            return jsonify({
                "success": False,
                "error": "Impossible de récupérer une image"
            }), 400
        
        # Options de traitement
        draw_detections = request.args.get('draw_detections', 'false').lower() == 'true'
        apply_blur = request.args.get('apply_blur', 'true').lower() == 'true'
        
        # Traiter l'image
        result = session.process_frame(frame, draw_detections, apply_blur)
        
        # Convertir l'image pour l'envoi
        _, img_encoded = cv2.imencode('.jpg', result["frame"])
        
        # Créer une réponse multipart avec l'image et les données de détection
        response = Response(
            img_encoded.tobytes(),
            mimetype='image/jpeg'
        )
        
        # Ajouter les données de détection dans l'en-tête
        response.headers['X-Detection-Data'] = json.dumps(result["detection_data"])
        
        return response
    
    # Stream vidéo (MJPEG)
    @app.route('/api/session/<session_id>/stream', methods=['GET'])
    def video_stream(session_id):
        if session_id not in ACTIVE_SESSIONS:
            return jsonify({
                "success": False,
                "error": "Session non trouvée"
            }), 404
        
        def generate_frames():
            session = ACTIVE_SESSIONS[session_id]
            
            # Options de traitement
            draw_detections = request.args.get('draw_detections', 'false').lower() == 'true'
            apply_blur = request.args.get('apply_blur', 'true').lower() == 'true'
            
            while session.is_running:
                frame = session.get_frame()
                if frame is None:
                    break
                
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
        
        return Response(
            generate_frames(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    
    # Récupérer les données de détection (sans l'image)
    @app.route('/api/session/<session_id>/detections', methods=['GET'])
    def get_detections(session_id):
        if session_id not in ACTIVE_SESSIONS:
            return jsonify({
                "success": False,
                "error": "Session non trouvée"
            }), 404
        
        session = ACTIVE_SESSIONS[session_id]
        
        # Utiliser la dernière image traitée si disponible
        if session.last_frame is None:
            frame = session.get_frame()
            if frame is None:
                return jsonify({
                    "success": False,
                    "error": "Impossible de récupérer une image"
                }), 400
        else:
            frame = session.last_frame
        
        # Détecter les visages sans appliquer de floutage ni dessiner
        _, faces_data = session.face_detector.detect_faces(frame)
        
        # Préparer la réponse
        height, width = frame.shape[:2]
        
        response = {
            "success": True,
            "faces": [
                {
                    "bbox": face["bbox"],
                    "keypoints": face["keypoints"],
                    "score": face["score"],
                    "face_id": idx
                }
                for idx, face in enumerate(faces_data)
            ],
            "frame_id": session.frame_count,
            "timestamp": time.time(),
            "width": width,
            "height": height
        }
        
        return jsonify(response)