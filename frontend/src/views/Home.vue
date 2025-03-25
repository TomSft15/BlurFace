<template>
  <div class="home">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Panneau de gauche (Configuration de la source) -->
      <div class="bg-white p-4 rounded shadow">
        <h2 class="text-xl font-bold mb-4">Source vidéo</h2>
        
        <div v-if="!hasActiveSession">
          <!-- Sélection de source -->
          <div class="mb-4">
            <label class="block mb-2">Type de source</label>
            <div class="flex">
              <button 
                @click="sourceType = 'webcam'"
                :class="['flex-1 py-2 border', sourceType === 'webcam' ? 'bg-blue-500 text-white' : 'bg-gray-100']"
              >
                Webcam
              </button>
              <button 
                @click="sourceType = 'file'"
                :class="['flex-1 py-2 border', sourceType === 'file' ? 'bg-blue-500 text-white' : 'bg-gray-100']"
              >
                Fichier Vidéo
              </button>
            </div>
          </div>
          
          <!-- Sélection de webcam -->
          <div v-if="sourceType === 'webcam'" class="mb-4">
            <label class="block mb-2">Webcam</label>
            <select v-model="deviceId" class="w-full p-2 border rounded">
              <option v-for="webcam in webcams" :key="webcam.device_id" :value="webcam.device_id">
                {{ webcam.name }} ({{ webcam.width }}x{{ webcam.height }})
              </option>
            </select>
            <button 
              @click="loadWebcams" 
              class="mt-2 bg-gray-200 text-gray-700 py-1 px-3 rounded text-sm"
            >
              Rafraîchir
            </button>
          </div>
          
          <!-- Sélection de fichier -->
          <div v-if="sourceType === 'file'" class="mb-4">
            <label class="block mb-2">Fichier vidéo</label>
            <input type="file" @change="handleFileUpload" accept="video/*" class="w-full p-2 border rounded">
            <div v-if="videoInfo" class="mt-2 text-sm">
              <p><strong>{{ videoInfo.filename }}</strong></p>
              <p>{{ videoInfo.width }}x{{ videoInfo.height }}, {{ videoInfo.fps.toFixed(1) }} FPS</p>
              <p>Durée: {{ videoInfo.duration_str }}</p>
            </div>
          </div>
          
          <!-- Bouton de démarrage -->
          <button 
            @click="startSession" 
            class="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
            :disabled="!canStartSession || loading"
          >
            <span v-if="loading">Chargement...</span>
            <span v-else>Démarrer</span>
          </button>
        </div>
        
        <div v-else>
          <!-- Informations sur la session -->
          <div class="mb-4">
            <p><strong>Source:</strong> {{ currentSource }}</p>
            <p v-if="videoInfo">
              <strong>Résolution:</strong> {{ videoInfo.width }}x{{ videoInfo.height }}
            </p>
          </div>
          
          <!-- Bouton d'arrêt -->
          <button 
            @click="stopSession" 
            class="w-full bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700"
            :disabled="loading"
          >
            <span v-if="loading">Arrêt en cours...</span>
            <span v-else>Arrêter</span>
          </button>
        </div>
      </div>
      
      <!-- Panneau central (Affichage vidéo) -->
      <div class="bg-white p-4 rounded shadow lg:col-span-2">
        <h2 class="text-xl font-bold mb-4">
          Vidéo
          <span v-if="hasActiveSession" class="ml-2 text-sm bg-green-500 text-white px-2 py-1 rounded">
            En direct
          </span>
        </h2>
        
        <div class="relative">
          <!-- Placeholder quand pas de session active -->
          <div v-if="!hasActiveSession" class="bg-gray-200 aspect-video flex items-center justify-center">
            <p class="text-gray-600">Sélectionnez une source vidéo pour commencer</p>
          </div>
          
          <!-- Flux vidéo quand session active -->
          <div v-else class="relative">
            <img :src="streamUrl" alt="Flux vidéo" class="w-full" />
            
            <!-- Overlay pour les visages détectés -->
            <div 
              v-for="(face, index) in detections.faces" 
              :key="index"
              :style="getFaceBoxStyle(face.bbox)"
              class="absolute border-2 border-blue-500 cursor-pointer"
              @click="toggleFaceSelection(index)"
            >
              <div class="absolute top-0 left-0 bg-blue-500 text-white text-xs px-1">
                {{ index }} ({{ (face.score * 100).toFixed(0) }}%)
              </div>
            </div>
          </div>
          
          <!-- Contrôles affichage -->
          <div v-if="hasActiveSession" class="mt-4 flex space-x-4">
            <label class="flex items-center cursor-pointer">
              <input type="checkbox" v-model="displaySettings.drawDetections" class="mr-2">
              Afficher détections
            </label>
            <label class="flex items-center cursor-pointer">
              <input type="checkbox" v-model="displaySettings.applyBlur" class="mr-2">
              Appliquer floutage
            </label>
          </div>
        </div>
      </div>
      
      <!-- Panneau de droite (Paramètres) -->
      <div class="bg-white p-4 rounded shadow col-span-full lg:col-span-1">
        <h2 class="text-xl font-bold mb-4">Paramètres</h2>
        
        <div :class="{ 'opacity-50 pointer-events-none': !hasActiveSession }">
          <!-- Paramètres de floutage -->
          <div class="mb-6">
            <h3 class="font-bold mb-2">Floutage</h3>
            
            <div class="mb-4">
              <label class="block mb-2">Méthode</label>
              <div class="grid grid-cols-3 gap-2">
                <button 
                  @click="updateBlurMethod('gaussian')"
                  :class="['py-2 border rounded', blurSettings.method === 'gaussian' ? 'bg-blue-500 text-white' : 'bg-gray-100']"
                >
                  Gaussien
                </button>
                <button 
                  @click="updateBlurMethod('pixelate')"
                  :class="['py-2 border rounded', blurSettings.method === 'pixelate' ? 'bg-blue-500 text-white' : 'bg-gray-100']"
                >
                  Pixelisé
                </button>
                <button 
                  @click="updateBlurMethod('solid')"
                  :class="['py-2 border rounded', blurSettings.method === 'solid' ? 'bg-blue-500 text-white' : 'bg-gray-100']"
                >
                  Solide
                </button>
              </div>
            </div>
            
            <div class="mb-4">
              <label class="block mb-2">
                Intensité: {{ blurSettings.intensity }}
              </label>
              <input 
                type="range" 
                v-model.number="blurIntensity" 
                min="1" 
                max="100" 
                class="w-full"
                @change="updateBlurIntensity"
              >
            </div>
            
            <div class="mb-4">
              <label class="block mb-2">Sélection des visages</label>
              <div class="flex">
                <button 
                  @click="selectAllFaces"
                  :class="['flex-1 py-2 border', blurSettings.selectedFaces === null ? 'bg-blue-500 text-white' : 'bg-gray-100']"
                >
                  Tous
                </button>
                <button 
                  @click="clearFaceSelection"
                  :class="['flex-1 py-2 border', blurSettings.selectedFaces?.length === 0 ? 'bg-blue-500 text-white' : 'bg-gray-100']"
                >
                  Aucun
                </button>
              </div>
              
              <div v-if="detections.faces.length > 0" class="mt-2">
                <div class="text-sm">
                  Visages sélectionnés: 
                  <span v-if="blurSettings.selectedFaces === null">Tous</span>
                  <span v-else-if="blurSettings.selectedFaces.length === 0">Aucun</span>
                  <span v-else>{{ blurSettings.selectedFaces.join(', ') }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Paramètres de détection -->
          <div>
            <h3 class="font-bold mb-2">Détection</h3>
            
            <div class="mb-4">
              <label class="block mb-2">
                Seuil de confiance: {{ (detectionSettings.minConfidence * 100).toFixed(0) }}%
              </label>
              <input 
                type="range" 
                v-model.number="confidenceThreshold" 
                min="1" 
                max="99" 
                class="w-full"
                @change="updateConfidenceThreshold"
              >
            </div>
            
            <div>
              <label class="block mb-2">Modèle</label>
              <div class="flex">
                <button 
                  @click="updateModelSelection(0)"
                  :class="['flex-1 py-2 border', detectionSettings.modelSelection === 0 ? 'bg-blue-500 text-white' : 'bg-gray-100']"
                >
                  Courte distance
                </button>
                <button 
                  @click="updateModelSelection(1)"
                  :class="['flex-1 py-2 border', detectionSettings.modelSelection === 1 ? 'bg-blue-500 text-white' : 'bg-gray-100']"
                >
                  Longue distance
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Message d'erreur global -->
    <div v-if="error" class="mt-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'HomeView',
  
  setup() {
    const store = useStore();
    
    // Source vidéo
    const sourceType = ref('webcam');
    const deviceId = ref(0);
    const filePath = ref('');
    const videoFile = ref(null);
    
    // Paramètres temporaires (pour ne pas déclencher trop de requêtes)
    const blurIntensity = ref(store.state.blurSettings.intensity);
    const confidenceThreshold = ref(store.state.detectionSettings.minConfidence * 100);
    
    // Chargement initial des webcams
    onMounted(() => {
      loadWebcams();
    });
    
    // Récupération des détections de visages toutes les 500ms
    let detectionsInterval = null;
    
    watch(() => store.getters.hasActiveSession, (isActive) => {
      if (isActive) {
        // Démarrer la récupération périodique des détections
        detectionsInterval = setInterval(() => {
          store.dispatch('fetchDetections');
        }, 500);
      } else {
        // Arrêter la récupération des détections
        if (detectionsInterval) {
          clearInterval(detectionsInterval);
          detectionsInterval = null;
        }
      }
    });
    
    // Charger la liste des webcams disponibles
    const loadWebcams = async () => {
      await store.dispatch('loadWebcams');
      // Sélectionner la première webcam si aucune n'est sélectionnée
      if (store.state.webcams.length > 0 && deviceId.value === 0) {
        deviceId.value = store.state.webcams[0].device_id;
      }
    };
    
    // Gestionnaire de sélection de fichier vidéo
    const handleFileUpload = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      
      videoFile.value = file;
      
      // Utilisez un chemin temporaire pour le test
      // Dans une vraie application, vous devriez télécharger le fichier au serveur
      filePath.value = `/temp/${file.name}`;
      
      try {
        // Simuler le chargement des infos vidéo
        // Dans une vraie application, vous appelleriez l'API
        store.commit('SET_VIDEO_INFO', {
          filename: file.name,
          width: 1280,
          height: 720,
          fps: 30,
          duration: 60,
          duration_str: '00:01:00',
          format: file.name.split('.').pop().toUpperCase()
        });
      } catch (error) {
        console.error('Erreur lors du chargement des informations vidéo:', error);
      }
    };
    
    // Démarrer une session vidéo
    const startSession = async () => {
      try {
        await store.dispatch('createSession', {
          sourceType: sourceType.value,
          deviceId: deviceId.value,
          filePath: filePath.value
        });
      } catch (error) {
        console.error('Erreur lors du démarrage de la session:', error);
      }
    };
    
    // Arrêter la session vidéo
    const stopSession = async () => {
      await store.dispatch('closeSession');
    };
    
    // Mise à jour des paramètres de floutage
    const updateBlurMethod = (method) => {
      store.dispatch('updateBlurSettings', { ...store.state.blurSettings, method });
    };
    
    const updateBlurIntensity = () => {
      store.dispatch('updateBlurSettings', { ...store.state.blurSettings, intensity: blurIntensity.value });
    };
    
    // Mise à jour des paramètres de détection
    const updateConfidenceThreshold = () => {
      store.dispatch('updateDetectionSettings', {
        ...store.state.detectionSettings,
        minConfidence: confidenceThreshold.value / 100
      });
    };
    
    const updateModelSelection = (model) => {
      store.dispatch('updateDetectionSettings', {
        ...store.state.detectionSettings,
        modelSelection: model
      });
    };
    
    // Gestion de la sélection des visages
    const toggleFaceSelection = (faceIndex) => {
      let selectedFaces = store.state.blurSettings.selectedFaces;
      
      // Si tous les visages sont sélectionnés, passer à une sélection spécifique
      if (selectedFaces === null) {
        // Sélectionner tous les visages sauf celui cliqué
        selectedFaces = store.state.detections.faces
          .map((_, index) => index)
          .filter(index => index !== faceIndex);
      } else {
        // Basculer la sélection du visage cliqué
        if (selectedFaces.includes(faceIndex)) {
          selectedFaces = selectedFaces.filter(index => index !== faceIndex);
        } else {
          selectedFaces = [...selectedFaces, faceIndex];
        }
      }
      
      store.dispatch('updateBlurSettings', {
        ...store.state.blurSettings,
        selectedFaces
      });
    };
    
    const selectAllFaces = () => {
      store.dispatch('updateBlurSettings', {
        ...store.state.blurSettings,
        selectedFaces: null
      });
    };
    
    const clearFaceSelection = () => {
      store.dispatch('updateBlurSettings', {
        ...store.state.blurSettings,
        selectedFaces: []
      });
    };
    
    // Style pour les rectangles de détection des visages
    const getFaceBoxStyle = (bbox) => {
      return {
        left: `${bbox.xmin}px`,
        top: `${bbox.ymin}px`,
        width: `${bbox.width}px`,
        height: `${bbox.height}px`
      };
    };
    
    // Mise à jour des paramètres d'affichage
    watch(() => store.state.displaySettings, () => {
      // Cette fonction est appelée chaque fois que displaySettings change
    }, { deep: true });
    
    // Vérification si une session peut être démarrée
    const canStartSession = computed(() => {
      if (sourceType.value === 'webcam') {
        return deviceId.value !== null && deviceId.value >= 0;
      } else if (sourceType.value === 'file') {
        return videoFile.value !== null;
      }
      return false;
    });
    
    // Écouter les changements des paramètres d'affichage
    watch(() => store.state.displaySettings, (newSettings) => {
      store.dispatch('updateDisplaySettings', newSettings);
    }, { deep: true });
    
    return {
      // État de la source
      sourceType,
      deviceId,
      filePath,
      videoFile,
      
      // Paramètres temporaires
      blurIntensity,
      confidenceThreshold,
      
      // Méthodes
      loadWebcams,
      handleFileUpload,
      startSession,
      stopSession,
      updateBlurMethod,
      updateBlurIntensity,
      updateConfidenceThreshold,
      updateModelSelection,
      toggleFaceSelection,
      selectAllFaces,
      clearFaceSelection,
      getFaceBoxStyle,
      
      // Accès à l'état
      webcams: computed(() => store.state.webcams),
      videoInfo: computed(() => store.state.videoInfo),
      hasActiveSession: computed(() => store.getters.hasActiveSession),
      streamUrl: computed(() => store.getters.streamUrl),
      currentSource: computed(() => store.getters.currentSource),
      blurSettings: computed(() => store.state.blurSettings),
      detectionSettings: computed(() => store.state.detectionSettings),
      detections: computed(() => store.state.detections),
      displaySettings: computed({
        get: () => store.state.displaySettings,
        set: (value) => store.dispatch('updateDisplaySettings', value)
      }),
      loading: computed(() => store.state.loading),
      error: computed(() => store.state.error),
      canStartSession
    };
  }
};
</script>