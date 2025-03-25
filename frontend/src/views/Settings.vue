<template>
    <div class="settings">
      <h1 class="text-3xl font-bold font-heading mb-6 text-gray-800">Paramètres</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Panneau de navigation latéral -->
        <div class="md:col-span-1">
          <div class="card">
            <nav class="flex flex-col space-y-1">
              <button 
                v-for="(section, index) in sections" 
                :key="index"
                @click="activeSection = section.id"
                :class="[
                  'text-left px-4 py-3 rounded-lg flex items-center transition-colors', 
                  activeSection === section.id ? 'bg-primary-50 text-primary-700 font-medium' : 'text-gray-600 hover:bg-gray-50'
                ]"
              >
                <span v-if="section.id === 'general'" class="mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </span>
                <span v-else-if="section.id === 'detection'" class="mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </span>
                <span v-else-if="section.id === 'blur'" class="mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </span>
                <span v-else-if="section.id === 'storage'" class="mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                  </svg>
                </span>
                <span v-else-if="section.id === 'advanced'" class="mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                  </svg>
                </span>
                {{ section.name }}
              </button>
            </nav>
          </div>
        </div>
        
        <!-- Panneau de contenu -->
        <div class="md:col-span-2">
          <div class="card">
            <!-- Section Général -->
            <div v-if="activeSection === 'general'" class="space-y-6">
              <h2 class="text-xl font-semibold text-gray-800 mb-4">Paramètres généraux</h2>
              
              <div>
                <label class="form-label">Langue</label>
                <select class="form-select">
                  <option value="fr">Français</option>
                  <option value="en">English</option>
                  <option value="es">Español</option>
                  <option value="de">Deutsch</option>
                </select>
              </div>
              
              <div>
                <label class="form-label">Thème</label>
                <div class="flex space-x-4">
                  <button class="w-8 h-8 rounded-full bg-white border-2 border-primary-500 flex items-center justify-center">
                    <span class="w-4 h-4 rounded-full bg-primary-500"></span>
                  </button>
                  <button class="w-8 h-8 rounded-full bg-gray-900"></button>
                  <button class="w-8 h-8 rounded-full bg-indigo-600"></button>
                  <button class="w-8 h-8 rounded-full bg-green-600"></button>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Notifications</h3>
                  <p class="text-sm text-gray-500">Recevoir des notifications lors de la fin de traitement</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="settings.notifications" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Qualité vidéo par défaut</h3>
                  <p class="text-sm text-gray-500">Définir la qualité d'enregistrement des vidéos traitées</p>
                </div>
                <select class="form-select w-32">
                  <option value="low">Basse</option>
                  <option value="medium">Moyenne</option>
                  <option value="high">Haute</option>
                </select>
              </div>
            </div>
            
            <!-- Section Détection de visage -->
            <div v-if="activeSection === 'detection'" class="space-y-6">
              <h2 class="text-xl font-semibold text-gray-800 mb-4">Paramètres de détection de visage</h2>
              
              <div>
                <label class="form-label">Modèle de détection par défaut</label>
                <select class="form-select" v-model="settings.defaultDetectionModel">
                  <option value="0">Courte distance (inférieur à 2m)</option>
                  <option value="1">Longue distance (inférieur à 5m)</option>
                </select>
              </div>
              
              <div>
                <label class="form-label">Seuil de confiance par défaut: {{ settings.defaultConfidenceThreshold * 100 }}%</label>
                <input type="range" min="0" max="100" v-model="confidenceSlider" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Suivi de visage avancé</h3>
                  <p class="text-sm text-gray-500">Améliore la précision mais utilise plus de ressources</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="settings.advancedTracking" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            </div>
            
            <!-- Section Floutage -->
            <div v-if="activeSection === 'blur'" class="space-y-6">
              <h2 class="text-xl font-semibold text-gray-800 mb-4">Paramètres de floutage</h2>
              
              <div>
                <label class="form-label">Méthode de floutage par défaut</label>
                <div class="grid grid-cols-3 gap-2">
                  <button 
                    @click="settings.defaultBlurMethod = 'gaussian'"
                    :class="['py-2 border rounded-lg transition-colors', settings.defaultBlurMethod === 'gaussian' ? 'bg-primary-500 text-white' : 'bg-gray-100']"
                  >
                    Gaussien
                  </button>
                  <button 
                    @click="settings.defaultBlurMethod = 'pixelate'"
                    :class="['py-2 border rounded-lg transition-colors', settings.defaultBlurMethod === 'pixelate' ? 'bg-primary-500 text-white' : 'bg-gray-100']"
                  >
                    Pixelisé
                  </button>
                  <button 
                    @click="settings.defaultBlurMethod = 'solid'"
                    :class="['py-2 border rounded-lg transition-colors', settings.defaultBlurMethod === 'solid' ? 'bg-primary-500 text-white' : 'bg-gray-100']"
                  >
                    Solide
                  </button>
                </div>
              </div>
              
              <div>
                <label class="form-label">Intensité de floutage par défaut: {{ settings.defaultBlurIntensity }}</label>
                <input type="range" min="1" max="100" v-model="settings.defaultBlurIntensity" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Flouter tous les visages par défaut</h3>
                  <p class="text-sm text-gray-500">Si désactivé, vous devrez sélectionner les visages à flouter</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="settings.blurAllFaces" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            </div>
            
            <!-- Section Stockage -->
            <div v-if="activeSection === 'storage'" class="space-y-6">
              <h2 class="text-xl font-semibold text-gray-800 mb-4">Paramètres de stockage</h2>
              
              <div class="mb-6">
                <h3 class="font-medium text-gray-900 mb-2">Utilisation du stockage</h3>
                <div class="w-full bg-gray-200 rounded-full h-4">
                  <div class="bg-primary-600 h-4 rounded-full" style="width: 45%"></div>
                </div>
                <div class="flex justify-between text-sm text-gray-600 mt-1">
                  <span>3.6 GB utilisés</span>
                  <span>8 GB total</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Compression vidéo</h3>
                  <p class="text-sm text-gray-500">Compresser automatiquement les vidéos enregistrées</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="settings.compressVideos" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Suppression automatique</h3>
                  <p class="text-sm text-gray-500">Supprimer les vidéos après une période d'inactivité</p>
                </div>
                <select class="form-select w-48">
                  <option value="never">Jamais</option>
                  <option value="30days">Après 30 jours</option>
                  <option value="90days">Après 90 jours</option>
                  <option value="1year">Après 1 an</option>
                </select>
              </div>
              
              <div>
                <button class="btn btn-primary">Vider le cache</button>
              </div>
            </div>
            
            <!-- Section Avancé -->
            <div v-if="activeSection === 'advanced'" class="space-y-6">
              <h2 class="text-xl font-semibold text-gray-800 mb-4">Paramètres avancés</h2>
              
              <div class="alert alert-warning">
                <p>Les paramètres avancés peuvent affecter les performances de l'application. Ne modifiez ces valeurs que si vous savez ce que vous faites.</p>
              </div>
              
              <div>
                <label class="form-label">Limite de mémoire (MB)</label>
                <input type="number" v-model="settings.memoryLimit" class="form-input">
              </div>
              
              <div>
                <label class="form-label">Nombre de processus parallèles</label>
                <input type="number" v-model="settings.parallelProcesses" min="1" max="8" class="form-input">
              </div>
              
              <div>
                <label class="form-label">Chemin d'enregistrement par défaut</label>
                <div class="flex">
                  <input type="text" v-model="settings.defaultSavePath" class="form-input rounded-r-none">
                  <button class="btn btn-primary rounded-l-none">Parcourir</button>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">Mode développeur</h3>
                  <p class="text-sm text-gray-500">Activer les fonctionnalités de débogage</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="settings.developerMode" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            </div>
          </div>
          
          <!-- Boutons d'action -->
          <div class="flex justify-end space-x-4 mt-4">
            <button class="btn btn-outline">Annuler</button>
            <button class="btn btn-primary" @click="saveSettings">Enregistrer</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
