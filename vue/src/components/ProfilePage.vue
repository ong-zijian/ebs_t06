<template>
  <header class="header">
    <button class="settings-btn"></button>
    <h1 class="header-title">Profile</h1>
    <button class="logout-btn" @click="confirmLogout">Logout</button>
  </header>
  <div v-if="showLogoutConfirmation" class="logout-confirmation-overlay">
    <div class="logout-confirmation-box">
      <p>Are you sure you want to logout?</p>
      <button @click="logout">Yes</button>
      <button @click="showLogoutConfirmation = false">No</button>
    </div>
  </div>
  <div class="profile-container mt-2 mb-4" v-if="!loading && student">
    <div class="card shadow m-2 p-2">
      <div class="d-flex justify-content-center align-items-center">
        <div class="d-flex justify-content-center align-items-center rounded-circle bg-primary text-white m-2"
          style="width: 5rem; height: 5rem; font-size: 3rem;">
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
        <p><strong>Start Time:</strong> {{ formatDate(appointment.sDateTime) }}</p>
        <p><strong>End Time:</strong> {{ formatDate(appointment.eDateTime) }}</p>
        <p><strong>Link:</strong> <a :href="appointment.video" target="_blank">{{ appointment.video }}</a></p>
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
      showLogoutConfirmation: false,
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
      var studentID = sessionStorage.getItem("studentID");
      axios.get(`https://smu-team06-api.ede20ab.kyma.ondemand.com/student/` + studentID)
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
      var studentID = sessionStorage.getItem("studentID");
      axios.get(`https://smu-team06-api.ede20ab.kyma.ondemand.com/bookingStudent/` + studentID)
        .then(response => {
          // Assuming `response.data` is an array of appointments
          this.appointments = response.data.sort((a, b) => {
            // Convert the start times to Date objects and compare them
            return new Date(a.sDateTime) - new Date(b.sDateTime);
          });
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
    confirmLogout() {
      this.showLogoutConfirmation = true;
    },
    logout() {
      sessionStorage.clear();
      this.$router.push('/');
    },
    formatDate(dateTimeString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateTimeString).toLocaleString('en-US', options);
    },
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
  /* This will space out your items */
  align-items: center;
  padding: 1rem;
  background-color: #007BFF;
  color: white;
  font-size: 1.5rem;
  /* Adjust the size as needed */
}

.header-title {
  flex: 1;
  text-align: center;
  margin: 0;
  /* Ensure the title has no margin to center it correctly */
  font-size: 1.5rem;
  /* Adjust the size as needed */
}

.settings-btn,
.logout-btn {
  /* Adjust padding as needed to give buttons more space */
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  /* Adjust the size as needed */
}

.header-title {
  /* No changes needed here */
  margin: 0;
  /* Ensures the title has no extra space around it */
}

/* Ensure that both buttons have the same width to maintain balance */
.settings-btn,
.logout-btn {
  min-width: 80px;
  /* Adjust as needed */
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
  object-fit: cover;
  /* Ensure the image covers the container without distortion */
}

.counselor-name {
  margin-top: 70px;
  /* Adjust this value as needed */
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
}

.logout-confirmation-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 100;
}

.logout-confirmation-box {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.logout-confirmation-box button {
  margin: 10px;
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
}
</style>