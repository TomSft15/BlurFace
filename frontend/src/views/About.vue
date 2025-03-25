<template>
  <div class="about">
    <div class="bg-white p-6 rounded shadow">
      <h1 class="text-2xl font-bold mb-4">À propos de BlurFace</h1>
      
      <div class="mb-6">
        <h2 class="text-xl font-semibold mb-2">Présentation</h2>
        <p class="mb-2">
          BlurFace est une application qui permet de flouter automatiquement les visages dans des flux vidéo en temps réel.
          Elle utilise des algorithmes de détection de visages basés sur MediaPipe pour localiser les visages
          et applique différentes méthodes de floutage pour préserver la confidentialité.
        </p>
        <p>
          L'application peut être utilisée avec une webcam ou avec des fichiers vidéo préenregistrés.
        </p>
      </div>
      
      <div class="mb-6">
        <h2 class="text-xl font-semibold mb-2">Fonctionnalités</h2>
        <ul class="list-disc list-inside space-y-1">
          <li>Détection de visages en temps réel</li>
          <li>Trois méthodes de floutage : gaussien, pixelisation, masque solide</li>
          <li>Contrôle de l'intensité du floutage</li>
          <li>Sélection des visages à flouter</li>
          <li>Compatibilité avec les webcams et les fichiers vidéo</li>
          <li>Interface utilisateur intuitive</li>
        </ul>
      </div>
      
      <div class="mb-6">
        <h2 class="text-xl font-semibold mb-2">Technologies utilisées</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 class="font-semibold">Backend</h3>
            <ul class="list-disc list-inside">
              <li>Python</li>
              <li>Flask (API REST)</li>
              <li>OpenCV</li>
              <li>MediaPipe</li>
            </ul>
          </div>
          <div>
            <h3 class="font-semibold">Frontend</h3>
            <ul class="list-disc list-inside">
              <li>Vue.js 3</li>
              <li>Vuex</li>
              <li>Tailwind CSS</li>
              <li>Axios</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div>
        <h2 class="text-xl font-semibold mb-2">Confidentialité</h2>
        <p>
          BlurFace traite toutes les vidéos localement et ne transfère aucune donnée vers des serveurs externes.
          Les visages détectés et floutés ne sont pas enregistrés par défaut, sauf si vous choisissez explicitement
          d'enregistrer le résultat.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>