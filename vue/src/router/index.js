// Import the functions you need from vue-router
import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import CreateJournal from '../components/CreateJournal.vue';
import chatBot from '../components/chatBot.vue';
import CounselorPage from '../components/CounselorPage.vue';
import CounselorProfilePage from '../components/CounselorProfilePage.vue';
import RatingPage from '../components/RatingPage.vue';
import ProfilePage from '../components/ProfilePage.vue';

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
  },
  {
    path: '/CounselorPage',
    name: 'CounselorPage',
    component: CounselorPage
  },
  {
    path: '/counselor/:counselorId',
    name: 'CounselorProfile',
    component: CounselorProfilePage,
    props: true
  },  
  {
    path: '/RatingPage',
    name: 'RatingPage',
    component: RatingPage
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage
  }
];

// Create the router instance
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
