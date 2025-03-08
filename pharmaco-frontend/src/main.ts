import './assets/main.css'
import './scss/styles.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import * as bootstrap from 'bootstrap'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
