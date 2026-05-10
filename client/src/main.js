import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

// Order matters: Pinia first, then Router.
// (Router navigation guards in Phase 4 will use stores, which need Pinia ready.)
app.use(createPinia())
app.use(router)

app.mount('#app')