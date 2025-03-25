import os
from pathlib import Path

# Chemins du projet
BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = os.path.join(BASE_DIR, "temp")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Créer les dossiers s'ils n'existent pas
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Paramètres de détection des visages
FACE_DETECTION_CONFIDENCE = 0.5
FACE_DETECTION_MODEL = "mediapipe"  # Options: 'mediapipe', 'opencv'

# Paramètres de floutage
DEFAULT_BLUR_METHOD = "gaussian"  # Options: 'gaussian', 'pixelate', 'solid'
DEFAULT_BLUR_INTENSITY = 35  # Plus la valeur est élevée, plus le floutage est intense

# Paramètres vidéo
DEFAULT_FPS = 30
DEFAULT_RESOLUTION = (640, 480)  # (width, height)