import axios from 'axios';

// Création d'une instance axios avec la configuration de base
const apiClient = axios.create({
  baseURL: 'http://localhost:5000', // Ajustez selon votre configuration
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Service pour les sessions vidéo
const sessionService = {
  /**
   * Crée une nouvelle session vidéo
   * @param {string} sourceType - Type de source ('webcam' ou 'file')
   * @param {number} deviceId - ID de la webcam (pour sourceType='webcam')
   * @param {string} filePath - Chemin du fichier (pour sourceType='file')
   * @returns {Promise} - Promesse avec l'ID de session
   */
  createSession(sourceType, deviceId = 0, filePath = '') {
    return apiClient.post('/session/create', {
      source_type: sourceType,
      device_id: deviceId,
      file_path: filePath
    });
  },

  /**
   * Ferme une session vidéo
   * @param {string} sessionId - ID de la session à fermer
   * @returns {Promise}
   */
  closeSession(sessionId) {
    return apiClient.post(`/session/${sessionId}/close`);
  },

  /**
   * Met à jour les paramètres de floutage
   * @param {string} sessionId - ID de la session
   * @param {object} settings - Paramètres de floutage
   * @returns {Promise}
   */
  updateBlurSettings(sessionId, settings) {
    return apiClient.put(`/session/${sessionId}/blur-settings`, settings);
  },

  /**
   * Met à jour les paramètres de détection
   * @param {string} sessionId - ID de la session
   * @param {object} settings - Paramètres de détection
   * @returns {Promise}
   */
  updateDetectionSettings(sessionId, settings) {
    return apiClient.put(`/session/${sessionId}/detection-settings`, settings);
  },

  /**
   * Récupère une image traitée
   * @param {string} sessionId - ID de la session
   * @param {boolean} drawDetections - Dessiner les détections
   * @param {boolean} applyBlur - Appliquer le floutage
   * @returns {Promise}
   */
  getFrame(sessionId, drawDetections = false, applyBlur = true) {
    return apiClient.get(`/session/${sessionId}/frame`, {
      params: {
        draw_detections: drawDetections,
        apply_blur: applyBlur
      }
    });
  },

  /**
   * Récupère les données de détection
   * @param {string} sessionId - ID de la session
   * @returns {Promise}
   */
  getDetections(sessionId) {
    return apiClient.get(`/session/${sessionId}/detections`);
  },

  /**
   * Récupère l'URL du flux vidéo
   * @param {string} sessionId - ID de la session
   * @param {boolean} drawDetections - Dessiner les détections
   * @param {boolean} applyBlur - Appliquer le floutage
   * @returns {string} - URL du flux vidéo
   */
  getStreamUrl(sessionId, drawDetections = false, applyBlur = true) {
    const params = new URLSearchParams({
      draw_detections: drawDetections,
      apply_blur: applyBlur,
      // Ajouter un timestamp pour éviter la mise en cache du navigateur
      t: Date.now()
    });
    return `${apiClient.defaults.baseURL}/session/${sessionId}/stream?${params.toString()}`;
  },

  // Dans sessionService
  getDownloadUrl(sessionId) {
    return `${apiClient.defaults.baseURL}/session/${sessionId}/download`;
  }
};

// Service pour les webcams
const webcamService = {
  /**
   * Récupère la liste des webcams disponibles
   * @returns {Promise}
   */
  getWebcams() {
    return apiClient.get('/webcams');
  }
};

// Service pour les vidéos
const videoService = {
  /**
   * Récupère les informations d'une vidéo
   * @param {string} filePath - Chemin du fichier vidéo
   * @returns {Promise}
   */
  getVideoInfo(filePath) {
    return apiClient.post('/videos/info', {
      file_path: filePath
    });
  },

  uploadVideo(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiClient.post('/videos/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
};

export default {
  sessionService,
  webcamService,
  videoService
};