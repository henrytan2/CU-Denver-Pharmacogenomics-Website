import './assets/main.css'
import './scss/styles.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import * as bootstrap from 'bootstrap'
import { Tooltip } from 'bootstrap'

const app = createApp(App)

// Initialize all tooltips once globally
app.mixin({
  mounted() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    tooltipTriggerList.forEach((el) => new Tooltip(el))
  }
})

app.use(createPinia())
app.use(router)

app.mount('#app')
