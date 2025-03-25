<template>
  <div class="about">
    <h1 class="text-3xl font-bold font-heading mb-6 text-gray-800">À propos de BlurFace</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Présentation principale -->
      <div class="lg:col-span-2">
        <div class="card mb-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Présentation</h2>
          <div class="prose prose-primary max-w-none">
            <p class="mb-4">
              <span class="text-primary-600 font-medium">BlurFace</span> est une application qui permet de flouter automatiquement les visages dans des flux vidéo en temps réel.
              Elle utilise des algorithmes de détection de visages basés sur MediaPipe pour localiser les visages
              et applique différentes méthodes de floutage pour préserver la confidentialité.
            </p>
            <p class="mb-4">
              Notre mission est de fournir un outil facile à utiliser permettant de protéger la vie privée des personnes apparaissant dans vos vidéos,
              que ce soit pour des raisons légales, éthiques ou de confidentialité.
            </p>
            <p>
              L'application peut être utilisée aussi bien avec une webcam en temps réel qu'avec des fichiers vidéo préenregistrés,
              offrant ainsi une flexibilité maximale pour vos besoins de floutage de visages.
            </p>
          </div>
        </div>
      
        <div class="card">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Fonctionnalités</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex items-start">
              <div class="flex-shrink-0 h-10 w-10 rounded-md bg-primary-100 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-900">Détection en temps réel</h3>
                <p class="text-gray-600">Détection de visages précise et rapide dans les flux vidéo en direct</p>
              </div>
            </div>
            
            <div class="flex items-start">
              <div class="flex-shrink-0 h-10 w-10 rounded-md bg-primary-100 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-900">Plusieurs méthodes de floutage</h3>
                <p class="text-gray-600">Gaussien, pixelisation et masque solide avec contrôle d'intensité</p>
              </div>
            </div>
            
            <div class="flex items-start">
              <div class="flex-shrink-0 h-10 w-10 rounded-md bg-primary-100 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-900">Sélection des visages</h3>
                <p class="text-gray-600">Possibilité de sélectionner individuellement les visages à flouter</p>
              </div>
            </div>
            
            <div class="flex items-start">
              <div class="flex-shrink-0 h-10 w-10 rounded-md bg-primary-100 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-900">Sources multiples</h3>
                <p class="text-gray-600">Compatibilité avec les webcams et les fichiers vidéo</p>
              </div>
            </div>
            
            <div class="flex items-start">
              <div class="flex-shrink-0 h-10 w-10 rounded-md bg-primary-100 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-900">Exportation facile</h3>
                <p class="text-gray-600">Possibilité d'enregistrer les vidéos traitées dans différents formats</p>
              </div>
            </div>
            
            <div class="flex items-start">
              <div class="flex-shrink-0 h-10 w-10 rounded-md bg-primary-100 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-900">Traitement local</h3>
                <p class="text-gray-600">Aucune donnée n'est envoyée sur des serveurs externes</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Sidebar d'informations -->
      <div class="lg:col-span-1">
        <div class="card mb-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Technologies utilisées</h2>
          <div class="space-y-6">
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">Backend</h3>
              <ul class="space-y-2">
                <li class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span>Python</span>
                </li>
                <li class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span>Flask (API REST)</span>
                </li>
                <li class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span>OpenCV</span>
                </li>
                <li class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span>MediaPipe</span>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">Frontend</h3>
              <ul class="space-y-2">
                <li class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span>Vue.js 3</span>
                </li>
                <li class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span>Vuex</span>
                </li>
                <li class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span>Tailwind CSS</span>
                </li>
                <li class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span>Axios</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="card">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Confidentialité</h2>
          <div class="bg-green-50 border-l-4 border-green-500 p-4 mb-4">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-green-800">Traitement 100% local</h3>
                <div class="mt-2 text-sm text-green-700">
                  <p>Toutes les vidéos sont traitées localement sur votre appareil.</p>
                </div>
              </div>
            </div>
          </div>
          
          <p class="text-gray-700 mb-4">
            BlurFace traite toutes les vidéos localement et ne transfère aucune donnée vers des serveurs externes.
            Les visages détectés et floutés ne sont pas enregistrés par défaut, sauf si vous choisissez explicitement
            d'enregistrer le résultat.
          </p>
          
          <p class="text-gray-700">
            Nous nous engageons à respecter et à protéger votre vie privée. Notre application
            est conçue dans un souci de confidentialité dès la conception.
          </p>
        </div>
      </div>
    </div>
    
    <!-- Section équipe et contact -->
    <div class="card mt-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">L'équipe</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
        <div class="flex flex-col items-center text-center">
          <div class="w-24 h-24 bg-gray-200 rounded-full mb-4 overflow-hidden">
            <img src="https://via.placeholder.com/150" alt="Photo de profil" class="w-full h-full object-cover" />
          </div>
          <h3 class="font-medium text-gray-900">Thomas Fiancette</h3>
          <p class="text-gray-600">Développeur backend</p>
        </div>
        
        <div class="flex flex-col items-center text-center">
          <div class="w-24 h-24 bg-gray-200 rounded-full mb-4 overflow-hidden">
            <img src="https://via.placeholder.com/150" alt="Photo de profil" class="w-full h-full object-cover" />
          </div>
          <h3 class="font-medium text-gray-900">Charles Fassel-Ashley</h3>
          <p class="text-gray-600">Développeur frontend</p>
        </div>
        
      </div>
      
      <div class="mt-8 pt-6 border-t border-gray-200 text-center">
        <p class="text-gray-600 mb-4">Vous avez des questions ou des suggestions ? N'hésitez pas à nous contacter !</p>
        <button class="btn btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
            <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
          </svg>
          Nous contacter
        </button>
      </div>
    </div>
    
    <!-- Pied de page avec version et licence -->
    <div class="mt-8 text-center text-gray-500 text-sm">
      <p>BlurFace v1.0.0 &copy; 2025</p>
      <p>Distribué sous licence MIT</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>