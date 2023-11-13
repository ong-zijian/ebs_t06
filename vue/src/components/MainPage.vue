<template>
  <div class="app-container">
    <!-- Header Section -->
    <div class="header">
      <div class="status-bar">
        <!-- Status bar content -->
      </div>
      <div class="user-greeting">
        <div class="greeting-text">
          <span class="hello-text">Hello,</span>
          <div v-if="user">
            <h3>{{ user.fname }}</h3>
          </div>
          <div v-else>
            <h3>Loading...</h3>
          </div>
        </div>
        <div class="d-flex justify-content-center align-items-center">
          <div class="d-flex justify-content-center align-items-center rounded-circle bg-primary text-white m-2" style="width: 3rem; height: 3rem; font-size: 1.5rem;">
            {{ user.fname.charAt(0) }}
          </div>
        </div>
      </div>
      <div class="card border-0 centered-container mb-4">
        <div class="d-flex justify-content-center align-items-center">
          <div class="d-flex justify-content-center align-items-center rounded-circle bg-primary text-white m-2" style="width: 5rem; height: 5rem; font-size: 3rem;">
            {{ user.fname.charAt(0) }}
          </div>
        </div><br>
          <h2>{{ user.fname }} {{ user.lname }}</h2>
      </div>
      
      <div class="mb-4 bg-secondary shadow p-2 text-white">
        <h2 class="text-center">Your Latest Emotion Score</h2>
        <h2 class="text-center">{{ this.plotData.datasets[0].data[this.plotData.datasets[0].data.length - 1] }}</h2>
        <p class="text-center">{{ userMessage }}</p>
      </div>
      <div v-if="journalMessages" >
        <div class="card shadow mb-4" :journal-entries="journalMessages.journal">
          <EmotionScoreChart :plot-data="plotData"/>
        </div>
        <WordCloud  :journal-entries="journalMessages.journal"/>
        <div class="content">
          <div class="message-card shadow" v-for="message in journalMessages.journal" :key="message._id">
            <div class="row inline">
              <h2>{{ message.title }}</h2>  
              <p>{{ message.date }}</p>
            </div>
            <p>{{ message.description }}</p>
          </div>  
        </div>
      </div>
      <div v-else>
        <div>
          <span>
            Loading...
          </span>
        </div>>
        
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import EmotionScoreChart from './EmotionScoreChart.vue';
import WordCloud from './WordCloud.vue';

export default {
  data() {
    return {
      journalMessages: { journal: [] },
      userProfileImage: 'https://w7.pngwing.com/pngs/205/731/png-transparent-default-avatar-thumbnail.png',
      user: null,
      plotData: {
        labels: [], 
        datasets: [{
          label: 'Score',
          data: [],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      messageToUser:["Keep it up and carry on the positivity!", "Not everyday is special, but you are doing great!", "Today might not be the best but it will get better!"]
    };
  },
  components: {
    EmotionScoreChart,
    WordCloud
  },
  created() {
    this.getAllJournal();
    this.getUserProfile();
  },
  computed:{
    userMessage() {
      const lastScore = this.plotData.datasets[0].data[this.plotData.datasets[0].data.length - 1];
      if (lastScore > 1) {
        return this.messageToUser[0];
      } else if (lastScore > -1) {
        return this.messageToUser[1];
      } else {
        return this.messageToUser[2];
      }
    }
  },
  methods: {
    // Your methods here
    async getAllJournal(){
      await axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/emotion/6544938b2b6d90d7618c3647')
      .then(response => {
          this.messages = response.data;
          this.journalMessages = this.messages;
          this.preparePlotData();
        //console.log(this.messages);
      })
    },
    async getUserProfile(){
      await axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/student/6544938b2b6d90d7618c3647')
      .then(response => {
        this.user = response.data;
        this.userProfileImage = this.user.image;
        console.log(this.user);
      })
    },
    preparePlotData() {
      if (this.journalMessages && Array.isArray(this.journalMessages.score)) {
        const sortedScores = this.journalMessages.score.sort((a, b) => new Date(a.date) - new Date(b.date));
        const scoresToPlot = sortedScores.slice(-7); // Get the last 7 scores
        
        // Update plotData with the scores and dates
        this.plotData.labels = scoresToPlot.map(entry => entry.date);
        this.plotData.datasets[0].data = scoresToPlot.map(entry => entry.score * 5);
        console.log(this.plotData);
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
}</style>
