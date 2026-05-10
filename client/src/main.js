<<<<<<< HEAD
import "./assets/main.css";
import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
=======
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
>>>>>>> 48da94096a2a516f3758e317689b63040e8a024f

const app = createApp(App);

<<<<<<< HEAD
app.use(createPinia());
app.use(router);

app.mount("#app");
=======
// Order matters: Pinia first, then Router.
// (Router navigation guards in Phase 4 will use stores, which need Pinia ready.)
app.use(createPinia())
app.use(router)

app.mount('#app')
>>>>>>> 48da94096a2a516f3758e317689b63040e8a024f
