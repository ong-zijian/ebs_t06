<template>
    <div class="profile-container">
      <div class="header">
        <button class="settings">Settings</button>
        <button class="logout">Logout</button>
      </div>
      <div class="profile-card">
        <div class="profile-image">
          <img :src="counselor.photo" :alt="`Profile picture of ${counselor.name}`">
        </div>
        <h1 class="profile-name">{{ counselor.name }}</h1>
        <p class="profile-title">{{ counselor.title }}</p>
        <button class="schedule-btn">Schedule Appointment</button>
      </div>
      <div class="review-section">
        <div v-for="review in counselor.reviews" :key="review.id" class="review">
          <div class="review-header">
            <span class="review-author">{{ review.author }}</span>
            <star-rating :rating="review.rating"></star-rating>
          </div>
          <p class="review-content">{{ review.content }}</p>
          <span class="review-timestamp">{{ review.timestamp }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CounselorProfile',
    props: {
      counselor: {
        type: Object,
        required: true
      }
    },
    // Dummy component for star-rating, replace with your own
    components: {
      'star-rating': {
        props: ['rating'],
        template: '<div class="star-rating">Stars: {{ rating }}</div>'
      }
    }
  };
  </script>
  
  <style scoped>
  .profile-container {
    font-family: 'Arial', sans-serif;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    padding: 10px 20px;
    background-color: #0077cc;
    color: white;
  }
  
  .profile-card {
    text-align: center;
    padding: 20px;
  }
  
  .profile-image img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    margin-bottom: 10px;
  }
  
  .profile-name {
    margin: 10px 0;
    font-size: 24px;
  }
  
  .profile-title {
    color: #555;
    margin-bottom: 20px;
  }
  
  .schedule-btn {
    padding: 10px 20px;
    background-color: #0077cc;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .review-section {
    background-color: #f7f7f7;
    padding: 20px;
  }
  
  .review {
    background-color: white;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 10px;
  }
  
  .review-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .review-author {
    font-weight: bold;
  }
  
  .review-content {
    color: #555;
    margin: 10px 0;
  }
  
  .review-timestamp {
    font-size: 0.8em;
    color: #999;
  }
  </style>
  