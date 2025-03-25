"""
Schémas de données pour l'API.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class BlurSettingsRequest:
    """Paramètres pour configurer le floutage."""
    method: str
    intensity: int
    selected_faces: Optional[List[int]] = None

@dataclass
class DetectionSettingsRequest:
    """Paramètres pour configurer la détection des visages."""
    min_confidence: float
    model_selection: int

@dataclass
class VideoSourceRequest:
    """Paramètres pour configurer la source vidéo."""
    source_type: str  # 'webcam' ou 'file'
    device_id: int = 0  # Pour webcam
    file_path: str = ""  # Pour fichier vidéo

@dataclass
class FaceData:
    """Données d'un visage détecté."""
    bbox: Dict[str, int]  # xmin, ymin, width, height, xmax, ymax
    keypoints: Dict[str, Dict[str, int]]
    score: float
    face_id: Optional[int] = None  # Pour le suivi des visages

@dataclass
class DetectionResponse:
    """Réponse contenant les résultats de la détection des visages."""
    faces: List[FaceData]
    frame_id: int
    timestamp: float
    width: int
    height: int

@dataclass
class ProcessingStatusResponse:
    """Statut du traitement d'une vidéo."""
    status: str  # 'processing', 'completed', 'error'
    progress: float  # 0.0 à 1.0
    frames_processed: int
    total_frames: int
    elapsed_time: float
    estimated_time_remaining: float
    error_message: Optional[str] = None

@dataclass
class VideoProcessingRequest:
    """Requête pour traiter une vidéo complète."""
    input_path: str
    output_path: str
    blur_settings: BlurSettingsRequest
    detection_settings: Optional[DetectionSettingsRequest] = None
    
@dataclass
class VideoStreamSettings:
    """Paramètres pour le streaming vidéo."""
    quality: str = "medium"  # low, medium, high
    fps: int = 30
    width: int = 640
    height: int = 480