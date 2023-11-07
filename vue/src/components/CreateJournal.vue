<template>
    <div id="journal-app">
        <header>
            <span class="settings-btn">Settings</span>
            <h1>Journal</h1>
            <span class="logout-btn">Logout</span>
        </header>

        <section class="user-profile">
            <div class="avatar-container">
                <img :src="user.avatar" :alt="user.name" class="user-avatar" />
            </div>
            <h2 class="user-name">{{ user.name }}</h2>
            <p class="user-location">{{ user.location }}</p>
        </section>

        <section class="journal-entry">
            <input type="text" v-model="journalEntry.title" placeholder="Title" class="entry-title" />
            <textarea v-model="journalEntry.content" placeholder="Journal" class="entry-content"></textarea>
        </section>

        <footer>
            <button class="cancel-btn">Cancel</button>
            <button class="post-btn" @click="submitEntry">Post</button>
        </footer>
    </div>
</template>
  
  <script>
  export default {
    name: 'JournalApp',
    data() {
      return {
        user: {
          name: 'Sarah Thompson',
          location: 'Singapore',
          avatar: 'https://w7.pngwing.com/pngs/205/731/png-transparent-default-avatar-thumbnail.png', // Replace with actual path
        },
        journalEntry: {
          title: '',
          content: ''
        }
      }
    },
    methods: {
      submitEntry() {
        // Handle the journal entry submission
        console.log("Title:", this.journalEntry.title);
        console.log("Content:", this.journalEntry.content);
        // You would typically send this data to a server here
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
  
  header, footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1em;
    background-color: #007bff;
    color: white;
  }
  
  .user-profile {
    text-align: center;
    margin-top: 20px;
  }
  
  .avatar-container {
    display: inline-block;
    width: 120px;
    height: 120px;
    margin-bottom: 10px;
  }
  
  .user-avatar {
    width: 100%;
    height: auto;
    border-radius: 50%;
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
  
  .entry-title, .entry-content {
    width: 100%;
    padding: 0.5em;
    margin: 0.5em 0;
    border: 1px solid #ccc;
    box-sizing: border-box;
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
  