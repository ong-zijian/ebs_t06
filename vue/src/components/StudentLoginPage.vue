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
        <button type="submit">LOGIN</button>
      </form>
    </div>
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
      if (user && user.password === this.credentials.password) {
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
        alert('Incorrect username or password.');
      }
    }
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
  box-sizing: border-box; /* Includes padding and border in the element's width and height */
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
</style>
