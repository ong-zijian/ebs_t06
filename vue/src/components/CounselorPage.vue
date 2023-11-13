<template>
    <div>
        <header>
            <button @click="goBack">Back</button>
            <h1>Counselors</h1>
            <button>Filter</button>
        </header>
        <div class="counselors-container">
            <div class="search-bar">
                <input type="text" v-model="searchTerm" placeholder="Search" />
            </div>
            <div class="counselor-list">
                <div v-for="counselor in counsellors" :key="counselor._id" class="counselor-item"
                    @click="goToCounselorProfile(counselor._id)">
                    <div class="profile-photo">
                        <img v-if="counselor && counselor.photo" :src="counselor.photo"
                            :alt="`Photo of ${counselor.name}`" />
                    </div>
                    <div class="profile-info">
                        <h2>{{ counselor.fname }} {{ counselor.lname }}</h2>
                        <p>{{ counselor.description }}</p>
                        <div class="rating">
                            <!-- Replace with your star-rating component -->
                            <span v-for="star in 5" :key="star" class="star"
                                :class="{ 'filled': star <= counselor.rating }">
                                ★
                            </span>
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
    name: 'CounselorProfile',
    data() {
        return {
            searchTerm: '',
            counsellors: [], // Start with an empty array
        };
    },
    created() {
        this.fetchCounselors();
    },
    methods: {
        fetchCounselors() {
            // Make sure the URL matches your Flask route
            axios.get('https://smu-team06-api.ede20ab.kyma.ondemand.com/counsellors')
                .then(response => {
                    // Assume the response data is an array of counselors
                    this.counsellors = response.data;
                    console.log('Counselors:', this.counsellors);
                })
                .catch(error => {
                    console.error('Error fetching counselors:', error);
                    // Handle the error accordingly
                });
        },
        goBack() {
            this.$router.go(-1); // Go back to the previous page
        },
        goToCounselorProfile(id) {
            if (id !== undefined) {
                this.$router.push({ name: 'CounselorProfile', params: { counselorId: id } });
            } else {
                console.error('Error: counselorId is undefined');
            }
        },
    },
    computed: {
        filteredCounselors() {
            return this.counselors.filter(counselor =>
                counselor.name.toLowerCase().includes(this.searchTerm.toLowerCase())
            );
        },
    },
};
</script>

<style>
/* Base styles for the page */
body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    background: #f4f4f4;
    color: #333;
}

/* .counselors-container {
    width: 90%;
    max-width: 600px;
    margin: 20px auto;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
} */

.counselors-container {
  width: 90%;
  margin: 20px auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media screen and (min-width: 768px) {
  .counselors-container {
    width: 95%; /* Adjust the percentage width based on your design */
    margin: 0 auto; /* Center the container */
  }
}



header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #0077cc;
    color: #ffffff;
}

header h1 {
    margin: 0;
    font-size: 1.5em;
}

button {
    background: none;
    border: none;
    color: #fff;
    font-size: 1em;
    cursor: pointer;
}

button:focus {
    outline: none;
}

.search-bar {
    padding: 10px 20px;
}

.search-bar input[type="text"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

.counselor-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.counselor-item {
    display: flex;
    align-items: center;
    border-bottom: 1px solid #eee;
    padding: 20px;
}

.profile-photo img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 15px;
}

.profile-info h2 {
    margin: 0 0 5px 0;
    font-size: 1.2em;
    color: #0077cc;
}

.profile-info p {
    margin: 0;
    font-size: 0.9em;
}

.rating {
    margin-top: 5px;
}

/* Add responsive design */
@media (max-width: 768px) {
    .counselors-container {
        width: 95%;
    }

    .profile-photo img {
        width: 50px;
        height: 50px;
    }
}

.star {
    color: gray;
    /* Color for unfilled star */
}

.filled {
    color: gold;
    /* Color for filled star */
}

@media (max-width: 480px) {
    header h1 {
        font-size: 1.2em;
    }

    .profile-info h2 {
        font-size: 1em;
    }
}
</style>