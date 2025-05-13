<template>
  <div class="home">
    <h1 class="text-3xl font-bold font-heading mb-6 text-gray-800">Traitement vidéo</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panneau de gauche (Configuration de la source) -->
      <div class="card source-panel">
        <h2 class="text-xl font-bold mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
          Source vidéo
        </h2>
        
        <div v-if="!hasActiveSession">
          <!-- Sélection de source -->
          <div class="mb-4">
            <label class="form-label">Type de source</label>
            <div class="flex">
              <button 
                @click="sourceType = 'webcam'"
                :class="['source-button', sourceType === 'webcam' ? 'active' : 'inactive']"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Webcam
              </button>
              <button 
                @click="sourceType = 'file'"
                :class="['source-button', sourceType === 'file' ? 'active' : 'inactive']"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                </svg>
                Fichier Vidéo
              </button>
            </div>
          </div>
          
          <!-- Sélection de webcam -->
          <div v-if="sourceType === 'webcam'" class="form-group">
            <label class="form-label">Webcam</label>
            <select v-model="deviceId" class="form-select">
              <option v-if="webcams.length === 0" value="" disabled>Aucune webcam détectée</option>
              <option v-for="webcam in webcams" :key="webcam.device_id" :value="webcam.device_id">
                {{ webcam.name }} ({{ webcam.width }}x{{ webcam.height }})
              </option>
            </select>
            <div class="mt-2 flex justify-between">
              <button 
                @click="loadWebcams" 
                class="btn btn-sm btn-outline flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Rafraîchir
              </button>
              <div class="text-xs text-gray-500 mt-1" v-if="webcams.length > 0">
                {{ webcams.length }} webcam{{ webcams.length > 1 ? 's' : '' }} disponible{{ webcams.length > 1 ? 's' : '' }}
              </div>
            </div>
          </div>
          
          <!-- Sélection de fichier -->
          <div v-if="sourceType === 'file'" class="form-group">
            <label class="form-label">Fichier vidéo</label>
            <div class="flex">
              <label class="w-full cursor-pointer bg-gray-50 border border-gray-300 rounded-lg p-2 flex items-center justify-center hover:bg-gray-100 transition-colors">
                <input type="file" @change="handleFileUpload" accept="video/*" class="hidden">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span>{{ videoFile ? 'Changer de fichier' : 'Sélectionner un fichier' }}</span>
              </label>
            </div>
            
            <div v-if="videoInfo" class="mt-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
              <div class="flex items-center mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                </svg>
                <h3 class="font-medium text-gray-900">{{ videoInfo.filename }}</h3>
              </div>
              <div class="grid grid-cols-2 gap-1 text-sm text-gray-600">
                <div class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {{ videoInfo.width }}x{{ videoInfo.height }}
                </div>
                <div class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ videoInfo.fps.toFixed(1) }} FPS
                </div>
                <div class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ videoInfo.duration_str }}
                </div>
                <div class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  {{ videoInfo.format }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- Bouton de démarrage -->
          <button 
            @click="startSession" 
            class="btn btn-primary w-full mt-4 flex items-center justify-center"
            :disabled="!canStartSession || loading"
          >
            <template v-if="loading">
              <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Chargement...
            </template>
            <template v-else>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Démarrer
            </template>
          </button>
        </div>
        
        <div v-else>
          <!-- Informations sur la session -->
          <div class="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div class="flex items-center mb-3">
              <div class="p-2 rounded-full bg-primary-100 mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
              <div>
                <div class="font-medium text-gray-900">Session active</div>
                <div class="text-sm text-gray-600">
                  ID: {{ session.id ? session.id.substring(0, 8) + '...' : 'N/A' }}
                </div>
              </div>
            </div>
            
            <div class="space-y-2">
              <div class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span><strong>Source:</strong> {{ currentSource }}</span>
              </div>
              <div v-if="videoInfo" class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <span><strong>Résolution:</strong> {{ videoInfo.width }}x{{ videoInfo.height }}</span>
              </div>
              <div class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z" />
                </svg>
                <span>
                  <strong>Méthode de floutage:</strong> 
                  {{ blurSettings.method === 'gaussian' ? 'Gaussien' : 
                     blurSettings.method === 'pixelate' ? 'Pixelisé' : 'Solide' }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- Statistiques de détection -->
          <div class="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <h3 class="text-sm font-medium text-gray-700 mb-2">Statistiques</h3>
            <div class="grid grid-cols-2 gap-2">
              <div class="bg-white p-2 rounded border border-gray-200">
                <div class="text-xs text-gray-500">Visages détectés</div>
                <div class="text-xl font-medium text-primary-600">{{ detections.faces.length }}</div>
              </div>
              <div class="bg-white p-2 rounded border border-gray-200">
                <div class="text-xs text-gray-500">Visages floutés</div>
                <div class="text-xl font-medium text-primary-600">
                  {{ blurSettings.selectedFaces === null ? detections.faces.length : 
                     blurSettings.selectedFaces.length }}
                </div>
              </div>
              <div class="bg-white p-2 rounded border border-gray-200">
                <div class="text-xs text-gray-500">Images traitées</div>
                <div class="text-xl font-medium text-primary-600">{{ detections.frameId }}</div>
              </div>
              <div class="bg-white p-2 rounded border border-gray-200">
                <div class="text-xs text-gray-500">Confiance moyenne</div>
                <div class="text-xl font-medium text-primary-600">
                  {{ detections.faces.length 
                     ? (detections.faces.reduce((sum, face) => sum + face.score, 0) / detections.faces.length * 100).toFixed(0) 
                     : 0 }}%
                </div>
              </div>
            </div>
          </div>
          
          <!-- Bouton d'arrêt -->
          <button 
            @click="stopSession" 
            class="btn btn-danger w-full flex items-center justify-center"
            :disabled="loading"
          >
            <template v-if="loading">
              <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Arrêt en cours...
            </template>
            <template v-else>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Arrêter
            </template>
          </button>
        </div>
      </div>
      
      <!-- Panneau central (Affichage vidéo) -->
      <div class="card lg:col-span-2">
        <div class="card-header">
          <h2 class="text-xl font-bold flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            Vidéo
          </h2>
          
          <div v-if="hasActiveSession" class="live-indicator">
            <div class="live-indicator-dot"></div>
            En direct
          </div>
        </div>
        
        <div class="video-container">
          <!-- Placeholder quand pas de session active -->
          <div v-if="!hasActiveSession" class="video-placeholder">
            <div class="text-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <p class="text-gray-600 mb-4">Sélectionnez une source vidéo et cliquez sur "Démarrer" pour commencer</p>
              <p class="text-sm text-gray-500">Vous pourrez voir le flux vidéo ici et ajuster les paramètres de floutage</p>
            </div>
          </div>
          
          <!-- Flux vidéo quand session active -->
          <div v-else class="relative">
            <img :src="streamUrl" alt="Flux vidéo" class="video-frame" />
            
            <!-- Overlay pour les visages détectés -->
            <div 
              v-for="(face, index) in detections.faces" 
              :key="`face-${index}-${faceBoxesKey}`"
              :style="getFaceBoxStyle(face.bbox)"
              :class="['face-box', isSelectedFace(index) ? 'border-primary-500' : 'border-blue-500']"
              @click="toggleFaceSelection(index)"
            >
              <div :class="['face-box-label', isSelectedFace(index) ? 'bg-primary-500' : 'bg-blue-500']">
                {{ index }} ({{ (face.score * 100).toFixed(0) }}%)
              </div>
            </div>
          </div>
        </div>
        
        <!-- Contrôles affichage -->
        <div v-if="hasActiveSession" class="control-panel">
          <div class="flex flex-wrap items-center gap-4">
            <label class="flex items-center cursor-pointer">
              <input type="checkbox" 
                    :checked="drawDetections" 
                    @change="toggleDrawDetections" 
                    class="form-checkbox h-4 w-4 text-primary-600 rounded focus:ring-primary-500 mr-2">
              <span>Afficher détections</span>
            </label>
            <label class="flex items-center cursor-pointer">
              <input type="checkbox" 
                    :checked="applyBlur" 
                    @change="toggleApplyBlur" 
                    class="form-checkbox h-4 w-4 text-primary-600 rounded focus:ring-primary-500 mr-2">
              <span>Appliquer floutage</span>
            </label>
            
            <div class="ml-auto flex space-x-2">
              <button 
                class="btn btn-sm btn-primary flex items-center" 
                @click="downloadVideo" 
                :disabled="loading"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Télécharger
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Panneau de droite (Paramètres) -->
      <div class="card settings-panel col-span-full lg:col-span-1">
        <div class="card-header">
          <h2 class="text-xl font-bold flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Paramètres
          </h2>
        </div>
        
        <div :class="{ 'opacity-50 pointer-events-none': !hasActiveSession }">
          <!-- Paramètres de floutage -->
          <div class="settings-section">
            <h3 class="font-bold mb-2 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z" />
              </svg>
              Floutage
            </h3>
            
            <div class="mb-4">
              <label class="form-label">Méthode</label>
              <div class="grid grid-cols-3 gap-2">
                <button 
                  @click="updateBlurMethod('gaussian')"
                  :class="['option-button', blurSettings.method === 'gaussian' ? 'active' : 'inactive']"
                >
                  Gaussien
                </button>
                <button 
                  @click="updateBlurMethod('pixelate')"
                  :class="['option-button', blurSettings.method === 'pixelate' ? 'active' : 'inactive']"
                >
                  Pixelisé
                </button>
                <button 
                  @click="updateBlurMethod('solid')"
                  :class="['option-button', blurSettings.method === 'solid' ? 'active' : 'inactive']"
                >
                  Solide
                </button>
              </div>
            </div>
            
            <div class="slider-container">
              <div class="slider-label">
                <span class="slider-label-text">Intensité</span>
                <span class="slider-value">{{ blurSettings.intensity }}</span>
              </div>
              <input 
                type="range" 
                v-model.number="blurIntensity" 
                min="1" 
                max="100" 
                class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                @change="updateBlurIntensity"
              >
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>Faible</span>
                <span>Fort</span>
              </div>
            </div>
          </div>
          
          <!-- Paramètres de détection -->
          <div class="settings-section">
            <h3 class="font-bold mb-2 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Détection
            </h3>
            
            <div class="slider-container">
              <div class="slider-label">
                <span class="slider-label-text">Seuil de confiance</span>
                <span class="slider-value">{{ (detectionSettings.minConfidence * 100).toFixed(0) }}%</span>
              </div>
              <input 
                type="range" 
                v-model.number="confidenceThreshold" 
                min="1" 
                max="99" 
                class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                @change="updateConfidenceThreshold"
              >
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>Plus de détections</span>
                <span>Plus précis</span>
              </div>
            </div>
            
            <div>
              <label class="form-label">Modèle</label>
              <div class="flex">
                <button 
                  @click="updateModelSelection(0)"
                  :class="['source-button', detectionSettings.modelSelection === 0 ? 'active' : 'inactive']"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Courte distance
                </button>
                <button 
                  @click="updateModelSelection(1)"
                  :class="['source-button', detectionSettings.modelSelection === 1 ? 'active' : 'inactive']"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                  </svg>
                  Longue distance
                </button>
              </div>
              <div class="mt-1 text-xs text-gray-500">
                <span v-if="detectionSettings.modelSelection === 0">Optimisé pour les visages proches (&lt;2m)</span>
                <span v-else>Optimisé pour les visages éloignés (&lt;5m)</span>
              </div>
            </div>
          </div>
          
          <!-- Conseils d'utilisation -->
          <div class="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-blue-800">Conseils</h3>
                <div class="mt-2 text-sm text-blue-700">
                  <ul class="list-disc space-y-1 pl-5">
                    <li>Ajustez le seuil de confiance pour améliorer les détections</li>
                    <li>Utilisez le floutage gaussien pour un effet naturel</li>
                    <li>Pour un anonymat complet, utilisez l'option "Solide"</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
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
      window.addEventListener('resize', handleResize);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize);
    });

    const handleResize = () => {
      faceBoxesKey.value += 1;
    };

    const faceBoxesKey = ref(0);
    
    // Récupération des détections de visages toutes les 500ms
    let detectionsInterval = null;
    
    // Fonction pour redémarrer le flux vidéo
    const restartVideoStream = async () => {
      if (store.getters.hasActiveSession) {
        // Stocker l'ID de session actuel
        const currentSettings = {
          sourceType: store.state.session.sourceType,
          deviceId: store.state.session.deviceId,
          filePath: store.state.session.filePath,
          blurSettings: {...store.state.blurSettings},
          detectionSettings: {...store.state.detectionSettings}
        };
        
        try {
          // Fermer la session actuelle
          await store.dispatch('closeSession');
          
          // Attendre un court instant pour que le backend puisse terminer proprement
          await new Promise(resolve => setTimeout(resolve, 500));
          
          // Recréer une nouvelle session avec les mêmes paramètres
          await store.dispatch('createSession', {
            sourceType: currentSettings.sourceType,
            deviceId: currentSettings.deviceId,
            filePath: currentSettings.filePath
          });
          
          // Restaurer les paramètres de floutage et de détection
          await store.dispatch('updateBlurSettings', currentSettings.blurSettings);
          await store.dispatch('updateDetectionSettings', currentSettings.detectionSettings);
          
          console.log("Flux vidéo redémarré avec succès");
        } catch (error) {
          console.error('Erreur lors du redémarrage du flux vidéo:', error);
        }
      }
    };

    // Mise à jour de toggleDrawDetections
    const toggleDrawDetections = async () => {
      try {
        // Inverser la valeur actuelle
        const newValue = !store.state.displaySettings.drawDetections;
        
        // Mettre à jour le paramètre
        await store.dispatch('updateDisplaySettings', {
          ...store.state.displaySettings,
          drawDetections: newValue
        });
        
        // Redémarrer le flux vidéo pour éviter les problèmes
        await restartVideoStream();
      } catch (error) {
        console.error('Erreur lors du changement de paramètre:', error);
      }
    };

    // Mise à jour de toggleApplyBlur
    const toggleApplyBlur = async () => {
      try {
        const newValue = !store.state.displaySettings.applyBlur;
        await store.dispatch('updateDisplaySettings', {
          ...store.state.displaySettings,
          applyBlur: newValue
        });
        
        // Redémarrer le flux vidéo pour éviter les problèmes
        await restartVideoStream();
      } catch (error) {
        console.error('Erreur lors du changement de paramètre:', error);
      }
    };

    const downloadVideo = async () => {
      try {
        await store.dispatch('downloadVideo');
      } catch (error) {
        console.error('Erreur lors du téléchargement de la vidéo:', error);
      }
    };

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
      
      try {
        // Utiliser l'action du store pour télécharger le fichier
        const uploadedFilePath = await store.dispatch('uploadVideo', file);
        
        // Mettre à jour le chemin du fichier
        filePath.value = uploadedFilePath;
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
    
    // Vérifier si un visage est sélectionné pour le floutage
    const isSelectedFace = (faceIndex) => {
      const selectedFaces = store.state.blurSettings.selectedFaces;
      // Si tous les visages sont sélectionnés (null) ou si ce visage est dans la liste
      return selectedFaces === null || 
             (selectedFaces && selectedFaces.includes(faceIndex));
    };
    
    // Style pour les rectangles de détection des visages
    const getFaceBoxStyle = (bbox) => {
      // Récupérer les dimensions actuelles de l'image affichée
      const videoElement = document.querySelector('.video-frame');
      
      if (!videoElement || !bbox) return {};
      
      // Obtenir les dimensions réelles de l'élément dans le DOM
      const displayedWidth = videoElement.offsetWidth;
      const displayedHeight = videoElement.offsetHeight;
      
      // Calculer les ratios d'échelle
      const widthRatio = displayedWidth / store.state.detections.width;
      const heightRatio = displayedHeight / store.state.detections.height;
      
      // Appliquer les ratios aux coordonnées
      return {
        left: `${bbox.xmin * widthRatio}px`,
        top: `${bbox.ymin * heightRatio}px`,
        width: `${bbox.width * widthRatio}px`,
        height: `${bbox.height * heightRatio}px`
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
      isSelectedFace,
      downloadVideo,
      handleResize,
      toggleDrawDetections,
      toggleApplyBlur,
      
      // Accès à l'état
      session: computed(() => store.state.session),
      webcams: computed(() => store.state.webcams),
      videoInfo: computed(() => store.state.videoInfo),
      hasActiveSession: computed(() => store.getters.hasActiveSession),
      streamUrl: computed(() => store.getters.streamUrl),
      currentSource: computed(() => store.getters.currentSource),
      blurSettings: computed(() => store.state.blurSettings),
      detectionSettings: computed(() => store.state.detectionSettings),
      detections: computed(() => store.state.detections),
      displaySettings: computed(() => store.state.displaySettings),
      loading: computed(() => store.state.loading),
      error: computed(() => store.state.error),
      drawDetections: computed(() => store.state.displaySettings.drawDetections),
      applyBlur: computed(() => store.state.displaySettings.applyBlur),
      canStartSession
    };
  }
};
</script>

