<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-success">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">EBST06</a>
        <button class="navbar-toggler" type="button" @click="toggleCollapse"
                aria-controls="navbarNav" :aria-expanded="!isCollapsed" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div :class="{ 'collapse': isCollapsed, 'navbar-collapse': true }" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" :class="{ 'active': activeRoute === '/' }" 
                           aria-current="page" to="/" @click="setActive('/')">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ 'active': activeRoute === '/about' }" 
                           to="/about" @click="setActive('/about')">About</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ 'active': activeRoute === '/services' }" 
                           to="/services" @click="setActive('/services')">Services</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ 'active': activeRoute === '/contact' }" 
                           to="/contact" @click="setActive('/contact')">Contact</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
    
  <script>
  export default {
      name: 'HeaderComponent',
      data() {
          return {
              isCollapsed: true,
              activeRoute: '/'
          }
      },
      methods: {
          toggleCollapse() {
              this.isCollapsed = !this.isCollapsed;
          },
          setActive(route) {
              this.activeRoute = route;
              this.isCollapsed = true; // Collapse the navbar when a link is clicked
          }
      }
  }
  </script>
    
  <style scoped>
  * {
      box-sizing: border-box;
  }
  </style>
  