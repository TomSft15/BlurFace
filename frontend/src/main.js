import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Toast from 'vue-toastification/dist/index.mjs'
import 'vue-toastification/dist/index.css'
import './assets/tailwind.css'
import '../styles/global.css'

// Options pour vue-toastification
const toastOptions = {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
}

// Création de l'application
const app = createApp(App)

// Ajout des plugins
app.use(store)
app.use(router)
app.use(Toast, toastOptions)

// Montage de l'application
app.mount('#app')