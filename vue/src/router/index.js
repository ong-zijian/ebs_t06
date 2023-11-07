// Import the functions you need from vue-router
import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';

// Define your routes
const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage
  },
  // ... other routes
];

// Create the router instance
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
