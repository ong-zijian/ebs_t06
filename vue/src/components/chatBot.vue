<template>
  <div class="app-container">
    <div class="header">
      <div class="container">
        <div class="row padded_row">
          <div class="col-md-7">
            <div class="chat_window">
              <div class="top_menu">
                <div class="title">Franky Chat</div>
              </div>
              <ul class="messages">
                <li
                  v-for="(message, index) in messages.slice()"
                  :key="index"
                  :class="[message.message_side === 'right' ? 'right' : '', 'message']"
                >
                  <div class="text_wrapper">
                    <div class="text">{{ message.text }}</div>
                    <div class="timestamp">{{ message.time }}</div>
                  </div>
                </li>
              </ul>

            </div>
            <div class="bottom_wrapper">
              <div class="input_container">
                <input v-model="message" type="text" id="msg_input" placeholder="Share your thoughts...">
                <button @click="sendMessage">Send</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      messages: [], // An array to store chat messages
      userMessages: [],
    };
  },
  methods: {
    renderMessageToScreen(args) {
      const displayDate = (args.time || this.getCurrentTimestamp()).toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
      });
      const messagesContainer = this.$el.querySelector('.messages'); // Use Vue's ref feature

      // Create a new message element
      const message = document.createElement('li');
      message.className = `message ${args.message_side}`;

      // Create the text wrapper element
      const textWrapper = document.createElement('div');
      textWrapper.className = 'text_wrapper';

      // Create the text element
      const text = document.createElement('div');
      text.className = 'text';
      text.textContent = args.text;

      // Create the timestamp element
      const timestamp = document.createElement('div');
      timestamp.className = 'timestamp';
      timestamp.textContent = displayDate;

      // Append the elements to the message
      textWrapper.appendChild(text);
      textWrapper.appendChild(timestamp);
      message.appendChild(textWrapper);

      // Append the message to the parent
      messagesContainer.appendChild(message);

      // Perform animations
      setTimeout(() => {
        message.classList.add('appeared');
      }, 0);

      // Scroll to the bottom of the chat window
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },
    sendMessage() {
      // Your existing send message logic...
      // User sends a message
      console.log("Before sending message: ", this.message);
      this.showUserMessage(this.message, new Date());
      console.log("test message: ", this.messages);

      // Make the botKyma() request with the user's input
      this.botKyma(this.message)
        .then(response => {
          // Once the response is received, show the actual bot message
          this.showBotMessage(response, new Date());
        })
        .catch(error => {
          // Handle any errors
          console.error(error);
        });
      this.message = '';
    },
    botKyma(userInput) {
      // Return a promise to handle the asynchronous nature of the Axios request
      console.log(userInput);
      return axios
        .post("https://smu-team06-api.ede20ab.kyma.ondemand.com/chatbot", {
          user_input: userInput,
        })
        .then(response => {
          // Return the bot's response
          return response.data.response;
        })
        .catch(error => {
          // Handle any errors
          throw error;
        });
    },
    showUserMessage(message, datetime) {
      if (datetime instanceof Date) {
        const userMessage = {
          text: message,
          time: datetime.toLocaleString('en-IN', {
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
          }),
          message_side: 'right',
        };
        console.log(this.messages);
        this.messages.push(userMessage); // Add the user's message to the messages array
        this.scrollChatToBottom(); // Scroll to the bottom of the chat window immediately
      } else {
        console.error('Invalid datetime object:', datetime);
      }
    },

    showBotMessage(message, datetime) {
      const botMessage = {
        text: message,
        time: datetime.toLocaleString('en-IN', {
          month: 'short',
          day: 'numeric',
          hour: 'numeric',
          minute: 'numeric',
        }),
        message_side: 'left',
      };

      this.messages.push(botMessage); // Add the bot's message to the messages array
      this.message = ''; // Clear the input field
      this.scrollChatToBottom(); // Scroll to the bottom of the chat window immediately
    },

    // Function to scroll the chat to the bottom
    scrollChatToBottom() {
      const messagesContainer = this.$el.querySelector('.messages');
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },
  },
};

</script>


<style scoped>
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


/* Franky chatbot */
.app-container {
  font-family: Arial, sans-serif;
  background-color: #f2f2f2; /* Soothing background color */
}

.header {
  background-color: #E4E4DC; /* Header color */
  color: #fff;
  padding: 20px;
}

.chat_window {
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  overflow: auto; /* Allow the messages to scroll inside the chat_window */
  background-color: #fff; /* Chat window background */
  height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Keep messages aligned at the top */
  position: relative; /* Add position relative */
}

.messages {
  list-style-type: none;
  margin: 0;
  padding: 0;
  flex: 1; /* Allow messages to grow and take up available space */
}

.bottom_wrapper {
  background-color: #fff; /* Input area background color */
  padding: 10px;
  position: relative; /* Keep the input_container relative to the chat_window */
  flex-shrink: 0; /* Prevent the input_container from shrinking */
}

.input_container {
  display: flex;
}

.top_menu {
  background-color: #1CAC78;
  padding: 10px;
  text-align: center;
  font-weight: bold;
}

.message {
  display: flex;
  margin: 10px;
}

.text_wrapper {
  background-color: #f9f9f9;  /*Message background color */
  border-radius: 5px;
  padding: 5px;
}

/* Styles for user messages on the right side */
.message.right {
  justify-content: flex-end; /* Align to the right side */
}

.text_wrapper.left {
  background-color: #f9f9f9; /* Background color for bot messages on the left */
  color: #000; /* Text color for bot messages on the left */
}
/* Style for the text wrapper of user messages on the right side */
.right message.text_wrapper {
  background-color: #1CAC78; /* Background color for user messages on the right */
  color: #fff; /* Text color for user messages on the right */
}

.text {
  font-size: 14px;
  color: #000; /* Improved text visibility */
  padding: 5%;
}

.timestamp {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}


input[type="text"] {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  background-color: #1CAC78;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  margin-left: 10px;
  cursor: pointer;
}
</style>
