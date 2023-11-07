import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap.css'

// Create the Vue application instance
const app = createApp(App);

// Use the router instance
app.use(router);

// Mount the app
app.mount('#app');
