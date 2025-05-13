import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import AboutView from '../views/About.vue'
import SettingsView from '../views/Settings.vue'
import HelpView from '../views/Help.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Accueil - BlurFace' }
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
    meta: { title: 'Paramètres - BlurFace' }
  },
  {
    path: '/help',
    name: 'help',
    component: HelpView,
    meta: { title: 'Aide - BlurFace' }
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: { title: 'À propos - BlurFace' }
  },
  // Route 404
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFound.vue'),
    meta: { title: 'Page non trouvée - BlurFace' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Mise à jour du titre de la page
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'BlurFace - Application de floutage de visages'
  next()
})

export default router