<template>
  <div class="app min-h-screen bg-gray-100">
    <header class="bg-blue-600 text-white p-4 shadow-md">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold">BlurFace</h1>
        <div>
          <router-link to="/" class="px-4 py-2 mr-2 rounded hover:bg-blue-700">Accueil</router-link>
          <router-link to="/about" class="px-4 py-2 rounded hover:bg-blue-700">À Propos</router-link>
        </div>
      </div>
    </header>

    <main class="container mx-auto p-4">
      <router-view />
    </main>

    <footer class="bg-gray-800 text-white p-4 mt-8">
      <div class="container mx-auto text-center">
        <p>BlurFace - Application de floutage de visages &copy; 2025</p>
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

body {
  margin: 0;
  font-family: 'Roboto', sans-serif;
}
</style>