<template>
    <div class="not-found flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full text-center">
        <div class="mb-8">
          <!-- Illustration 404 stylisée -->
          <div class="relative">
            <div class="text-9xl font-bold text-gray-200 tracking-widest">404</div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-5xl font-bold text-primary-600 tracking-wide">Oops!</div>
            </div>
          </div>
        </div>
        
        <h1 class="mt-4 text-3xl font-bold text-gray-900 mb-2">Page non trouvée</h1>
        <p class="text-lg text-gray-600 mb-8">
          La page que vous recherchez semble introuvable ou a été déplacée.
        </p>
        
        <div class="space-y-4">
          <router-link to="/" class="btn btn-primary inline-flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
            Retour à l'accueil
          </router-link>
          
          <div class="flex justify-center space-x-4 pt-4 border-t border-gray-200">
            <router-link to="/help" class="text-primary-600 hover:text-primary-800 transition-colors">
              Centre d'aide
            </router-link>
            <span class="text-gray-300">|</span>
            <router-link to="/gallery" class="text-primary-600 hover:text-primary-800 transition-colors">
              Galerie vidéo
            </router-link>
            <span class="text-gray-300">|</span>
            <router-link to="/about" class="text-primary-600 hover:text-primary-800 transition-colors">
              À propos
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotFoundView'
  }
  </script>