//   import { useStore } from 'vuex';
  
  export default {
    name: 'SettingsView',
    
    setup() {
    //   const store = useStore();
      const activeSection = ref('general');
      
      // Liste des sections
      const sections = [
        { id: 'general', name: 'Général' },
        { id: 'detection', name: 'Détection de visage' },
        { id: 'blur', name: 'Floutage' },
        { id: 'storage', name: 'Stockage' },
        { id: 'advanced', name: 'Avancé' }
      ];
      
      // Paramètres de l'application (à stocker dans Vuex dans une vraie application)
      const settings = ref({
        // Général
        language: 'fr',
        theme: 'light',
        notifications: true,
        videoQuality: 'medium',
        
        // Détection
        defaultDetectionModel: 1,
        defaultConfidenceThreshold: 0.5,
        advancedTracking: false,
        
        // Floutage
        defaultBlurMethod: 'gaussian',
        defaultBlurIntensity: 35,
        blurAllFaces: true,
        
        // Stockage
        storageUsed: 3.6,
        storageTotal: 8,
        compressVideos: true,
        autoDeletion: 'never',
        
        // Avancé
        memoryLimit: 1024,
        parallelProcesses: 2,
        defaultSavePath: 'C:/Users/Documents/BlurFace',
        developerMode: false
      });
      
      // Pour la synchronisation du slider avec la valeur
      const confidenceSlider = computed({
        get: () => settings.value.defaultConfidenceThreshold * 100,
        set: (val) => { settings.value.defaultConfidenceThreshold = val / 100; }
      });
      
      // Charger les paramètres depuis le store
      onMounted(() => {
        // Dans une vraie application, on chargerait les paramètres depuis le store
        // settings.value = store.state.settings;
      });
      
      // Sauvegarder les paramètres
      const saveSettings = () => {
        // Dans une vraie application, on sauvegarderait les paramètres dans le store
        // store.dispatch('saveSettings', settings.value);
        
        // Afficher un message de succès
        alert('Paramètres enregistrés avec succès');
      };
      
      return {
        activeSection,
        sections,
        settings,
        confidenceSlider,
        saveSettings
      };
    }
  };
  </script>