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
          <div v-if="this.user.fname">
            <h1>Hi {{ this.user.fname }}</h1>
          </div>
          <div v-else>
            <h1>Hi</h1>
          </div>
        </div>
        <div class="initial-icon">
          S <!-- This will be dynamically generated based on the user's name -->
        </div>
      </div>
      <div class="centered-container mb-4">
        <div class="user-image-container">
          <img :src="userProfileImage" alt="Sarah" class="user-image">
        </div>
      </div>
      <div class="mb-4 bg-secondary shadow p-2 text-white">
        <h2 class="text-center">Your Latest Emotion Score</h2>
        <h2 class="text-center">{{ this.plotData.datasets[0].data[this.plotData.datasets[0].data.length - 1] }}</h2>
        <p class="text-center">{{ userMessage }}</p>
      </div>
      <div class="card shadow mb-4">
        <canvas id="scoreChart"></canvas>
      </div>
      <div ref="wordcloud"></div>
      <div class="content" v-if="journalMessages">
        <div class="message-card shadow" v-for="message in journalMessages.journal" :key="message._id">
          <div class="row inline">
            <h2>{{ message.title }}</h2>  
            <p>{{ message.date }}</p>
          </div>
          <p>{{ message.description }}</p>
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
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import * as d3 from 'd3';
import d3Cloud from 'd3-cloud';

export default {
  data() {
    return {
      // messages: [
      //   { id: 1, title: 'Tiring Day', content: 'Today was a tiring day for me. omg, I need to rant about...' },
      //   { id: 2, title: 'V tired', content: 'zzz' },
      //   // Add more message objects here
      // ],
      journalMessages: null,
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
  created() {
    this.getAllJournal();
    this.getUserProfile();
  },
  mounted() {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: this.plotData,
      options: {
        scales: {
          y: {
            beginAtZero: true,
            grid:{
              display: false
            }
          }
        },
        x:{
          grid:{
            display: false
          }
        },
        plugins: {
          legend: {
            display: false
          }
        }
      }
    });
    // Set up dimensions for the word cloud SVG
    let width = 500;
    let height = 500;

    // Select the container in which to append the SVG
    let svg = d3.select(this.$refs.wordcloud).append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // Prepare the word data for the word cloud
    let wordCloudData = this.createWordFrequencyArray(this.journalMessages.journal);

    // Set up the size scale for the word cloud
    let sizeScale = d3.scaleLinear()
      .domain([0, d3.max(wordCloudData, d => d.size)])
      .range([10, 100]); // Adjust min and max font sizes as needed

    // Create the word cloud layout and draw
    let layout = d3Cloud()
      .size([width, height])
      .words(wordCloudData)
      .padding(5)
      .rotate(() => 0) // Rotation of words; adjust as needed
      .font("Impact")
      .fontSize(d => sizeScale(d.size))
      .on("end", words => {
        svg.selectAll("text")
          .data(words)
          .enter().append("text")
          .style("font-size", d => d.size + "px")
          .style("fill", "#000") // Set the text color
          .attr("text-anchor", "middle")
          .attr("transform", d => `translate(${d.x}, ${d.y})rotate(${d.rotate})`)
          .text(d => d.text);
      });

    // Start the layout calculation
    layout.start();
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
        console.log(this.messages);
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
      const sortedScores = this.journalMessages.score.sort((a, b) => new Date(a.date) - new Date(b.date));
      const scoresToPlot = sortedScores.slice(-7); // Get the last 7 scores
      
      // Update plotData with the scores and dates
      this.plotData.labels = scoresToPlot.map(entry => entry.date);
      this.plotData.datasets[0].data = scoresToPlot.map(entry => entry.score * 5);
      console.log(this.plotData);
    },
    createWordFrequencyArray(journalEntries) {
      let allDescriptions = journalEntries.map(entry => entry.description).join(" ");
      let wordArray = allDescriptions.split(/\s+/);

      let wordFrequency = wordArray.reduce((accumulator, word) => {
        let cleanedWord = word.replace(/[^\w\s]|_/g, "").toLowerCase();
        if (cleanedWord && cleanedWord.length > 3) { // skip short words
          accumulator[cleanedWord] = (accumulator[cleanedWord] || 0) + 1;
        }
        return accumulator;
      }, {});

      return Object.keys(wordFrequency).map(word => {
        return { text: word, size: wordFrequency[word] };
      });
    }
  },
  // ...
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
