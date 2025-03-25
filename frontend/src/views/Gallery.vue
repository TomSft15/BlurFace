<template>
    <div class="gallery">
      <h1 class="text-3xl font-bold font-heading mb-6 text-gray-800">Galerie Vidéo</h1>
      
      <div class="mb-8">
        <div class="card mb-4">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-800">Vidéos traitées</h2>
            <button class="btn btn-primary flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
              Importer une vidéo
            </button>
          </div>
          
          <div v-if="videos.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Aucune vidéo traitée</h3>
            <p class="text-gray-600 mb-4">Commencez par traiter une vidéo sur la page d'accueil ou importez un fichier existant.</p>
            <router-link to="/" class="btn btn-outline">
              Aller à la page d'accueil
            </router-link>
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="(video, index) in videos" :key="index" class="overflow-hidden rounded-lg border border-gray-200 bg-white transition-all duration-300 hover:shadow-md">
              <div class="relative aspect-video bg-gray-100">
                <img :src="video.thumbnail" alt="Thumbnail" class="w-full h-full object-cover" />
                <div class="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300">
                  <button class="btn btn-primary mx-1 p-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                    </svg>
                  </button>
                  <button class="btn btn-secondary mx-1 p-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                  </button>
                  <button class="btn btn-accent mx-1 p-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
              <div class="p-4">
                <h3 class="font-medium text-gray-900 mb-1">{{ video.name }}</h3>
                <div class="flex justify-between text-sm text-gray-500">
                  <span>{{ video.duration }}</span>
                  <span>{{ video.date }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mb-8">
        <div class="card">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Historique de traitement</h2>
          
          <div v-if="processHistory.length === 0" class="bg-gray-50 rounded-lg p-6 text-center">
            <p class="text-gray-600">Aucun historique de traitement disponible.</p>
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fichier</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Paramètres</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statut</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(item, index) in processHistory" :key="index">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.filename }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.date }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-1">
                      {{ item.blurMethod }}
                    </span>
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {{ item.intensité }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span v-if="item.status === 'completed'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Complété
                    </span>
                    <span v-else-if="item.status === 'processing'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      En cours
                    </span>
                    <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      Erreur
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    name: 'GalleryView',
    
    setup() {
      // Simulation de données pour les vidéos
      const videos = ref([
        {
          name: 'Interview_20240315.mp4',
          thumbnail: 'https://via.placeholder.com/400x225',
          duration: '02:45',
          date: '15/03/2024'
        },
        {
          name: 'Conference_20240226.mp4',
          thumbnail: 'https://via.placeholder.com/400x225',
          duration: '15:30',
          date: '26/02/2024'
        },
        {
          name: 'MeetingTeam_20240110.mp4',
          thumbnail: 'https://via.placeholder.com/400x225',
          duration: '48:12',
          date: '10/01/2024'
        }
      ]);
      
      // Simulation de données pour l'historique de traitement
      const processHistory = ref([
        {
          filename: 'Interview_20240315.mp4',
          date: '15/03/2024 14:30',
          blurMethod: 'Gaussian',
          intensité: 'Moyenne',
          status: 'completed'
        },
        {
          filename: 'Conference_20240226.mp4',
          date: '26/02/2024 09:15',
          blurMethod: 'Pixelisé',
          intensité: 'Élevée',
          status: 'completed'
        },
        {
          filename: 'MeetingTeam_20240110.mp4',
          date: '10/01/2024 16:45',
          blurMethod: 'Solide',
          intensité: 'Faible',
          status: 'completed'
        }
      ]);
      
      return {
        videos,
        processHistory
      };
    }
  };
  </script>