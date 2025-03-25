"""
Module pour la détection de visages utilisant MediaPipe.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import List, Dict, Any, Tuple

class FaceDetector:
    """
    Classe pour détecter les visages dans les images ou les flux vidéo 
    en utilisant MediaPipe.
    """

    def __init__(self, min_detection_confidence: float = 0.5, model_selection: int = 1):
        """
        Initialise le détecteur de visages.
        
        Args:
            min_detection_confidence: Seuil de confiance minimum pour la détection
            model_selection: 0 pour les visages à courte distance (<2m), 1 pour les visages à longue distance (<5m)
        """
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.min_detection_confidence = min_detection_confidence
        self.model_selection = model_selection
        
        # Initialise le détecteur de visages
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=self.min_detection_confidence,
            model_selection=self.model_selection
        )

    def detect_faces(self, image: np.ndarray) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Détecte les visages dans une image.
        
        Args:
            image: Image au format numpy array (BGR)
            
        Returns:
            Tuple contenant:
                - L'image annotée avec les détections (si draw est True)
                - Liste des visages détectés avec leurs coordonnées et scores
        """
        # Convertir l'image BGR en RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = image.shape
        
        # Traiter l'image avec MediaPipe
        results = self.face_detection.process(image_rgb)
        
        # Préparer les données à retourner
        faces_data = []
        
        # Traiter les résultats
        if results.detections:
            for detection in results.detections:
                # Obtenir le rectangle englobant (bounding box)
                bboxC = detection.location_data.relative_bounding_box
                bbox = {
                    'xmin': int(bboxC.xmin * image_width),
                    'ymin': int(bboxC.ymin * image_height),
                    'width': int(bboxC.width * image_width),
                    'height': int(bboxC.height * image_height),
                    'score': float(detection.score[0])
                }
                
                # Calculer les coordonnées maximales pour faciliter l'utilisation
                bbox['xmax'] = bbox['xmin'] + bbox['width']
                bbox['ymax'] = bbox['ymin'] + bbox['height']
                
                # Extraire les points clés du visage (yeux, nez, bouche)
                keypoints = {}
                if detection.location_data.HasField('relative_keypoints'):
                    for idx, kp in enumerate(detection.location_data.relative_keypoints):
                        # Convertir les coordonnées relatives en coordonnées absolues
                        keypoints[idx] = {
                            'x': int(kp.x * image_width),
                            'y': int(kp.y * image_height)
                        }
                
                # Ajouter les données du visage à la liste
                faces_data.append({
                    'bbox': bbox,
                    'keypoints': keypoints,
                    'score': float(detection.score[0])
                })
        
        return image, faces_data
    
    def draw_detections(self, image: np.ndarray, faces_data: List[Dict[str, Any]]) -> np.ndarray:
        """
        Dessine les détections de visages sur l'image.
        
        Args:
            image: Image au format numpy array
            faces_data: Liste des visages détectés (retournée par detect_faces)
            
        Returns:
            Image avec les annotations dessinées
        """
        annotated_image = image.copy()
        
        for face in faces_data:
            bbox = face['bbox']
            score = face['score']
            
            # Dessiner le rectangle englobant
            cv2.rectangle(
                annotated_image,
                (bbox['xmin'], bbox['ymin']),
                (bbox['xmax'], bbox['ymax']),
                (0, 255, 0),  # Couleur verte
                2              # Épaisseur
            )
            
            # Ajouter le score
            cv2.putText(
                annotated_image,
                f"Score: {score:.2f}",
                (bbox['xmin'], bbox['ymin'] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
            
            # Dessiner les points clés
            for _, point in face['keypoints'].items():
                cv2.circle(
                    annotated_image,
                    (point['x'], point['y']),
                    2,
                    (255, 0, 0),  # Couleur bleue
                    2              # Épaisseur
                )
                
        return annotated_image

    def release(self):
        """Libère les ressources utilisées par le détecteur."""
        self.face_detection.close()