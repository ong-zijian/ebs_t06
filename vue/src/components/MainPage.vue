<template>
  <div class="app-container">
    <div class="header">
      <!-- Greeting section -->
      <div v-if="user" :style="{ backgroundColor: userMessageBackgroundColor }" class="user-greeting d-flex justify-content-between align-items-center p-3 bg-light rounded">
        <div class="greeting-text">
          <span class="hello-text text-secondary">Hello,</span>
          <h3 class="mb-0">{{ user.fname }}</h3>
        </div>
        <div :style="{ backgroundColor: userMessageBackgroundColor }" class="user-avatar d-flex justify-content-center align-items-center bg-primary text-white rounded-circle m-2"
          style="width: 3rem; height: 3rem; font-size: 1.5rem;">
          {{ user?.fname.charAt(0) }}
        </div>
      </div>
      <div v-else>
        <h3 class="mb-0">Loading...</h3>
      </div>

      <!-- User profile and name -->
      <div v-if="user" class="card border-0 centered-container mb-4">
        <div class="d-flex justify-content-center align-items-center">
          <div class="d-flex justify-content-center align-items-center rounded-circle bg-primary text-white m-2"
            style="width: 5rem; height: 5rem; font-size: 3rem;">
            {{ user.fname.charAt(0) }}
          </div>
        </div><br>
        <h2>{{ user.fname }} {{ user.lname }}</h2>
        <div class="row m-2 p-2">
          <div class="col text-center">
            <button :style="{ backgroundColor: userMessageBackgroundColor }" class="btn text-white fw-bold w-75" @click="positiveLiving">Positive Living Tip</button>
          </div>
          <div class="col text-center">
            <button :style="{ backgroundColor: userMessageBackgroundColor }" class="btn text-white fw-bold w-80" @click="managingAttack">Managing Panic Attack </button>
          </div>
        </div>
      </div>

      <!-- Emotion score section -->
      <div v-if="plotData.datasets[0].data.length" class="mb-4 shadow p-2 text-white"
        :style="{ backgroundColor: userMessageBackgroundColor }">
        <h2 class="text-center">Your Latest Emotion Score</h2>
        <h2 class="text-center">{{ plotData.datasets[0].data[plotData.datasets[0].data.length-1] }}</h2>
        <p class="text-center">{{ userMessage }}</p>
      </div>

      <div class="m-2 p-2 text-center">
        <h2 class="text-center">Your Streak:</h2>
        <span v-if="calculateStreak() >= 3" :style="{ backgroundColor: userMessageBackgroundColor }" class="badge py-2 px-4 my-2 d-inline-block fs-3">{{ calculateStreak() }} days 🔥</span>
        <div class="progress my-3" style="height: 35px;">
          <div class="progress-bar" role="progressbar" :style="{ width: streakPercentage + '%', backgroundColor: userMessageBackgroundColor  }" :aria-valuenow="calculateStreak()" aria-valuemin="0" aria-valuemax="30">
            {{ calculateStreak() }} / 30 days
          </div>
        </div>
      </div>

      <!-- Journal entries -->
      <div v-if="journalMessages">
        <div class="card shadow mb-4">
          <EmotionScoreChart :plot-data="plotData" />
        </div>

        <div class="text-center">
          <WordCloud :journal-entries="journalMessages.journal" />
        </div>

        <div class="content bg-light p-4">
          <div v-for="message in reversedJournalMessages" :key="message._id"
            class="message-card shadow mb-4 p-3 bg-white rounded">
            <div class="row">
              <div class="col-md-8">
                <h2 class="mb-2">{{ message.title }}</h2>
                <p class="text-muted">{{ message.date }}</p>
              </div>
            </div>
            <p>{{ message.description }}</p>
          </div>
        </div>
      </div>
      <div v-else>
        <span>Loading...</span>
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
      journalMessages: null,
      userProfileImage: 'https://w7.pngwing.com/pngs/205/731/png-transparent-default-avatar-thumbnail.png',
      user: null,
      plotData: {
        labels: [],
        datasets: [{
          label: 'Emotion Score',
          data: [],
          fill: true,
          lineTension: 0.4,
          backgroundColor: 'rgba(54, 162, 235, 0.4)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 2,
          pointRadius: 5,
          pointBackgroundColor: function (context) {
            var value = context.dataset.data[context.dataIndex];
            return value >= 0 ? 'rgba(0, 255, 0, 1)' : 'rgba(255, 0, 0, 1)';
          },
        }],
      },
      messageToUser: ["Keep it up and carry on the positivity!", "Not everyday is special, but you are doing great!", "Today might not be the best but it will get better!"]
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
  computed: {
    userMessage() {
      const lastScore = this.plotData.datasets[0].data[this.plotData.datasets[0].data.length - 1];
      if (lastScore > 1) {
        return this.messageToUser[0];
      } else if (lastScore > -1) {
        return this.messageToUser[1];
      } else {
        return this.messageToUser[2];
      }
    },
    userMessageBackgroundColor() {
      const lastScore = this.plotData.datasets[0].data[this.plotData.datasets[0].data.length - 1];
      if (lastScore > 1) {
        return 'green';
      } else if (lastScore > -1) {
        return 'yellow';
      } else {
        return 'red';
      }
    },
    reversedJournalMessages() {
      // Check if journalMessages and journalMessages.journal are defined before calling slice
      if (this.journalMessages && this.journalMessages.journal) {
        return this.journalMessages.journal.slice().reverse();
      }
      return []; // Return an empty array if journalMessages.journal is undefined
    },
    currentStreak() {
      return this.calculateStreak();
    },
    streakPercentage() {
      return (this.calculateStreak() / 30) * 100;
    },

  },
  methods: {
    // Your methods here
    async getUserProfile() {
      var studentID = sessionStorage.getItem('studentID');
      await axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/student/' + studentID)
        .then(response => {
          this.user = response.data;
          this.userProfileImage = this.user.image;
          console.log(this.user);
        })
    },

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

    calculateStreak() {
      // Assuming journalMessages are already sorted by date in ascending order
      // If not, sort them first
      if (!this.journalMessages || !Array.isArray(this.journalMessages.journal)) {
        return 0;
      }

      const entries = this.journalMessages.journal;
      const today = new Date().setHours(0, 0, 0, 0);
      let streak = 0;
      let previousDate = new Date(today);

      for (let i = entries.length - 1; i >= 0; i--) {
        const entryDate = new Date(entries[i].date).setHours(0, 0, 0, 0);
        const timeDiff = previousDate - entryDate;
        const dayDiff = timeDiff / (1000 * 3600 * 24);

        if (dayDiff === 1) {
          // Consecutive day
          streak++;
        } else if (dayDiff > 1) {
          // Break in streak
          break;
        }

        previousDate = new Date(entryDate);
      }

      if (this.journalMessages && this.journalMessages.journal && this.journalMessages.journal.length > 0) {
        const lastEntry = this.journalMessages.journal[this.journalMessages.journal.length - 1];
        // Parse the date string to ensure it's a valid Date object
        const lastEntryDate = new Date(lastEntry.date);

        // Check if the date string was valid and lastEntryDate is a Date object
        if (!isNaN(lastEntryDate.getTime())) {
          // Compare dates without time
          const lastEntryDay = new Date(lastEntryDate.setHours(0, 0, 0, 0));
          const today = new Date().setHours(0, 0, 0, 0);

          if (lastEntryDay.getTime() === today) {
            streak++;
          }
        } else {
          console.error('Invalid date in last journal entry:', lastEntry.date);
        }
      }

      return streak;
    },
    getStreakAchievement() {
      const streak = this.calculateStreak();
      let achievement = '';

      if (  streak >= 30) {
        achievement = '1 month streak! Amazing!';
      } else if (streak >= 7) {
        achievement = '1 week streak! Keep going!';
      } else if (streak >= 3) {
        achievement = '3 days streak! Nice start!';
      }

      return {
        streak,
        achievement
      };
    },
    positiveLiving() {
      this.$router.push('/StayPositive');
    },  
    managingAttack() {
      this.$router.push('/ManagingAttacks');
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
