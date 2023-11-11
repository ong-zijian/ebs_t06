<template>
  <div class="navigation-bar">
    <div class="nav-item">
      <router-link to="/">
        <img src="https://cdn-icons-png.flaticon.com/512/25/25694.png" alt="Home" />
      </router-link>
    </div>
    <div class="nav-item">
      <router-link to="/chatBot">
        <img
          src="https://w7.pngwing.com/pngs/983/399/png-transparent-computer-icons-internet-bot-robot-robot-thumbnail.png"
          alt="Chat" />
      </router-link>
    </div>
    <div class="nav-item plus-icon">
      <!-- The Plus button is aligned with the other items but has a margin-top to offset it upwards -->
      <router-link to="/CreateJournal" class="plus">+</router-link>
    </div>
    <div class="nav-item">
      <router-link to="/CouselorPage">
        <img src="https://cdn-icons-png.flaticon.com/512/55/55281.png" alt="Calendar" />
      </router-link>
    </div>
    <div class="nav-item">
      <img src="https://cdn-icons-png.flaticon.com/512/3106/3106773.png" alt="Profile" />
    </div>
  </div>
</template>

<style>
.navigation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  background-color: #f2f2f2;
  /* Background color of the bar */
  position: relative;
}

.nav-item {
  flex: 1;
  text-align: center;
}

.nav-item img {
  width: 24px;
  /* Size of icons */
  height: 24px;
}

.placeholder {
  /* This element is invisible and only used to balance the space */
  visibility: hidden;
}

.plus-icon {
  position: absolute;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
  /* Position the plus button halfway across the screen, then shift it back half its own width to center it */
}

.plus {
  width: 40px;
  /* Size of plus icon */
  height: 40px;
  background-color: #4CAF50;
  /* Color of plus button */
  border-radius: 50%;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  /* Size of plus symbol */
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  /* Optional shadow for depth */
  text-decoration: none;
}</style>
