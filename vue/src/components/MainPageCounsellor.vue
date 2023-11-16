<template>
  <div>
    <header class="header">
      <!-- <button class="settings-btn"></button> -->
      <button @click="adminPage">Alerts</button>
      <h1 class="header-title">Home</h1>
      <button class="logout-btn" @click="confirmLogout">Logout</button>
    </header>
    <div class="profile-container mt-2 mb-4">
      <div class="card shadow m-2 p-2">
        <div class="d-flex justify-content-center align-items-center">
          <div class="d-flex justify-content-center align-items-center rounded-circle bg-primary text-white m-2"
            style="width: 5rem; height: 5rem; font-size: 3rem;">
            {{ fname.charAt(0) }}
          </div>
        </div>
        <div class="text-center">
          <h2>{{ fname }} {{ lname }}</h2>
        </div>
        <form class="form">
          <div class="form-group row mt-3">
            <label for="name" class="col-form-label"><strong>Email:</strong></label>
            <div>
              <input type="text" id="name" class="form-control" :value="email" readonly>
            </div>
          </div>
        </form>
      </div>

      <div class="text-center p-2">
        <h2>Upcoming Appointments</h2>
        <div v-for="appointment in upcomingAppointments" :key="appointment._id" class="card shadow m-2 p-2 text-left">
          <p><strong>Start Time:</strong> {{ formatDate(appointment.sDateTime) }}</p>
          <p><strong>End Time:</strong> {{ formatDate(appointment.eDateTime) }}</p>
          <p><strong>Link:</strong> <a :href="appointment.video" target="_blank">{{ appointment.video }}</a></p>
        </div>
      </div>

      <div class="text-center p-2">
        <h2>Past Appointments</h2>
        <div v-for="appointment in pastAppointments" :key="appointment._id" class="card shadow m-2 p-2 text-left">
          <p><strong>Start Time:</strong> {{ formatDate(appointment.sDateTime) }}</p>
          <p><strong>End Time:</strong> {{ formatDate(appointment.eDateTime) }}</p>
          <p><strong>Link:</strong> <a :href="appointment.video" target="_blank">{{ appointment.video }}</a></p>
        </div>
      </div>
    </div>

  </div>
  <div v-if="showLogoutConfirmation" class="modal-overlay">
    <div class="modal-container">
      <p>Are you sure you want to logout?</p>
      <div class="modal-button-container">
        <button @click="logout">Yes</button>
        <button @click="cancelLogout">No</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      counsellor_ID: null,
      fname: null,
      lname: null,
      email: null,
      appointments: [],
      showLogoutConfirmation: false,
    };
  },
  created() {
    this.getAllAppointments();
  },
  computed: {
    upcomingAppointments() {
      const now = new Date();
      return this.appointments.filter(appointment => new Date(appointment.sDateTime) > now);
    },
    pastAppointments() {
      const now = new Date();
      return this.appointments.filter(appointment => new Date(appointment.sDateTime) <= now);
    },
  },
  methods: {
    async getAllAppointments() {
      this.counsellor_ID = sessionStorage.getItem('counselorID');
      this.fname = sessionStorage.getItem('counselorFName');
      this.lname = sessionStorage.getItem('counselorLName');
      this.email = sessionStorage.getItem('counselorEmail');
      await axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/bookingCounsellor/' + this.counsellor_ID)
        .then(response => {
          this.appointments = response.data;
          console.log('appointments: ', this.appointments);
        })
    },
    formatDate(dateTimeString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateTimeString).toLocaleString('en-US', options);
    },
    confirmLogout() {
      this.showLogoutConfirmation = true;
    },
    logout() {
      sessionStorage.clear();
      this.$router.push('/CounselorLogin'); // Replace '/login' with your actual login route
      this.showLogoutConfirmation = false;
    },
    cancelLogout() {
      this.showLogoutConfirmation = false;
    },
    adminPage() {
      this.$router.push('/AdminPage');
    },
  },
};
</script>

<style scoped>
/* Existing styles... */

.user-greeting {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* Adjusted for spacing */
  background-color: #fff;
  /* Light blue background */
  padding: 1em;
}

.hello-text {
  font-size: 1.2em;
  /* Adjust size as needed */
  color: #000;
  /* Black text */
  align-self: flex-start;
  /* Aligns 'Hello' to the top */
}

.initial-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  /* Adjust as needed */
  background: #4287f5;
  font-weight: bold;
  margin-left: auto;
  /* Pushes the initial to the right */
}

.greeting-text {
  text-align: left;
  /* Aligns text to the left */
}

.greeting-text h1 {
  margin: 0;
  color: #000;
  /* Black text */
}

.user-image-container {
  background-color: #4287f5;
  /* Replace with your preferred color */
  border-radius: 20px;
  /* Adjust for desired roundness of corners */
  width: 305px;
  /* Adjust as needed */
  height: 182px;
  /* Adjust as needed */
  display: flex;
  justify-content: center;
  align-items: center;
}

.user-image {
  width: 100px;
  /* Adjust as needed */
  height: 100px;
  /* Adjust as needed */
  border-radius: 50%;
  /* This makes the image circular */
  border: 3px solid #ffffff;
  /* Adjust color and size as needed */
  box-sizing: border-box;
}

/* Rest of your CSS... */
.message-card {
  /* Replace with the desired background color */
  border-radius: 10px;
  padding: 1em;
  margin-bottom: 1em;

}

html,
body {
  height: 100%;
  /* This makes sure the body takes up the full viewport height */
  margin: 0;
  /* Removes default margin */
}

.centered-container {
  display: flex;
  justify-content: center;
  /* Centers horizontally */
  align-items: center;
  /* Centers vertically */
  height: 100%;
  /* Takes up the full height of the viewport */
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  /* High z-index to be on top of other content */
}

.modal-container {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  /* Ensure it's above the overlay */
}

.modal-button-container {
  display: flex;
  justify-content: space-between;
  /* This will place one button at each end */
}

.modal-container button {
  padding: 10px 20px;
  margin-top: 20px;
  /* Add some space above the buttons */
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  flex: 1;
  /* This makes the buttons take up equal space */
}

.modal-container button {
  max-width: 100px;
  /* Adjust as needed */
}
</style>
