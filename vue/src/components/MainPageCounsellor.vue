<template>
  <div>
    <header class="header">
      <button class="settings-btn"></button>
      <h1 class="header-title">Profile</h1>
      <button class="logout-btn" @click="confirmLogout">Logout</button>
    </header>


  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
    
    };
  },
  created() {

  },
  computed: {

  },
  methods: {
    async getAllJournal() {
      var studentID = sessionStorage.getItem('studentID');
      await axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/emotion/' + studentID)
        .then(response => {
          this.messages = response.data;
          this.journalMessages = this.messages;
          console.log('journal msg: ', this.journalMessages);
          this.preparePlotData();
          //console.log(this.messages);
        })
    },
    preparePlotData() {
      if (this.journalMessages && Array.isArray(this.journalMessages.score)) {
        const sortedScores = this.journalMessages.score.sort((a, b) => new Date(a.date) - new Date(b.date));
        const scoresToPlot = sortedScores.slice(-7); // Get the last 7 scores

        // Update plotData with the scores and dates
        this.plotData.labels = scoresToPlot.map(entry => entry.date);
        this.plotData.datasets[0].data = scoresToPlot.map(entry => entry.score * 5);
        console.log("plot data:", this.plotData);
      }
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
