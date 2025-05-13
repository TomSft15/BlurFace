<template>
  <div class="app min-h-screen bg-gray-50">
    <header class="bg-primary-600 text-white p-4 shadow-md">
      <div class="container mx-auto flex justify-between items-center">
        <router-link to="/" class="flex items-center">
          <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center mr-3">
            <div class="w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center">
              <div class="w-3 h-3 bg-white rounded-full"></div>
            </div>
          </div>
          <h1 class="text-2xl font-bold font-heading">BlurFace</h1>
        </router-link>
        <nav class="flex space-x-1">
          <router-link to="/" 
            class="px-4 py-2 rounded-lg transition-colors duration-200 hover:bg-primary-500 flex items-center"
            active-class="bg-primary-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
            </svg>
            Accueil
          </router-link>
          <router-link to="/settings"
            class="px-4 py-2 rounded-lg transition-colors duration-200 hover:bg-primary-500 flex items-center"
            active-class="bg-primary-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
            </svg>
            Paramètres
          </router-link>
          <router-link to="/help"
            class="px-4 py-2 rounded-lg transition-colors duration-200 hover:bg-primary-500 flex items-center"
            active-class="bg-primary-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
            </svg>
            Aide
          </router-link>
          <router-link to="/about" 
            class="px-4 py-2 rounded-lg transition-colors duration-200 hover:bg-primary-500 flex items-center"
            active-class="bg-primary-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
            À Propos
          </router-link>
        </nav>
      </div>
    </header>

    <main class="container mx-auto p-4">
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </main>

    <footer class="bg-gray-800 text-white p-4 mt-8">
      <div class="container mx-auto">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0">
            <p class="font-bold">BlurFace - Application de floutage de visages &copy; 2025</p>
          </div>
          <div class="flex space-x-4">
            <a href="#" class="hover:text-primary-300 transition-colors duration-200">Vie privée</a>
            <a href="#" class="hover:text-primary-300 transition-colors duration-200">Conditions</a>
            <a href="#" class="hover:text-primary-300 transition-colors duration-200">Contact</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* Styles de base */
/* Utilisation du CDN Tailwind à la place des imports locaux */

body {
  margin: 0;
  font-family: 'Roboto', sans-serif;
}

/* Animations de transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Personnalisation des boutons */
.btn {
  @apply px-4 py-2 rounded-lg transition-all duration-200 font-medium focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.btn-primary {
  @apply bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500;
}

.btn-secondary {
  @apply bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-secondary-500;
}

.btn-accent {
  @apply bg-accent-500 text-white hover:bg-accent-600 focus:ring-accent-400;
}

.btn-outline {
  @apply border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:ring-primary-500;
}

/* Personnalisation des cartes */
.card {
  @apply bg-white rounded-xl shadow-card transition-shadow duration-300 hover:shadow-card-hover p-6;
}

/* Personnalisation des formulaires */
.form-input {
  @apply w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.form-select {
  @apply w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200;
}

/* Personnalisation des alertes */
.alert {
  @apply p-4 rounded-lg mb-4;
}

.alert-info {
  @apply bg-blue-100 text-blue-800 border-l-4 border-blue-500;
}

.alert-success {
  @apply bg-green-100 text-green-800 border-l-4 border-green-500;
}

.alert-warning {
  @apply bg-yellow-100 text-yellow-800 border-l-4 border-yellow-500;
}

.alert-error {
  @apply bg-red-100 text-red-800 border-l-4 border-red-500;
}
</style>