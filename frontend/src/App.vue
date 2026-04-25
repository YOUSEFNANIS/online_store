<template>
    <div>
      <nav-bar v-if="showNavBar" @search="getSearchQueryResults"></nav-bar>
      <transition name="slide-fade">
      <div v-if="banner" class="success-banner">
          saved !
      </div>
      </transition>
      <router-view class="page-content"  @saved="showBanner"></router-view>
      
      <chat-bot></chat-bot>
    </div>
</template>

<script>
import chatBot from './chat-bot.vue'
import NavBar from './components/helperComponents/nav-bar.vue';
import ShowCart from './show-cart.vue';

export default {
  components: {
    chatBot,
    NavBar,
    ShowCart
  },
  data(){
    return {
      banner: false,
    }
  },
  computed:{
    showNavBar(){
      if (this.$route.path === '/login' || this.$route.path === '/signup'){
          return false
      }
      else if (this.$route.path === '/landingpage'){
          return false
      }
      else {
        return true
      }
    },
  },
  methods: {
    
    showBanner(){
      this.banner= true
      setTimeout(() => {
        this.banner = false;
      }, 2500);
    },
    getSearchQueryResults(results){
      this.$router.push({
      path: '/products',
      query: { searchQuery: results}
  })
    }
  }
}
</script>


<style>
* {
  border-radius: 9px;
}
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  background: #f4f4f4;
}
a {
  color: black;
  text-decoration: none;
  font-weight: bold;
  font-size: inherit;
}
.page-content {
  display: flex;
  flex-wrap: wrap;
  width: 90%;
  height: 90%;
  position: relative;
  margin: 5% 0 0 0;/* same as navbar height */
}

.success-banner {
  position: fixed;
  top: 9.6%; /* below navbar */
  left: 0;
  width: 100%;
  background-color: #83fd8d;
  color: #0a3d0f;
  text-align: center;
  padding: 18px 0;
  font-size: 20px;
  z-index: 100;
  border-radius: 6px;
}

.remove-btn{
  border:none;
  background:none;
  font-size:18px;
  cursor:pointer;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

/* Enter from slightly below the navbar */
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px); /* small offset below navbar */
}
.slide-fade-enter-to {
  opacity: 1;
  transform: translateY(0);
}

/* Leave by sliding up but still below navbar */
.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.btn{
  background:black;
  color:white;
  font-size:24px;
  padding:10px 25px;
  border:none;
  cursor:pointer;
  box-shadow:0 3px 5px rgba(0,0,0,0.3);
}

.btn:hover{
  opacity:0.9;
  transform: translateY(-1px);
}
.pagination {
  display: flex;
  margin: auto;
  padding-bottom: 25px;
  gap: 10px;
  align-items: center;
}

.pagination-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background-color: #e5e5e5;
  color: #333;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
}

.pagination-btn:hover {
  background-color: #d4d4d4;
}

.pagination-btn.active {
  background-color: #3c5d8c; /* blue/purple like your image */
  color: white;
}
</style>