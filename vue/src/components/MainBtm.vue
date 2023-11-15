<template>
  <div class="navigation-bar">
    <div class="nav-item">
      <router-link to="/home" exact active-class="active">
        <img src="https://cdn-icons-png.flaticon.com/512/25/25694.png" alt="Home" />
      </router-link>
    </div>
    <div class="nav-item">
      <router-link to="/chatBot" active-class="active">
        <img src="https://static.thenounproject.com/png/1913797-200.png" alt="Chat" />
      </router-link>
    </div>
    <div class="nav-item plus-icon" v-if="$route.path !== '/CreateJournal'">
      <router-link to="/CreateJournal" class="plus">+</router-link>
    </div>
    <div class="nav-item">
      <router-link to="/CounselorPage" active-class="active">
        <img src="https://cdn-icons-png.flaticon.com/512/55/55281.png" alt="Calendar" />
      </router-link>
    </div>
    <div class="nav-item">
      <router-link to="/profile" active-class="active">
        <img src="https://cdn-icons-png.flaticon.com/512/3106/3106773.png" alt="Profile" />
      </router-link>
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
  position: fixed;
  /* Set the position to fixed */
  bottom: 0;
  /* Position it at the bottom of the viewport */
  width: 100%;
  /* Occupy full width */
}

/* Remove relative positioning from .navigation-bar */
.nav-item {
  flex: 1;
  text-align: center;
}

.nav-item img {
  width: 24px;
  height: 24px;
}

.plus-icon {
  position: absolute;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
}

.plus {
  width: 40px;
  height: 40px;
  background-color: #4CAF50;
  border-radius: 50%;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  text-decoration: none;
}

/* Style for active link */
.active img {
  background-color: #4CAF50; 
  border-radius: 50%; 
  padding: 4px;
}

.plus-icon .active .plus {
  border: 2px solid #4CAF50;
}

</style>
