<template>
  <header>
      <button @click="goBack">Back</button>
      <h1>Profile</h1>
  </header>
  <div class="profile-container mt-2 mb-4" v-if="!loading && student">
    <div class="card shadow m-2 p-2">
      <div class="d-flex justify-content-center align-items-center">
        <div class="d-flex justify-content-center align-items-center rounded-circle bg-primary text-white m-2" style="width: 5rem; height: 5rem; font-size: 3rem;">
          {{ student.fname.charAt(0) }}
        </div>
      </div>
      <h2>{{ student.fname }} {{ student.lname }}</h2>
      <form class="form">
        <div class="form-group row mt-3">
          <label for="name" class="col-form-label"><strong>Email:</strong></label>
          <div>
              <input type="text" id="name" class="form-control" :value="student.email" readonly>
          </div>
          <label for="name" class="col-form-label"><strong>Location:</strong></label>
          <div>
              <input type="text" id="name" class="form-control" :value="student.location" readonly>
          </div>
        </div>
      </form>
    </div>
    <div>
      <h2>Appointments</h2>
    </div>
    <div v-if="appointments">
      <div v-for="appointment in appointments" :key="appointment._id" class="card shadow m-2 p-2 text-left">
        <a><strong>Start Time: </strong>{{ appointment.sDateTime}}</a>
        <a><strong>End Time: </strong>{{ appointment.eDateTime}}</a>
        <p><strong>Link: </strong><a :href="appointment.video" target="_blank">{{ appointment.video }}</a></p>
      </div>
    </div>
  </div>
  <div v-if="loading">
    Loading...
  </div>

  <div v-if="error">
    {{ error }}
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'CounselorProfile',
  data() {
    return {
      studentId: "6544938b2b6d90d7618c3647",
      student: null,
      appointments: null,
      loading: true,  
      error: null,    
    };
  },
  created() {
    this.loading = true; 
    Promise.all([this.fetchCounselorData(), this.fetchAppointments()]).finally(() => {
      this.loading = false; 
    });
  },
  methods: {
    fetchCounselorData() {
      axios.get(`https://smu-team06-api.ede20ab.kyma.ondemand.com/student/${this.studentId}`)
        .then(response => {
          this.student = response.data;
          console.log('Student:', this.student)
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching student data:', error);
          this.error = 'Failed to load the counselor data.'; // Set the error variable here
          this.loading = false;
        });
    },
    fetchAppointments() {
      axios.get(`https://smu-team06-api.ede20ab.kyma.ondemand.com/bookingStudent/${this.studentId}`)
        .then(response => {
          this.appointments = response.data;
          console.log('Appointments:', this.appointments)
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching appointments:', error);
          this.error = 'Failed to load the appointments.'; // Set the error variable here
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