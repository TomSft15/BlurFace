import { createStore } from 'vuex';
import api from '@/services/api';

export default createStore({
  state: {
    // Session vidéo
    session: {
      id: null,
      isActive: false,
      sourceType: null, // 'webcam' ou 'file'
      deviceId: 0,
      filePath: ''
    },
    // Paramètres de floutage
    blurSettings: {
      method: 'gaussian', // 'gaussian', 'pixelate', 'solid'
      intensity: 35,
      selectedFaces: null // null = tous les visages
    },
    // Paramètres de détection
    detectionSettings: {
      minConfidence: 0.5,
      modelSelection: 1
    },
    // Liste des webcams disponibles
    webcams: [],
    // Informations sur la vidéo actuelle
    videoInfo: null,
    // Données de détection des visages
    detections: {
      faces: [],
      frameId: 0,
      timestamp: 0,
      width: 0,
      height: 0
    },
    // Paramètres d'affichage
    displaySettings: {
      drawDetections: true,
      applyBlur: true
    },
    // Statut de chargement global
    loading: false,
    // Message d'erreur global
    error: null
  },
  
  getters: {
    // URL du flux vidéo
    streamUrl: (state) => {
      if (!state.session.id) return null;
      return api.sessionService.getStreamUrl(
        state.session.id,
        state.displaySettings.drawDetections,
        state.displaySettings.applyBlur
      );
    },
    
    // Vérifier si une session est active
    hasActiveSession: (state) => {
      return state.session.isActive && state.session.id !== null;
    },
    
    // Informations sur la source vidéo actuelle
    currentSource: (state) => {
      if (state.session.sourceType === 'webcam') {
        const webcam = state.webcams.find(w => w.device_id === state.session.deviceId);
        return webcam ? webcam.name : `Webcam ${state.session.deviceId}`;
      } else if (state.session.sourceType === 'file') {
        return state.videoInfo ? state.videoInfo.filename : state.session.filePath;
      }
      return 'Aucune source';
    }
  },
  
  mutations: {
    SET_SESSION(state, session) {
      state.session = { ...state.session, ...session };
    },
    
    SET_BLUR_SETTINGS(state, settings) {
      state.blurSettings = { ...state.blurSettings, ...settings };
    },
    
    SET_DETECTION_SETTINGS(state, settings) {
      state.detectionSettings = { ...state.detectionSettings, ...settings };
    },
    
    SET_WEBCAMS(state, webcams) {
      state.webcams = webcams;
    },
    
    SET_VIDEO_INFO(state, info) {
      state.videoInfo = info;
    },
    
    SET_DETECTIONS(state, detections) {
      state.detections = detections;
    },
    
    SET_DISPLAY_SETTINGS(state, settings) {
      state.displaySettings = { ...state.displaySettings, ...settings };
    },
    
    SET_LOADING(state, isLoading) {
      state.loading = isLoading;
    },
    
    SET_ERROR(state, error) {
      state.error = error;
    },
    
    RESET_SESSION(state) {
      state.session = {
        id: null,
        isActive: false,
        sourceType: null,
        deviceId: 0,
        filePath: ''
      };
      state.videoInfo = null;
      state.detections = {
        faces: [],
        frameId: 0,
        timestamp: 0,
        width: 0,
        height: 0
      };
    }
  },
  
  actions: {
    // Charger la liste des webcams
    async loadWebcams({ commit }) {
      try {
        commit('SET_LOADING', true);
        const response = await api.webcamService.getWebcams();
        commit('SET_WEBCAMS', response.data.webcams);
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors du chargement des webcams: ' + error.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    // Charger les informations d'une vidéo
    async loadVideoInfo({ commit }, filePath) {
      try {
        commit('SET_LOADING', true);
        const response = await api.videoService.getVideoInfo(filePath);
        commit('SET_VIDEO_INFO', response.data);
        return response.data;
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors du chargement des informations vidéo: ' + error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    // Créer une nouvelle session
    async createSession({ commit }, { sourceType, deviceId, filePath }) {
      try {
        commit('SET_LOADING', true);
        commit('SET_ERROR', null);
        
        // Créer la session
        const response = await api.sessionService.createSession(sourceType, deviceId, filePath);
        
        if (response.data.success) {
          // Mise à jour de l'état de la session
          commit('SET_SESSION', {
            id: response.data.session_id,
            isActive: true,
            sourceType,
            deviceId,
            filePath
          });
          
          return response.data.session_id;
        } else {
          throw new Error(response.data.error || 'Échec de la création de session');
        }
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors de la création de la session: ' + error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    // Fermer la session actuelle
    async closeSession({ commit, state }) {
      if (!state.session.id) return;
      
      try {
        commit('SET_LOADING', true);
        await api.sessionService.closeSession(state.session.id);
        commit('RESET_SESSION');
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors de la fermeture de la session: ' + error.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    // Mettre à jour les paramètres de floutage
    async updateBlurSettings({ commit, state }, settings) {
      if (!state.session.id) return;
      
      try {
        commit('SET_LOADING', true);
        // Convertir les noms de paramètres au format snake_case pour l'API
        const apiSettings = {
          method: settings.method,
          intensity: settings.intensity,
          selected_faces: settings.selectedFaces
        };
        
        await api.sessionService.updateBlurSettings(state.session.id, apiSettings);
        commit('SET_BLUR_SETTINGS', settings);
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors de la mise à jour des paramètres de floutage: ' + error.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    // Mettre à jour les paramètres de détection
    async updateDetectionSettings({ commit, state }, settings) {
      if (!state.session.id) return;
      
      try {
        commit('SET_LOADING', true);
        // Convertir les noms de paramètres au format snake_case pour l'API
        const apiSettings = {
          min_confidence: settings.minConfidence,
          model_selection: settings.modelSelection
        };
        
        await api.sessionService.updateDetectionSettings(state.session.id, apiSettings);
        commit('SET_DETECTION_SETTINGS', settings);
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors de la mise à jour des paramètres de détection: ' + error.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    // Récupérer les détections de visages
    async fetchDetections({ commit, state }) {
      if (!state.session.id) return;
      
      try {
        const response = await api.sessionService.getDetections(state.session.id);
        if (response.data.success) {
          commit('SET_DETECTIONS', response.data);
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des détections:', error);
      }
    },
    
    // Mettre à jour les paramètres d'affichage
    async updateDisplaySettings({ commit }, settings) {
      commit('SET_DISPLAY_SETTINGS', settings);
    },

    // Ajouter cette action dans la section actions du store
    async uploadVideo({ commit }, file) {
      try {
        commit('SET_LOADING', true);
        commit('SET_ERROR', null);
        
        // Appel à l'API pour télécharger le fichier
        const response = await api.videoService.uploadVideo(file);
        
        if (response.data.success) {
          // Mettre à jour les informations du fichier et de la vidéo
          commit('SET_VIDEO_INFO', response.data.video_info);
          return response.data.file_path;
        } else {
          throw new Error(response.data.error || 'Échec du téléchargement de la vidéo');
        }
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors du téléchargement: ' + error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },

    // Ajouter cette action dans la section actions du store
    async downloadVideo({ commit, state }) {
      if (!state.session.id) return;
      
      try {
        commit('SET_LOADING', true);
        
        // Créer un lien de téléchargement
        const downloadUrl = api.sessionService.getDownloadUrl(state.session.id);
        
        // Créer un lien invisible et déclencher le téléchargement
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `video_floutee_${new Date().toISOString().replace(/:/g, '-')}.mp4`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        return true;
      } catch (error) {
        commit('SET_ERROR', 'Erreur lors du téléchargement: ' + error.message);
        throw error;
      } finally {
        // Masquer l'indicateur de chargement après un court délai
        setTimeout(() => {
          commit('SET_LOADING', false);
        }, 1000);
      }
    }
  }
});