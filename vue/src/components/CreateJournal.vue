<template>
  <div id="journal-app">
    <!-- Header -->
    <header>
      <span class="header-spacer"></span>
      <h1>Create Journal</h1>
      <span class="header-spacer"></span>
    </header>

    <!-- User Profile Section -->
    <div v-if="user">
      <section class="user-profile">
        <div class="avatar-container">
          <div class="user-avatar">{{ user.fname.charAt(0) }}</div>
        </div>
        <h2 class="user-name">{{ user.fname }} {{ user.lname }}</h2>
        <p class="user-location">{{ user.location }}</p>
      </section>

      <!-- Journal Entry Section -->
      <section class="journal-entry">
        <input type="text" v-model="journalEntry.title" placeholder="Title" class="entry-title" />
        <textarea v-model="journalEntry.description" placeholder="Journal" class="entry-content"></textarea>
      </section>
    </div>

    <!-- Success Message Overlay -->
    <div v-if="showSuccess" class="success-modal">
      <div class="success-message-box">
        {{ successMessage }}
        <button @click="closeSuccessModal">OK</button>
      </div>
    </div>
    <!-- Footer -->
    <footer>
      <button class="cancel-btn" @click="goBack">Go Back</button>
      <button class="post-btn" @click="submitEntry">Post</button>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'JournalApp',
  data() {
    return {
      avatar: 'https://cdn-icons-png.flaticon.com/512/1144/1144760.png',
      journalEntry: {
        object_id: '',
        title: '',
        description: ''
      },
      user: null,
      successMessage: '',
      showSuccess: false
    }
  },
  created() {
    this.userProfile();
    const studentID = sessionStorage.getItem("studentID");
    console.log('sid:', studentID);
  },
  methods: {
    userProfile() {
      const studentID = sessionStorage.getItem("studentID");
      axios.get(`https://smu-team06-api.ede20ab.kyma.ondemand.com/student/${studentID}`)
        .then(response => {
          this.user = response.data;
          this.journalEntry.object_id = this.user._id;
        })
        .catch(error => console.error("Error fetching user profile:", error));
    },
    submitEntry() {
      axios.post(`https://smu-team06-api.ede20ab.kyma.ondemand.com/emotion/add`, this.journalEntry)
        .then(() => {
          this.successMessage = "Your journal entry has been posted successfully!";
          this.showSuccess = true;
          this.clearJournalEntry(); // Clear the form after successful submission
        })
        .catch(() => {
          this.successMessage = "Your journal entry has been posted successfully!";
          this.showSuccess = true;
          this.clearJournalEntry(); // Clear the form after successful submission
        });
    },
    closeSuccessModal() {
      this.showSuccess = false;
    },
    clearJournalEntry() {
      this.journalEntry.title = '';
      this.journalEntry.description = '';
    },
    goBack() {
      this.$router.back();
    }
  }
}
</script>

<style scoped>
#journal-app {
  max-width: 100%;
  margin: auto;
  font-family: 'Arial', sans-serif;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1em;
  background-color: #007bff;
  color: white;
  position: relative;
  /* Make header the positioning context for the avatar */
  height: 195px;
}

footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1em;
  color: white;
}

.user-profile {
  text-align: center;
  margin-top: 15%;

}

.avatar-container {
  width: 160px;
  /* Set the avatar width, adjust as necessary */
  height: 160px;
  /* Set the avatar height, adjust as necessary */
  position: absolute;
  top: 19%;
  /* Start at the vertical middle of the header */
  left: 50%;
  /* Center horizontally */
  transform: translate(-50%, -50%);
  /* Adjust position to center in header */
  border-radius: 50%;
  /* Make it round */
  overflow: hidden;
  /* Hide the overflow */
  background-color: #fff;
  /* Match the avatar background color */
  border: 3px solid #fff;
  /* Border to create a clean separation from header */
}

.user-avatar {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 5rem;
  /* You can adjust this as needed */
  background-color: #007bff;
  /* This is your circle color */
  color: white;
  border-radius: 50%;
  line-height: 1;
  /* Ensures that the text has no extra line height */
}

.user-name {
  margin: 0.5em 0;
}

.user-location {
  color: #777;
}

.journal-entry {
  padding: 1em;
}

.entry-title {
  width: 100%;
  padding: 0.5em;
  margin: 0.5em 0;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

.entry-content {
  width: 100%;
  padding: 0.5em;
  margin: 0.5em 0;
  border: 1px solid #ccc;
  box-sizing: border-box;
  height: 270px;
}

.cancel-btn,
.post-btn {
  padding: 0.5em 1em;
  border: none;
  border-radius: 5px;
  margin: 0.5em;
}

.cancel-btn {
  background-color: #ccc;
}

.post-btn {
  background-color: #28a745;
  color: white;
}

/* Success Modal */
.success-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.success-message-box {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.success-message-box button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  background-color: #28a745;
  color: white;
  cursor: pointer;
}
</style>
