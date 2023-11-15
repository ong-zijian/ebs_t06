<template>
  <div id="app" class="help-guide">
    <header class="header">
      <h1>Managing Panic Attacks</h1>
      <p>A step-by-step guide to help you through the moments of panic.</p>
    </header>

    <main class="content">
      <section id="understanding-attacks">
        <h2>Understanding Panic Attacks</h2>
        <p>Learn what panic attacks are and why they happen.</p>
        <!-- You can add a <img> tag here with an image that helps understanding -->
        <img :src="panicAttackTipsImage" alt="Panic attack Tips Poster" class="section-poster">
      </section>

      <section id="immediate-steps">
        <h2>Immediate Steps</h2>
        <p>Follow these steps as soon as you feel a panic attack coming on.</p>
        <ol>
          <li>Find a safe place.</li>
          <li>Focus on deep breathing.</li>
          <li>Acknowledge and accept the attack.</li>
          <li>Close your eyes and visualize calmness.</li>
          <li>Use muscle relaxation techniques.</li>
        </ol>
      </section>

      <section id="long-term-management">
        <h2>Long-Term Management</h2>
        <p>Strategies for managing anxiety and reducing the frequency of panic attacks in the long term.</p>
        <ul>
          <li>Regular exercise and healthy diet.</li>
          <li>Consistent sleep schedule.</li>
          <li>Mindfulness and meditation.</li>
          <li>Professional therapy and counseling.</li>
        </ul>
      </section>

      <section id="when-to-seek-help">
        <h2>When to Seek Help</h2>
        <p>If panic attacks frequently disrupt your life, it may be time to seek professional help. Contact a healthcare
          provider if you find yourself in this situation.</p>
      </section>
    </main>

    <footer class="footer">
      <p>Remember, you're not alone. Help is available.</p>
    </footer>
  </div>
</template>
  
<script>
export default {
  name: 'App',
  data() {
    return {
      panicAttackTipsImage: require('@/assets/panicattack.png'),
      // Define other image paths similarly
    }
  }
}
</script>
  
<style scoped>
.help-guide {
  /* font-family: 'Arial', sans-serif; */
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


.content h2 {
  color: #0056b3;
  margin-bottom: 10px;
}

.content p,
.content ol,
.content ul {
  margin-bottom: 10px;
}

.footer {
  text-align: center;
  margin-top: 20px;
  padding: 10px;
  background-color: #f4f4f4;
  margin-bottom: 50px; /* This creates space below the footer */
}
</style>
  