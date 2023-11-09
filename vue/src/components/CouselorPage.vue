<template>
    <header>
        <button>Back</button>
        <h1>Counselors</h1>
        <button>Filter</button>
    </header>
    <div class="counselors-container">
        <div class="search-bar">
            <input type="text" placeholder="Search" />
        </div>
        <div class="counselor-list">
            <div v-for="counselor in CousProfiles" :key="counselor.name" class="counselor-item">
                <div class="profile-photo">
                    <img :src="counselor.photo" :alt="`Photo of ${counselor.name}`" />
                </div>
                <div class="profile-info">
                    <h2>{{ counselor.name }}</h2>
                    <p>{{ counselor.description }}</p>
                    <div class="rating">
                        <star-rating :rating="counselor.rating"></star-rating>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'CousProfiles',
    data() {
        return {
            searchTerm: '',
            CousProfiles: [
                {
                    name: 'Ada Johnson',
                    photo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwVRR689h-rJJsTMJbY7w4zLP30xxYflNRy6HM164ZjtcJHhgL8su7kCJgBLqdJOx_2D4&usqp=CAU', // Replace with the path to the image
                    description: 'Specializing in youth and family counseling, Ada brings over 20 years of compassionate experience to her practice.',
                    rating: 4.5
                },
                {
                    name: 'Steven Miller',
                    photo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwQQTS4NPqnCGbJPd4x7O_YJNOJ5gH6KkejH3nhVfIhxwwJPHEotjPs0VCpGg-UcybvxM&usqp=CAU', // Replace with the path to the image
                    description: 'With a focus on community well-being, Steven aids diverse groups in overcoming a myriad of challenges.',
                    rating: 4.7
                },
                {
                    name: 'Jenny Smith',
                    photo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfbspSuAlbAFC2RqZweFBTjOF4cWY9gizRbQKEzzLE0QdxIKrV5E-iZipiZxcdYyB7aTU&usqp=CAU', // Replace with the path to the image
                    description: 'Jenny has dedicated more than a decade to social services, empowering her clients to reach personal milestones.',
                    rating: 4.2
                },
                {
                    name: 'Mylene Cruz',
                    photo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxapDwCeVLL0T69nhwV_BgqH9lztNDYQGhCbUVKHMgITKzGDlPsa55HS-6dqUdC8Qt5VU&usqp=CAU', // Replace with the path to the image
                    description: 'Utilizing an array of therapeutic techniques, including Satir Transformational Systemic Therapy, Mylene tailors her approach to each client\'s needs.',
                    rating: 4.8
                },
                {
                    name: 'Raj Patel',
                    photo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZcsVaOflHr9kVRKa_voybME0NUIV0s6Ks8IPWPfwDlDqFB4ZKRE0Pjx1gAUfWVdGzOi4&usqp=CAU', // Replace with the path to the image
                    description: 'Raj brings mindfulness and cognitive-behavioral strategies to help clients cope with anxiety and stress.',
                    rating: 4.6
                },
            ],
        };
    },
    computed: {
        filteredCounselors() {
            return this.counselors.filter((counselor) =>
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

.counselors-container {
    width: 90%;
    max-width: 600px;
    margin: 20px auto;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

@media (max-width: 480px) {
    header h1 {
        font-size: 1.2em;
    }

    .profile-info h2 {
        font-size: 1em;
    }
}
</style>