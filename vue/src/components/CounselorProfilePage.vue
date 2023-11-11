<template>
  <div class="profile-container">
    <div class="header">
      <button class="settings-btn" @click="goToSettings">Settings</button>
      <span class="header-spacer"></span>
      <button class="logout-btn" @click="logout">Logout</button>
    </div>

    <!-- Conditionally render profile card only when counselor data is available -->
    <div v-if="counselor" class="profile-card">
      <div class="avatar-container">
        <img :src="counselor?.photo" :alt="`Profile of ${counselor?.name}`" class="profile-photo" />
      </div>
      <div class="profile-info">
        <h1 class="counselor-name">{{ counselor?.name }}</h1>
        <p class="counselor-title">{{ counselor?.title }}</p>
        <p class="counselor-description">{{ counselor?.description }}</p>
        <StarRating :rating="counselor?.rating" />
        <button class="schedule-btn" @click="scheduleAppointment">Schedule Appointment</button>
      </div>
    </div>
    <div v-else-if="loading">
      Loading...
    </div>
    <div v-else>
      {{ error }}
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import StarRating from './StarRating.vue';

export default {
  name: 'CounselorProfile',
  components: {
    StarRating
  },
  data() {
    return {
      counselor: null,
      loading: true,
      error: null,
    };
  },
  props: {
    counselorId: {
      type: Number,
      required: true
    }
  },
  created() {
    this.fetchCounselorData();
  },
  methods: {
    fetchCounselorData() {
      axios.get(`http://localhost:5000/api/counselor/${this.counselorId}`)
        .then(response => {
          this.counselor = response.data;
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching counselor data:', error);
          this.error = 'Failed to load the counselor data.'; // Set the error variable here
          this.loading = false;
        });
    },
    goToSettings() {
      // Implement your logic here
    },
    logout() {
      // Implement your logic here
    }
  }
};

</script>

<style scoped>
.profile-container {
  text-align: center;
  background-color: #FFFFFF;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem;
  background-color: #007BFF;
  color: white;
  position: relative; /* Add position relative to header */
  height: 195px;
}

.avatar-container {
  width: 150px; /* Adjust the width as needed */
  height: 150px; /* Adjust the height as needed */
  position: absolute;
  top: -10%; /* Set top to the bottom of the header */
  left: 50%; /* Center horizontally */
  transform: translate(-50%, -50%); /* Center vertically */
  border-radius: 50%;
  overflow: hidden;
  border: 6px solid white; /* Adjust border size for separation */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Optional: add shadow for depth */
}

.settings-btn,
.logout-btn {
  background: none;
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.header-spacer {
  flex-grow: 1;
}

.profile-card {
  position: relative;
  padding-top: 4rem;
  /* Adjust based on your profile photo size */
  background-color: #F1F1F1;
  /* Light grey background */
  border-radius: 20px;
  /* Rounded corners for the card */
  margin: 1rem;
  padding: 1rem;
}

.profile-photo {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ensure the image covers the container without distortion */
}

.counselor-name {
  margin-top: 70px; /* Adjust this value as needed */
  font-size: 1.5rem;
  color: #333;
}

.counselor-title {
  font-size: 1rem;
  color: #555;
  margin-bottom: 1rem;
}

.schedule-btn {
  background-color: #22C55E;
  /* Green color */
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 1rem;
  /* Add some space above the button */
}

/* Additional styles for your reviews and other content */</style>