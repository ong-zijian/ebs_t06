<template>
  <div id="app">
    <!-- <AppHeader /> -->
    <router-view/>
    <div v-if="usertype && usertype === 'student'">
      <AppFooter/>
    </div>
    <div v-else>
    </div>
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
  created() {
    this.usertype = sessionStorage.getItem('userType');
  }

};
</script>
