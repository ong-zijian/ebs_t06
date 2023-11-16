<template>
  <div id="app">
    <!-- <AppHeader /> -->
    <router-view />
    <AppFooter v-if="showFooter" />
  </div>
</template>

<script>
import AppFooter from './components/MainBtm.vue';

export default {
  name: 'App',
  components: {
    AppFooter,
  },
  data() {
    return {
      test: null,
      usertype: null,
    };
  },
  computed: {
    showFooter() {
      // The footer will show only if usertype is explicitly 'student'
      return this.usertype === 'student';
    }
  },
  watch: {
    '$route'() {
      this.usertype = sessionStorage.getItem('userType');
    }
  },
  created() {
    this.usertype = sessionStorage.getItem('userType');
    console.log('User Type:', this.usertype); // Debug: Check the retrieved user type
  },
};
</script>
