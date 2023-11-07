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
          <h1>Hi Sarah</h1>
        </div>
        <div class="initial-icon">
          S <!-- This will be dynamically generated based on the user's name -->
        </div>
      </div>
      <div class="centered-container">
        <div class="user-image-container">
          <img :src="userProfileImage" alt="Sarah" class="user-image">
        </div>
      </div>
      <div class="content">
        <div class="message-card" v-for="message in messages" :key="message.id">
          <h2>{{ message.title }}</h2>
          <p>{{ message.content }}</p>
        </div>
      </div>
    </div>
    <!-- Remaining sections -->

  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [
        { id: 1, title: 'Tiring Day', content: 'Today was a tiring day for me. omg, I need to rant about...' },
        { id: 2, title: 'V tired', content: 'zzz' },
        // Add more message objects here
      ],
      userProfileImage: 'https://w7.pngwing.com/pngs/205/731/png-transparent-default-avatar-thumbnail.png',
      // ...
    };
  },
  computed: {
    // Your computed properties here
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
