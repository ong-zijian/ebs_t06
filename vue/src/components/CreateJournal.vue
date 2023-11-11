<template>
  <div id="journal-app">
    <header>
      <span class="settings-btn">Settings</span>
      <h1>Journal</h1>
      <span class="logout-btn">Logout</span>
    </header>
    <div v-if="user">
      <section class="user-profile">
        <div class="avatar-container">
          <img :src="avatar" :alt="user.fname" class="user-avatar" />
        </div>
        <h2 class="user-name">{{ user.fname }} {{ user.lname }}</h2>
        <p class="user-location">{{ user.location }}</p>
      </section>

      <section class="journal-entry">
        <input type="text" v-model="journalEntry.title" placeholder="Title" class="entry-title" />
        <textarea v-model="journalEntry.description" placeholder="Journal" class="entry-content"></textarea>
      </section>
    </div>
    <div v-else>
      ...
    </div>

    <footer>
      <button class="cancel-btn">Cancel</button>
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
      user: null
    }
  },
  created() {
    this.userProfile();
  },
  methods: {
    userProfile(){
        axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/student/6544938b2b6d90d7618c3647')
        .then(response => {
          this.user = response.data;
          this.journalEntry.object_id = this.user._id;
          console.log(this.user);
        })
    },
    submitEntry() {
      // Handle the journal entry submission
      // console.log("Title:", this.journalEntry.title);
      // console.log("Content:", this.journalEntry.content);
      // You would typically send this data to a server here
      axios.post(`https://smu-team06-api.ede20ab.kyma.ondemand.com/emotion/add`, this.journalEntry)
      .then(response => {
        console.log(response);
      }) 
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
  position: relative; /* Make header the positioning context for the avatar */
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
  width: 160px; /* Set the avatar width, adjust as necessary */
  height: 160px; /* Set the avatar height, adjust as necessary */
  position: absolute;
  top: 19%; /* Start at the vertical middle of the header */
  left: 50%; /* Center horizontally */
  transform: translate(-50%, -50%); /* Adjust position to center in header */
  border-radius: 50%; /* Make it round */
  overflow: hidden; /* Hide the overflow */
  background-color: #fff; /* Match the avatar background color */
  border: 3px solid #fff; /* Border to create a clean separation from header */
}

.user-avatar {
  width: 100%;
  height: auto;
  border-radius: 50%; /* Update this to match the desired border-radius */
  /* Add any additional styling here for the avatar image */
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

.cancel-btn, .post-btn {
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

/* Add additional styling as per your design requirements */
</style>
