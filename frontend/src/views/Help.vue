<template>
    <div class="help">
      <h1 class="text-3xl font-bold font-heading mb-6 text-gray-800">Centre d'aide</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Sections principales -->
        <div class="md:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="card bg-primary-50 border border-primary-100 hover:bg-primary-100 transition-colors" @click="activeSection = 'getting-started'">
            <div class="flex items-center mb-4">
              <div class="bg-primary-100 p-3 rounded-lg mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-primary-900">Premiers pas</h2>
            </div>
            <p class="text-primary-800">Tout ce dont vous avez besoin pour bien démarrer avec BlurFace</p>
          </div>
          
          <div class="card bg-secondary-50 border border-secondary-100 hover:bg-secondary-100 transition-colors" @click="activeSection = 'tutorials'">
            <div class="flex items-center mb-4">
              <div class="bg-secondary-100 p-3 rounded-lg mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-secondary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-secondary-900">Tutoriels vidéo</h2>
            </div>
            <p class="text-secondary-800">Des guides pas à pas pour utiliser toutes les fonctionnalités</p>
          </div>
          
          <div class="card bg-accent-50 border border-accent-100 hover:bg-accent-100 transition-colors" @click="activeSection = 'faq'">
            <div class="flex items-center mb-4">
              <div class="bg-accent-100 p-3 rounded-lg mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-accent-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-accent-900">FAQ</h2>
            </div>
            <p class="text-accent-800">Réponses aux questions fréquemment posées</p>
          </div>
        </div>
        
        <!-- Contenu des sections -->
        <div class="md:col-span-3">
          <!-- Premiers pas -->
          <div v-if="activeSection === 'getting-started'" class="card">
            <h2 class="text-2xl font-semibold text-gray-800 mb-6">Premiers pas avec BlurFace</h2>
            
            <div class="mb-8">
              <h3 class="text-xl font-medium text-gray-800 mb-4">Installation et configuration</h3>
              <ol class="list-decimal pl-6 space-y-3">
                <li>
                  <strong>Téléchargement et installation</strong>
                  <p class="text-gray-600 mt-1">Téléchargez la dernière version de BlurFace depuis notre site web et suivez l'assistant d'installation.</p>
                </li>
                <li>
                  <strong>Lancement de l'application</strong>
                  <p class="text-gray-600 mt-1">Une fois installée, lancez l'application en double-cliquant sur l'icône BlurFace sur votre bureau.</p>
                </li>
                <li>
                  <strong>Configuration des webcams</strong>
                  <p class="text-gray-600 mt-1">Lors du premier lancement, BlurFace détectera automatiquement les webcams connectées à votre ordinateur.</p>
                </li>
              </ol>
            </div>
            
            <div class="mb-8">
              <h3 class="text-xl font-medium text-gray-800 mb-4">Traitement d'une vidéo</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-3">
                    <div class="bg-primary-100 text-primary-700 rounded-full w-8 h-8 flex items-center justify-center mr-3 font-bold">1</div>
                    <h4 class="font-medium">Sélectionner la source</h4>
                  </div>
                  <p class="text-gray-600">Choisissez entre "Webcam" ou "Fichier vidéo" sur la page d'accueil.</p>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-3">
                    <div class="bg-primary-100 text-primary-700 rounded-full w-8 h-8 flex items-center justify-center mr-3 font-bold">2</div>
                    <h4 class="font-medium">Configurer le floutage</h4>
                  </div>
                  <p class="text-gray-600">Choisissez la méthode et l'intensité de floutage dans les paramètres.</p>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-3">
                    <div class="bg-primary-100 text-primary-700 rounded-full w-8 h-8 flex items-center justify-center mr-3 font-bold">3</div>
                    <h4 class="font-medium">Démarrer le traitement</h4>
                  </div>
                  <p class="text-gray-600">Cliquez sur "Démarrer" pour commencer le traitement de votre vidéo.</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-xl font-medium text-gray-800 mb-4">Ressources supplémentaires</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <a href="#" class="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <div>
                    <h4 class="font-medium text-gray-900">Documentation complète</h4>
                    <p class="text-sm text-gray-600">Consultez notre documentation détaillée</p>
                  </div>
                </a>
                
                <a href="#" class="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <h4 class="font-medium text-gray-900">Tutoriels vidéo</h4>
                    <p class="text-sm text-gray-600">Apprenez en regardant nos guides</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
          
          <!-- Tutoriels -->
          <div v-if="activeSection === 'tutorials'" class="card">
            <h2 class="text-2xl font-semibold text-gray-800 mb-6">Tutoriels vidéo</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-for="(tutorial, index) in tutorials" :key="index" class="overflow-hidden rounded-lg border border-gray-200 hover:shadow-lg transition-shadow duration-300">
                <div class="relative aspect-video bg-gray-100">
                  <img :src="tutorial.thumbnail" alt="Thumbnail" class="w-full h-full object-cover" />
                  <div class="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
                    <button class="bg-white bg-opacity-90 rounded-full p-3 hover:bg-opacity-100 transition-colors">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      </svg>
                    </button>
                  </div>
                </div>
                <div class="p-4">
                  <h3 class="font-semibold text-gray-900 mb-1">{{ tutorial.title }}</h3>
                  <p class="text-gray-600 text-sm mb-2">{{ tutorial.duration }} • {{ tutorial.date }}</p>
                  <p class="text-gray-700">{{ tutorial.description }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- FAQ -->
          <div v-if="activeSection === 'faq'" class="card">
            <h2 class="text-2xl font-semibold text-gray-800 mb-6">Foire aux questions</h2>
            
            <div class="space-y-4">
              <div v-for="(question, index) in faq" :key="index" class="border border-gray-200 rounded-lg overflow-hidden">
                <button 
                  @click="toggleFAQ(index)"
                  class="w-full flex justify-between items-center p-4 text-left focus:outline-none hover:bg-gray-50"
                  :class="{ 'bg-gray-50': openFAQ === index }"
                >
                  <h3 class="font-medium text-gray-900">{{ question.question }}</h3>
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    class="h-5 w-5 transition-transform" 
                    :class="{ 'transform rotate-180': openFAQ === index }"
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div v-if="openFAQ === index" class="p-4 bg-gray-50 border-t border-gray-200">
                  <p class="text-gray-700">{{ question.answer }}</p>
                </div>
              </div>
            </div>
            
            <div class="mt-8 bg-gray-50 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-900 mb-2">Vous ne trouvez pas de réponse à votre question ?</h3>
              <p class="text-gray-600 mb-4">N'hésitez pas à nous contacter pour obtenir de l'aide supplémentaire.</p>
              <button class="btn btn-primary">Contacter le support</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    name: 'HelpView',
    
    setup() {
      const activeSection = ref('getting-started');
      const openFAQ = ref(null);
      
      // Tutoriels vidéo
      const tutorials = [
        {
          title: "Premiers pas avec BlurFace",
          thumbnail: "https://via.placeholder.com/640x360",
          duration: "5:23",
          date: "12/01/2024",
          description: "Apprenez les bases de l'application et comment configurer votre première session."
        },
        {
          title: "Utilisation des différentes méthodes de floutage",
          thumbnail: "https://via.placeholder.com/640x360",
          duration: "7:45",
          date: "15/01/2024",
          description: "Découvrez les différentes méthodes de floutage et quand les utiliser."
        },
        {
          title: "Traitement par lots de vidéos",
          thumbnail: "https://via.placeholder.com/640x360",
          duration: "10:17",
          date: "22/01/2024",
          description: "Apprenez à traiter plusieurs vidéos simultanément pour gagner du temps."
        },
        {
          title: "Exportation et partage des vidéos floutées",
          thumbnail: "https://via.placeholder.com/640x360",
          duration: "4:56",
          date: "03/02/2024",
          description: "Comment exporter vos vidéos et les partager en toute sécurité."
        }
      ];
      
      // FAQ
      const faq = [
        {
          question: "Quelles webcams sont compatibles avec BlurFace ?",
          answer: "BlurFace est compatible avec la plupart des webcams USB standard, y compris les webcams intégrées aux ordinateurs portables. Si votre webcam fonctionne avec d'autres applications vidéo, elle devrait également fonctionner avec BlurFace."
        },
        {
          question: "Quels formats vidéo sont pris en charge ?",
          answer: "BlurFace prend en charge les formats vidéo courants tels que MP4, AVI, MOV et WMV. Pour obtenir les meilleurs résultats, nous recommandons d'utiliser des vidéos MP4 avec codec H.264."
        },
        {
          question: "Puis-je traiter des vidéos en 4K ?",
          answer: "Oui, BlurFace peut traiter des vidéos 4K, mais cela nécessite un ordinateur avec des ressources suffisantes. Pour des performances optimales, nous recommandons un processeur récent et au moins 8 Go de RAM pour les vidéos 4K."
        },
        {
          question: "Comment puis-je sélectionner quels visages flouter ?",
          answer: "Pendant le traitement vidéo, les visages détectés sont encadrés et numérotés. Vous pouvez cliquer sur ces cadres pour sélectionner/désélectionner les visages à flouter. Vous pouvez également utiliser les options 'Tous' ou 'Aucun' dans les paramètres de floutage."
        },
        {
          question: "Mes vidéos sont-elles envoyées sur des serveurs externes ?",
          answer: "Non, BlurFace traite toutes les vidéos localement sur votre ordinateur. Aucune donnée n'est envoyée sur des serveurs externes, garantissant ainsi la confidentialité totale de vos vidéos."
        },
        {
          question: "Comment améliorer la précision de la détection des visages ?",
          answer: "Pour améliorer la précision, assurez-vous que l'éclairage est adéquat, évitez les angles extrêmes, et ajustez le seuil de confiance dans les paramètres de détection. Vous pouvez également essayer de changer de modèle de détection selon la distance des visages."
        }
      ];
      
      // Fonction pour basculer l'affichage des réponses FAQ
      const toggleFAQ = (index) => {
        if (openFAQ.value === index) {
          openFAQ.value = null;
        } else {
          openFAQ.value = index;
        }
      };
      
      return {
        activeSection,
        tutorials,
        faq,
        openFAQ,
        toggleFAQ
      };
    }
  };
  </script>