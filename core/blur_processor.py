"""
Module pour le floutage de visages dans les images.
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

class BlurProcessor:
    """
    Classe pour appliquer différents types de floutage sur les visages détectés.
    """

    def __init__(self, blur_method: str = "gaussian", blur_intensity: int = 35):
        """
        Initialise le processeur de floutage.
        
        Args:
            blur_method: Méthode de floutage ('gaussian', 'pixelate', 'solid')
            blur_intensity: Intensité du floutage (plus la valeur est élevée, plus le flou est intense)
        """
        self.blur_method = blur_method
        self.blur_intensity = blur_intensity
        
        # Méthodes de floutage disponibles
        self.blur_methods = {
            "gaussian": self._apply_gaussian_blur,
            "pixelate": self._apply_pixelation,
            "solid": self._apply_solid_mask
        }
    
    def set_blur_method(self, method: str):
        """
        Change la méthode de floutage.
        
        Args:
            method: Nouvelle méthode de floutage ('gaussian', 'pixelate', 'solid')
        """
        if method in self.blur_methods:
            self.blur_method = method
        else:
            raise ValueError(f"Méthode de floutage '{method}' non supportée. Options: {list(self.blur_methods.keys())}")
    
    def set_blur_intensity(self, intensity: int):
        """
        Change l'intensité du floutage.
        
        Args:
            intensity: Nouvelle intensité du floutage
        """
        self.blur_intensity = max(1, intensity)  # Assurer une intensité minimale
    
    def blur_faces(self, image: np.ndarray, faces_data: List[Dict[str, Any]], 
                  selected_faces: Optional[List[int]] = None) -> np.ndarray:
        """
        Applique le floutage sur les visages détectés.
        
        Args:
            image: Image au format numpy array
            faces_data: Liste des visages détectés avec leurs coordonnées et scores
            selected_faces: Liste des indices des visages à flouter (None = tous)
            
        Returns:
            Image avec les visages floutés
        """
        # Créer une copie de l'image pour ne pas modifier l'original
        result_image = image.copy()
        
        # Déterminer quels visages flouter
        if selected_faces is None:
            # Flouter tous les visages
            faces_to_blur = range(len(faces_data))
        else:
            # Flouter uniquement les visages sélectionnés
            faces_to_blur = selected_faces
        
        # Appliquer le floutage aux visages sélectionnés
        for idx in faces_to_blur:
            if idx < len(faces_data):
                face = faces_data[idx]
                bbox = face['bbox']
                
                # Extraire la région du visage
                face_region = result_image[
                    bbox['ymin']:bbox['ymax'],
                    bbox['xmin']:bbox['xmax']
                ]
                
                # Appliquer le floutage approprié
                blur_method = self.blur_methods.get(self.blur_method, self._apply_gaussian_blur)
                blurred_face = blur_method(face_region)
                
                # Appliquer la région floutée à l'image résultante
                result_image[
                    bbox['ymin']:bbox['ymax'],
                    bbox['xmin']:bbox['xmax']
                ] = blurred_face
        
        return result_image
    
    def _apply_gaussian_blur(self, face_region: np.ndarray) -> np.ndarray:
        """
        Applique un flou gaussien à la région du visage.
        
        Args:
            face_region: Portion de l'image contenant le visage
            
        Returns:
            Région du visage avec flou gaussien appliqué
        """
        # Le flou gaussien utilise un noyau (kernel) de taille impaire
        # L'intensité est utilisée pour déterminer la taille du noyau
        kernel_size = self.blur_intensity * 2 + 1
        return cv2.GaussianBlur(face_region, (kernel_size, kernel_size), 0)
    
    def _apply_pixelation(self, face_region: np.ndarray) -> np.ndarray:
        """
        Applique une pixellisation à la région du visage.
        
        Args:
            face_region: Portion de l'image contenant le visage
            
        Returns:
            Région du visage pixellisée
        """
        # Calculer la taille des pixels en fonction de l'intensité
        height, width = face_region.shape[:2]
        
        # Le facteur de réduction détermine combien l'image est réduite
        # Plus l'intensité est grande, plus le facteur est grand
        factor = max(1, self.blur_intensity // 10)
        
        # Calculer la nouvelle taille
        h, w = height // factor, width // factor
        
        # Éviter les divisions par zéro
        if h < 1: h = 1
        if w < 1: w = 1
        
        # Réduire puis agrandir pour créer l'effet pixellisé
        temp = cv2.resize(face_region, (w, h), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    
    def _apply_solid_mask(self, face_region: np.ndarray) -> np.ndarray:
        """
        Applique un masque solide à la région du visage.
        
        Args:
            face_region: Portion de l'image contenant le visage
            
        Returns:
            Région du visage avec masque solide appliqué
        """
        # Créer un masque de couleur uniforme
        mask = np.zeros_like(face_region)
        
        # Couleur du masque (gris par défaut)
        color = 128  # Valeur entre 0 et 255
        mask[:] = (color, color, color)
        
        # Mélanger le masque avec la région du visage en fonction de l'intensité
        alpha = min(1.0, self.blur_intensity / 100)
        return cv2.addWeighted(face_region, 1 - alpha, mask, alpha, 0)