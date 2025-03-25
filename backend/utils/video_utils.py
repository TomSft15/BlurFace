"""
Utilitaires pour la gestion des fichiers vidéo.
"""

import os
import time
import tempfile
import subprocess
import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Callable

class VideoProcessor:
    """Classe pour traiter les fichiers vidéo complets."""
    
    def __init__(self, 
                 input_path: str, 
                 output_path: str, 
                 face_detector, 
                 blur_processor,
                 progress_callback: Optional[Callable[[float, int, int, float, float], None]] = None):
        """
        Initialise le processeur vidéo.
        
        Args:
            input_path: Chemin du fichier vidéo d'entrée
            output_path: Chemin du fichier vidéo de sortie
            face_detector: Instance de FaceDetector
            blur_processor: Instance de BlurProcessor
            progress_callback: Fonction de rappel pour le suivi de la progression
                              (progress, frames_processed, total_frames, elapsed_time, estimated_time_remaining)
        """
        self.input_path = input_path
        self.output_path = output_path
        self.face_detector = face_detector
        self.blur_processor = blur_processor
        self.progress_callback = progress_callback
        
        self.processing_status = {
            "status": "idle",
            "progress": 0.0,
            "frames_processed": 0,
            "total_frames": 0,
            "elapsed_time": 0.0,
            "estimated_time_remaining": 0.0,
            "error_message": None
        }
        
        # Tenter d'obtenir les informations sur la vidéo
        try:
            cap = cv2.VideoCapture(input_path)
            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = cap.get(cv2.CAP_PROP_FPS)
            self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            self.processing_status["total_frames"] = self.total_frames
        except Exception as e:
            self.processing_status["status"] = "error"
            self.processing_status["error_message"] = f"Erreur lors de l'accès à la vidéo: {str(e)}"
    
    def process_video(self, 
                     selected_faces: Optional[List[int]] = None, 
                     draw_detections: bool = False) -> Dict[str, Any]:
        """
        Traite la vidéo complète en détectant et floutant les visages.
        
        Args:
            selected_faces: Liste des indices des visages à flouter (None = tous)
            draw_detections: Si True, dessine les rectangles de détection
            
        Returns:
            Dictionnaire avec le statut final du traitement
        """
        # Mise à jour du statut
        self.processing_status["status"] = "processing"
        self.processing_status["progress"] = 0.0
        self.processing_status["frames_processed"] = 0
        self.processing_status["elapsed_time"] = 0.0
        self.processing_status["estimated_time_remaining"] = 0.0
        
        start_time = time.time()
        
        try:
            # Ouvrir la vidéo d'entrée
            cap = cv2.VideoCapture(self.input_path)
            
            if not cap.isOpened():
                raise ValueError(f"Impossible d'ouvrir la vidéo: {self.input_path}")
            
            # Créer le dossier de sortie si nécessaire
            output_dir = os.path.dirname(self.output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Configurer l'encodeur vidéo
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec MP4
            out = cv2.VideoWriter(
                self.output_path, 
                fourcc, 
                self.fps, 
                (self.width, self.height)
            )
            
            # Traiter chaque image
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Détecter les visages
                _, faces_data = self.face_detector.detect_faces(frame)
                
                # Appliquer le floutage
                processed_frame = self.blur_processor.blur_faces(frame, faces_data, selected_faces)
                
                # Dessiner les détections si demandé
                if draw_detections:
                    processed_frame = self.face_detector.draw_detections(processed_frame, faces_data)
                
                # Écrire l'image traitée
                out.write(processed_frame)
                
                # Mise à jour du statut
                self.processing_status["frames_processed"] += 1
                current_progress = self.processing_status["frames_processed"] / self.total_frames
                self.processing_status["progress"] = current_progress
                
                # Calcul du temps restant
                elapsed_time = time.time() - start_time
                self.processing_status["elapsed_time"] = elapsed_time
                
                if current_progress > 0:
                    estimated_total_time = elapsed_time / current_progress
                    estimated_time_remaining = estimated_total_time - elapsed_time
                    self.processing_status["estimated_time_remaining"] = estimated_time_remaining
                
                # Appel de la fonction de rappel si elle existe
                if self.progress_callback:
                    self.progress_callback(
                        current_progress,
                        self.processing_status["frames_processed"],
                        self.total_frames,
                        elapsed_time,
                        self.processing_status["estimated_time_remaining"]
                    )
            
            # Libérer les ressources
            cap.release()
            out.release()
            
            # Finaliser le statut
            self.processing_status["status"] = "completed"
            self.processing_status["progress"] = 1.0
            
        except Exception as e:
            # En cas d'erreur, mettre à jour le statut
            self.processing_status["status"] = "error"
            self.processing_status["error_message"] = str(e)
            
            # Libérer les ressources en cas d'erreur
            if 'cap' in locals() and cap is not None:
                cap.release()
            if 'out' in locals() and out is not None:
                out.release()
        
        return self.processing_status
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel du traitement."""
        return self.processing_status


def get_video_info(video_path: str) -> Dict[str, Any]:
    """
    Récupère les informations sur une vidéo.
    
    Args:
        video_path: Chemin du fichier vidéo
        
    Returns:
        Dictionnaire contenant les informations de la vidéo
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {
                "success": False,
                "error": f"Impossible d'ouvrir la vidéo: {video_path}"
            }
        
        info = {
            "success": True,
            "path": video_path,
            "filename": os.path.basename(video_path),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "duration": int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)),
            "format": os.path.splitext(video_path)[1][1:].upper()
        }
        
        # Calculer la durée au format hh:mm:ss
        total_seconds = info["duration"]
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        info["duration_str"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        cap.release()
        return info
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def extract_frame(video_path: str, frame_number: int) -> Tuple[bool, Optional[np.ndarray]]:
    """
    Extrait une image spécifique d'une vidéo.
    
    Args:
        video_path: Chemin du fichier vidéo
        frame_number: Numéro de l'image à extraire
        
    Returns:
        Tuple (succès, image)
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, None
        
        # Vérifier que le numéro d'image est valide
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_number < 0 or frame_number >= total_frames:
            cap.release()
            return False, None
        
        # Positionner le curseur à l'image souhaitée
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Lire l'image
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return False, None
        
        return True, frame
        
    except Exception:
        return False, None


def get_available_webcams() -> List[Dict[str, Any]]:
    """
    Détecte les webcams disponibles sur le système.
    
    Returns:
        Liste des webcams disponibles avec leurs informations
    """
    available_cameras = []
    
    # Tester les 10 premiers indices de caméra (0-9)
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Récupérer les informations de la caméra
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            available_cameras.append({
                "device_id": i,
                "name": f"Caméra {i}",
                "width": width,
                "height": height,
                "fps": fps
            })
            
            # Libérer la caméra
            cap.release()
    
    return available_cameras