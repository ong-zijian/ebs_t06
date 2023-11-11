<template>
  <div class="rating-page">
    <div class="rating-container">
      <div class="star-rating">
        <!-- Use index+1 to match the rating with the number of stars -->
        <span v-for="index in 5" :key="index" class="star"
              :class="{ 'filled': rating >= index }"
              @click="rating = index">
          ★
        </span>
      </div>
      <h2>Rate Ada!</h2>
      <div class="comment-box">
        <label for="comment">Comment:</label>
        <textarea id="comment" v-model="comment" placeholder="Leave a comment..."></textarea>
      </div>
      <button @click="submitRating">Confirm</button>
      <p class="feedback" @click="giveFeedback">Don’t like the Service? Let us know.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rating: 0,
      comment: '',
    };
  },
  methods: {
    submitRating() {
      // Submit the rating and comment
      console.log('Rating:', this.rating);
      console.log('Comment:', this.comment);
      // Here you would typically make an API call to submit the rating and comment
    },
    giveFeedback() {
      // Handle feedback action
      console.log('Feedback action');
      // Possibly navigate to a feedback form or contact page
    }
  }
};
</script>

<style scoped>
.rating-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #007bff; /* Set the page background to blue */
}

.rating-container {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  width: 90%; /* Adjust the width as per your design */
  max-width: 400px; /* Maximum width */
}

.star-rating {
  color: gray;
  font-size: 25px;
  cursor: pointer;
}

.star-rating .star {
  display: inline-block;
}

.star-rating .filled {
  color: gold; /* Color for filled stars */
}

.comment-box {
  margin: 20px 0;
}

.comment-box textarea {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  min-height: 100px;
  box-sizing: border-box;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}

.feedback {
  color: #007bff;
  cursor: pointer;
  margin-top: 10px;
  text-decoration: underline;
}

.feedback:hover {
  opacity: 0.8;
}
</style>
