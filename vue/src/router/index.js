// Import the functions you need from vue-router
import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import CreateJournal from '../components/CreateJournal.vue';
import chatBot from '../components/chatBot.vue';

// Define your routes
const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage
  },
  {
    path: '/CreateJournal',
    name: 'CreateJournal',
    component: CreateJournal
  },
  {
    path: '/chatBot',
    name: 'chatBot',
    component: chatBot
  }
  // ... other routes
];

// Create the router instance
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
