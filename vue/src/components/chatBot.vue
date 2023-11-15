<template>
  <div class="app-container">
    <header class="app-header">
      <div class="logo-and-title">
        <img src="@/assets/aichatbot.png" alt="Logo" class="logo"/>
        <div class="title">Franky AI</div>
      </div>
    </header>

    <div class="chat-window" ref="messageList">
      <ul class="messages">
        <li v-for="(message, index) in messages" :key="index"
          :class="['message', message.message_side === 'right' ? 'right' : 'left']">
          <div class="text-wrapper">
            <div class="text">{{ message.text }}</div>
            <div class="timestamp">{{ message.time }}</div>
          </div>
        </li>
      </ul>
    </div>

    <div class="message-input">
      <input type="text" v-model="message" placeholder="Share your thoughts...">
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      messages: [],
      frankyChatIcon: `...` // SVG Icon
    };
  },
  mounted() {
    this.scrollChatToBottom();
  },
  methods: {
    sendMessage() {
      if (!this.message.trim()) return;

      const messagePayload = {
        text: this.message,
        time: new Date(),
        message_side: 'right',
      };
      this.addMessage(messagePayload);
      this.message = '';
      this.sendToBot(messagePayload.text);
      this.scrollChatToBottom();
    },
    addMessage(messagePayload) {
      this.messages.push({
        ...messagePayload,
        time: this.formatTimestamp(messagePayload.time),
      });
      this.scrollChatToBottom();
    },
    sendToBot(text) {
      axios.post("https://smu-team06-api.ede20ab.kyma.ondemand.com/chatbot", { user_input: text })
        .then(response => {
          this.addMessage({
            text: response.data.response,
            time: new Date(),
            message_side: 'left',
          });
          // No need to call scrollChatToBottom here because it's already called in addMessage
        })
        .catch(error => console.error('Error sending the message: ', error));
    },
    formatTimestamp(timestamp) {
      return timestamp.toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
      });
    },
    scrollChatToBottom() {
      this.$nextTick(() => {
        const chatWindow = this.$refs.messageList;
        console.log('Before scroll:', chatWindow.scrollTop, chatWindow.scrollHeight);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        console.log('After scroll:', chatWindow.scrollTop);
      });
    },

  },
};
</script>



<style scoped>

.logo-and-title {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px; /* Adjust based on your logo's size */
  margin-right: 10px; /* Adjust spacing between logo and title */
}

.app-header {
  background-color: #1e90ff;
  color: white;
  padding: 10px;
  display: flex;
  justify-content: center;
}

.title {
  font-size: 1.5rem;
  /* Other styles as needed */
}

.app-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 40px);
  /* Adjust 60px to the height of your footer */
  box-sizing: border-box;
  /* Include padding in the height calculation */
  background-color: #e6e6fa;
  font-family: Arial, sans-serif;
  overflow: hidden;
  /* Prevent scrolling outside the chat window */
}

.app-header {
  background-color: #1e90ff;
  color: white;
  padding: 20px;
  text-align: center;
}

.chat-window {
  flex-grow: 1;
  overflow: auto;
  padding: 20px;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
}

.messages {
  list-style: none;
  padding: 0;
}

.message {
  display: flex;
  padding: 0.5em;
  clear: both;
}

.message.right {
  justify-content: flex-end;
  align-self: flex-end;
}

.message.left {
  justify-content: flex-start;
  align-self: flex-start;
}

.message.left .text-wrapper {
  background-color: #e5e5ea;
  /* Light grey background for chatbot messages */
  color: black;
  margin-right: auto;
  /* Pushes the bubble to the left */
}

.message.right .text-wrapper {
  background-color: #dcf8c6;
  /* Light green background for user messages */
  color: black;
  margin-left: auto;
  /* Pushes the bubble to the right */
}

.text-wrapper {
  max-width: 80%;
  /* Max width for message bubbles */
  margin: 0.2em;
  padding: 0.5em 1em;
  border-radius: 15px;
  box-shadow: 0px 0px 5px 0px rgba(0, 0, 0, 0.15);
}

.message-input {
  display: flex;
  padding: 10px;
}

input[type="text"] {
  flex-grow: 1;
  border-radius: 5px;
  padding: 10px;
  border: 1px solid #ddd;
}

.chat-window {
  flex-grow: 1;
  overflow-y: auto;
  /* Other styles remain unchanged */
}

button {
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  margin-left: 10px;
  background-color: #1e90ff;
  color: white;
  cursor: pointer;
}
</style>
