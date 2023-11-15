<template>
    <div id="app" class="documentation-style">
        <header class="header">
            <h1>Stay Positive & Destress</h1>
            <p>Welcome to your guide on staying positive and managing stress.</p>
        </header>

        <main>
            <section id="destress-tips">
                <h2>Destress Tips</h2>
                <img :src="destressTipsImage" alt="Destress Tips Poster" class="section-poster">
                <p>Discover various techniques to reduce stress, such as deep breathing exercises, meditation, and
                    mindfulness practices.</p>
                <!-- Additional content -->
                <img>
            </section>

            <section id="positive-thinking">
                <h2>Positive Thinking</h2>
                <img :src="positivityTipsImage" alt="Positive Tips Poster" class="section-poster">
                <p>Explore ways to cultivate a positive mindset with affirmations, success stories, and motivational quotes.
                </p>
                <!-- Additional content -->
            </section>

            <section id="relaxing-activities">
                <h2>Relaxing Activities</h2>
                <img :src="relaxingTipsImage" alt="Relaxing Tips Poster" class="section-poster">
                <p>Find activities that help you relax and unwind, like yoga, reading, or listening to calming music.</p>
                <!-- Additional content -->
            </section>

            <section id="interactive-section" style="padding-bottom:10px;">
                <h2>Interactive Fun</h2>
                <img :src="interactiveTipsImage" alt="Interactive Tips Poster" class="section-poster">
                <p>Engage with interactive elements such as mood trackers, quick games, or a positivity journal.</p>
                <!-- Interactive elements -->
            </section> 
        </main>
    </div>
</template>
  
<script>
export default {
  name: 'App',
  data() {
    return {
        destressTipsImage: require('@/assets/destress.png'),
        positivityTipsImage: require('@/assets/positivity.jpg'),
        relaxingTipsImage: require('@/assets/relaxing.png'),
        interactiveTipsImage: require('@/assets/interactive.png')
      // Define other image paths similarly
    }
  }
}
</script>
  
<style scoped>
.documentation-style {
    /* font-family: 'Arial', sans-serif; */
    line-height: 1.6;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.section-poster {
  width: 100%;
  height: auto;
  margin-bottom: 20px; /* Add some space between the image and text */
}

.header {
    text-align: center;
    /* or left, if preferred */
    padding: 20px;
    background-color: #0056b3;
    /* A calming blue */
    color: white;
    /* Ensures readability */
    border-bottom: 1px solid #ddd;
}

.header h1 {
    font-size: 2em;
    /* Larger size for main title */
    font-weight: bold;
    /* Bold for emphasis */
    margin-bottom: 0.25em;
    /* Adjust spacing to your preference */
}

.header p {
    font-size: 1em;
    /* Subtitle size */
    font-weight: lighter;
    /* Lighter weight for the subtitle */
    margin-top: 0;
    /* Remove margin from the top of the subtitle */
}


h1 {
    margin-bottom: 0.5em;
}

h2 {
    color: #0056b3;
    margin-top: 1em;
}

section {
    margin-bottom: 2em;
}

</style>
  