<style>
/* Styles spécifiques à cette vue */
.source-panel {
  @apply transition-all duration-300 hover:shadow-lg;
}

.source-button {
  @apply flex-1 py-2 border transition-colors duration-200 flex items-center justify-center;
}

.source-button.active {
  @apply bg-primary-600 text-white border-primary-600;
}

.source-button.inactive {
  @apply bg-gray-100 hover:bg-gray-200 text-gray-800;
}

/* Styles pour l'écran vidéo */
.video-container {
  @apply relative overflow-hidden rounded-lg border-2 border-gray-200 bg-gray-100;
  position: relative;
}

.video-placeholder {
  @apply aspect-video flex items-center justify-center p-8 text-center;
}

.video-frame {
  @apply w-full aspect-video object-cover;
  display: block;
}

.face-box {
  @apply absolute border-2 cursor-pointer transition-all duration-200;
  z-index: 10;
}

.face-box:hover {
  @apply border-accent-500 shadow-md;
}

.face-box-label {
  @apply absolute top-0 left-0 text-white text-xs px-1 py-0.5 rounded-br;
}

/* Animation pour le streaming */
@keyframes pulse-recording {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.live-indicator {
  @apply ml-2 text-sm bg-green-500 text-white px-2 py-1 rounded inline-flex items-center;
  animation: pulse-recording 2s ease-in-out infinite;
}

.live-indicator-dot {
  @apply w-2 h-2 bg-white rounded-full mr-1;
}
</style>