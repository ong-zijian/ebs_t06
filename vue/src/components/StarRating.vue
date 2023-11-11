<template>
    <div class="star-rating">
      <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= rating }">
        ★
      </span>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      rating: {
        type: Number,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  .star {
    color: gray; /* Color for unfilled star */
  }
  
  .filled {
    color: gold; /* Color for filled star */
  }
  </style>
  