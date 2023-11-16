<template>
  <div class="container">
    <div class="login-container">
      <div class="  text-center">
        <img src="../assets/aichatbot.png" alt="MindSculpt Logo" class="w-50 h-50">
        <h1>MindSculpt</h1>
      </div>
      <h1>STUDENT SIGN IN</h1>
      <form @submit.prevent="login">
        <div class="input-group">
          <input type="email" placeholder="Email" v-model="credentials.email" required>
        </div>
        <div class="input-group">
          <input type="password" placeholder="Password" v-model="credentials.password" required>
        </div>
        <div class="register-link">
          You're a counselor? <router-link to="/CounselorLogin" active-class="active-link">Click Here</router-link>
        </div>
        <div class="consent-group">
          <label>
            <input type="checkbox" v-model="consentChecked" class="checkeddata" @change="handleConsentChange">
            <span>I agree to share my data</span>
          </label>
        </div>
        <div v-if="showNotificationModal" class="notification-modal">
          <span v-html="notificationContent"></span>
          <button @click="hideNotificationModal">Close</button>
        </div>
        <button type="submit">LOGIN</button>
      </form>
    </div>
  </div>
  <div class="alert" ref="alert">
    Please check the consent box before logging in or enter correct username/password.
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      students: [],
      credentials: {
        email: '',
        password: '',
      },
      loginSuccessful: false,
      consentChecked: false,
      showNotificationModal: false,
      notificationContent: "",
    };
  },
  created() {
    this.fetchStudents();
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/students');
        this.students = response.data;
      } catch (error) {
        console.error('There was an error fetching the students:', error);
      }
    },
    login() {
      const user = this.students.find(student => student.email === this.credentials.email);
      if (user && user.password === this.credentials.password && this.consentChecked) {
        // Perform login action
        this.loginSuccessful = true;

        // Store user details in sessionStorage
        
        sessionStorage.setItem('studentID', user._id);
        sessionStorage.setItem('studentFName', user.fname);
        sessionStorage.setItem('studentLName', user.lname);
        sessionStorage.setItem('studentLocation', user.location);
        sessionStorage.setItem('studentEmail', user.email);
        sessionStorage.setItem('userType', 'student');

        // Navigate to the root URL
        this.$router.push('/home');
      } else {
        // Handle login failure
        this.showAlert();
      }
    },
    showAlert() {
    const alertElement = document.querySelector('.alert');
    alertElement.style.display = 'block';
    setTimeout(() => {
      alertElement.style.display = 'none';
    }, 5000); // Hide the alert after 5 seconds, adjust as needed
  },
  handleConsentChange() {
    if (this.consentChecked) {
      // Set notification content
      this.notificationContent = `
        <div>
          <h2>PDPA Consent for User Data</h2>
          <p>
            By proceeding to use this web application, you acknowledge and consent to the collection and processing of your personal data for the sole purpose of studying and improving user mental wellness. Your data will be handled with the utmost confidentiality and used exclusively to enhance our algorithm, providing you with a more personalized and effective experience.
          </p>
          <p>
            We adhere to the principles of the Personal Data Protection Act (PDPA) and assure you that your information will not be shared with third parties without your explicit consent.
          </p>
        </div>
      `;

      // Show the notification modal
      this.showNotificationModal = true;
    }
  },
  hideNotificationModal() {
    // Hide the notification modal
    this.showNotificationModal = false;
  },
  
}
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background: #f0f0f0; /* Or any other background color you prefer */
}

.login-container {
  background: #fff;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  width: 100%; /* Makes the container take full width */
  max-width: 400px; /* Sets a maximum width */
}

h1 {
  margin-bottom: 2rem;
}

.input-group {
  margin-bottom: 1rem;
}

input {
  width: calc(100% - 20px); /* 100% width minus the total horizontal padding */
  padding: 10px;
  margin: 0; /* Removes default margin */
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box; 
}

.register-link {
  margin: 1rem 0;
}

button {
  width: 100%;
  padding: 10px;
  background: #000;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #333;
}

.consent-group {
  margin-bottom: 1rem;
}

label {
  display: flex;
  align-items: center;
}

span {
  margin-left: -140px; 
  align-self: flex-start; 

}

.checkeddata{
  margin-left: -150px; 
}

.alert {
  position: fixed;
  margin-top: 2%;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ff5252; 
  color: #fff;
  padding: 1rem;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  display: none;
}
/* PDPA Notification */
.notification-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #f0f0f0; 
  padding: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); 
  color: #333; 
}

.notification-modal button {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #555; 
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.notification-modal button:hover {
  background-color: #FF8C00;
}
</style>
