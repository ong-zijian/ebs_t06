<template>
  <div>
    <header class="header">
      <!-- <button class="settings-btn"></button> -->
      <button @click="goBack">Back</button>
      <h1 class="header-title"><button @click="profilePage">Home</button></h1>
      <button class="logout-btn" @click="confirmLogout">Logout</button>
    </header>
    <div v-if="alerts">
      <div class="text-center p-2">
        <h2>Alerts</h2>
      </div>
      <div v-for="alert in alerts" :key="alert._id" class="card shadow m-2 p-2 text-left">
        <table class="table">
          <tr>
            <td><strong>Student Name:</strong></td>
            <td>{{ alert.studentName }}</td>
          </tr>
          <tr>
            <td><strong>Student Email:</strong></td>
            <td>{{ alert.studentEmail }}</td>
          </tr>
          <tr>
            <td><strong>Message:</strong></td>
            <td>{{ alert.message }}</td>
          </tr>
          <tr>
            <td><strong>Status:</strong></td>
            <td>{{ alert.status }}</td>
          </tr>
          <tr>
            <td>
              <!--disable button if alert.status === "addressed"-->

              <button @click="address(alert._id)" class="btn btn-primary bg-primary text-white"
                :disabled="alert.status === 'addressed'">
                Addressed?
              </button>
            </td>
          </tr>
        </table>
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
      alerts: [],
      alertsFull: [],
    };
  },
  created() {
    this.getAllAlerts();
  },
  computed: {

  },
  methods: {
    async getAllAlerts() {
      this.counsellor_ID = sessionStorage.getItem('counselorID');
      this.fname = sessionStorage.getItem('counselorFName');
      this.lname = sessionStorage.getItem('counselorLName');
      this.email = sessionStorage.getItem('counselorEmail');
      await axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/checkStudent')
        .then(response => {
          this.alerts = response.data;
          console.log('alerts: ', this.alerts);
          this.populateAlerts();
        })
    },
    async populateAlerts() {
      for (const alert of this.alerts) {
        try {
          const response = await axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/student/' + alert.sid);
          // Add response data to the alert object
          alert.studentName = response.data.fname + " " + response.data.lname;
          alert.studentEmail = response.data.email;
        } catch (error) {
          console.error('Error fetching student details:', error);
          // Handle error, maybe set some defaults
          alert.studentName = 'Unknown';
          alert.studentEmail = 'Unknown';
        }
      }
      // This will ensure that Vue reacts to changes in the alerts array
      this.alerts = [...this.alerts];
    },
    goBack() {
      this.$router.go(-1); // This will take you one step back in the browser history
      // Alternatively, you can use:
      // this.$router.back();
    },
    address(objectID) {
      axios.put('https://smu-team06-api.ede20ab.kyma.ondemand.com/checkStudent/' + objectID + "/address")
        .then(response => {
          console.log(response.data);
          this.getAllAlerts();

        })
    },
    formatDate(dateTimeString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateTimeString).toLocaleString('en-US', options);
    },
    confirmLogout() {
      this.showLogoutConfirmation = true;
    },
    adminPage() {
      this.$router.push('/AdminPage');
    },
    profilePage() {
      this.$router.push('/CounsellorHome');
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
</style>
