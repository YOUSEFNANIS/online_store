<template>
  <div>
  <div class="navbar-wrapper">
    <nav class="navbar">
      <!-- Logo Button -->
      <router-link :to="'/'" class="logo-btn" >
        <img 
          src="@/assets/ysfstore.webp" 
          alt="Logo" 
          class="logo-img"
        />
      </router-link>

        <div class="search-container">
          <Search class="search-icon" :size="18" />
          <input 
            type="text" 
            v-model="searchQuery" 
            @keyup.enter="debouncedSearch" 
            placeholder="Search products..."
            class="search-input"
          >
        </div>
        <div class="access-buttons">
          <h1 class="balance" v-if="role==='seller'">total balance: {{user_data.balance}} LYD</h1>

          <router-link :to="'/login'" v-else-if="role===null" class="login-btn">
            login 
            <LogIn class="icon"/>
          </router-link>

          <ShoppingCart v-else-if="role==='customer'" class="cart"  @click.stop="showCart = !showCart"/>
        </div>
        <div>
        <img :src="profile_image" class="profile-image" @click="showMenu = !showMenu"  ref="MenuContainer">
          <div v-if="showMenu" class="dropdown">

            <div class="dropdown-content">
              <h3 class="username">{{user_data.username}}</h3>
              <p class="email">{{user_data.email}}</p>
              <hr />

              <button class="logout" @click="LogOut">
                Logout
                <LogOut/>
              </button>
            </div>
          </div>
        </div>
    </nav>
    <nav class="side-menu">
      

      <router-link v-if="role==='seller'" :class="tab === '/products/create' ? 'menu-item selected' : 'menu-item'" 
          title="Create Product" :to="'/products/create'">
        <CirclePlus class="icon"/>
      </router-link>
      <router-link :to="'/products'" title="Products List" 
      :class="tab === '/products' ? 'menu-item selected' : 'menu-item'">
        <List  class="icon"/>
      </router-link>
      <router-link :to="'/orderslist'"  title="Orders List" 
      :class="tab === '/orderslist' ? 'menu-item selected' : 'menu-item'">
        <Package2 class="icon"/>
      </router-link>
      
      <router-link :to="'/settings'"  title="Settings" 
      :class="tab === '/settings' ? 'menu-item selected' : 'menu-item'">
        <settings class="icon"/>
      </router-link>

    </nav>
  </div>
    <show-cart v-if="showCart" ref="cartContainer" @close="showCart=false"></show-cart>
</div>
</template>

<script>
import { useRoleStore } from '@/stores/role'
import api from '@/services/api';
import { ShoppingCart, Search, LogOut ,Settings, Package2, LogIn, CirclePlus, List } from '@lucide/vue';
import userIcon from '@/assets/user.svg';

export default {
  name: "Navbar",
  components: {ShoppingCart, Search, LogOut, Settings, Package2,CirclePlus , LogIn, List},
  beforeUnmount() {
    document.removeEventListener('click', this.handleCartOutsideClick);
    document.removeEventListener('click', this.handleMenuOutsideClick);
  },
  mounted() {
    document.addEventListener('click', this.handleCartOutsideClick);
    document.addEventListener('click', this.handleMenuOutsideClick);
    this.retrieveData()
    console.log(this.user_data)
  },
  computed: {
    roleStore() {
      return useRoleStore()
    },
    tab(){
      return this.$route.path
    },
    role() {
      return this.roleStore.role
    },
    profile_image(){
      return this.user_data?.profile_image || userIcon;
    }
  },

  data(){
    return {
      user_data: {},
      isOpen: false,
      showCart: false,
      isCustomer: false,
      debounceTimer: null,
      searchQuery: null,
      showMenu: false
    }
  },
  methods: {
    handleCartOutsideClick(event) {
      if (this.showCart && this.$refs.cartContainer?.$el && !this.$refs.cartContainer.$el.contains(event.target)) {
    this.showCart = false;
  }
    },
    handleMenuOutsideClick(event) {
      if (this.isOpen && this.$refs.MenuContainer && !this.$refs.MenuContainer.contains(event.target)) {
        this.isOpen = false;
      }
    },

    debouncedSearch(){
      this.$emit('search', this.searchQuery)
    },
      async LogOut(){
      try{
        this.$router.push('/login')
        const response = await api.post('http://127.0.0.1:8000/signup/logout/')
        this.roleStore.logout()
      }
      catch(error){
        console.log(error)
      }
    },

    async retrieveData(){
      try {
        const url = 'http://127.0.0.1:8000/signup/get_id/me/'
        const response = await api.get(url)
        this.user_data['username'] = response.data['first_name'] + ' ' + response.data['last_name']
        if (response.data['profile_image']!==null){
          this.user_data['profile_image'] = 'http://127.0.0.1:8000'+ response.data['profile_image']
        }
        
        this.user_data['balance'] = response.data['balance']
        this.user_data['email'] = response.data['email']
        console.log(response.data)
      }
      catch(error){
        console.log(error)
      }
    }
      },
  }
  
</script>

<style scoped>
.navbar-wrapper{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;  
}
.navbar {
  position: fixed;
  top: 0;
  height: 60px;
  margin-bottom: 0;
  background-color: #475569;
  justify-content: space-between;
  align-items: center;
  display: inline-flex;
  padding: 0.2%;
  border-radius: 0px;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}
.logo-btn {
  display: flex;
  align-items: center;
  background-color: #000000;
  margin-right: 10%;
  margin-left: 1%;
  font-size: 20px;
  cursor: pointer;
  transition: 0.2s ease;
}
.logo-img {
  height: 3rem;
  width: auto;
}
.search-container {
  display: flex;
  align-items: center;
  margin: auto;
  background-color: #444; 
  opacity: 70%;
  border: 1px solid #6b6b6b; 
  border-radius: 999px;
  padding: 0.5rem 20px; 
  height: 50%;
  width: 95%;
  max-width: 600px;
  overflow: hidden;
  box-sizing: border-box; /* Ensures padding doesn't affect total width */
  transition: border-color 0.2s, box-shadow 0.2s; /* Smooth interactions */
}
.search-container:focus-within {
  border-color: #cdcdcd;
}
.search-icon {
  color: #a0a0a0; 
  margin-right:auto; 
  flex-shrink: 0; /* Prevents icon from squishing */
}
.search-input {
  /* Remove default input styling */
  border: none;
  outline: none;
  background: transparent;
  font-size: 16px;
  color: #ffffff; 
  width: 100%;
  padding: 0; /* Let the container handle padding */
}
.search-input::placeholder {
  color: #cbcbcb; 
  opacity: 1;
}
.access-buttons {
  background-color: #475569;
  max-height: 90%;
  overflow: hidden;
  font-size: 1rem;
  cursor: pointer;
  margin-left: auto;
  align-items: center;
  display: flex;
  justify-content: center;
  color: white;
  transition: all 0.3s ease;
  position: relative;
}
.access-buttons:hover {
  border-color: #ffffff;
  background-color: #404b5c;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}
.access-buttons:active {
  transform: translateY(0) scale(0.96); /* Feels like a real button press */
  background-color: #222222;
}
.access-buttons:focus-visible {
  box-shadow: 0 0 0 4px #475569;
}
.balance {
  font-size: 1rem;
  padding: 0.3rem 1rem;
  border: 0.15rem solid #888888;
}
.cart{
  width: 45%;
  min-width: 30px;
  position: relative;
  height: 90%;
  object-fit: cover;
  padding: 0px 20px;
}
.login-btn {
  display: inline-flex;    /* use inline-flex so it doesn't take 100% width */
  align-items: center;     /* vertical alignment */
  justify-content: center;
  color: #ffffff;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border: 0.15rem solid #888888;
  outline: none;
}
.logo-btn:hover {
  opacity: 0.85;
}
.profile-image{
  position: relative; /* VERY IMPORTANT */
  display: inline-block;
  width: 2.5rem;
  height: 2.5rem;
  background-color:rgb(0, 0, 0);
  border-radius: 50%;
  margin: 0 3rem;
}

.side-menu {
  position: fixed;
  top: 60px; /* SAME as navbar height */
  height: 50px;
  margin: auto;
  background-color: #ffffff;
  justify-content: center;
  align-content: center;
  display: flex;
  padding: 0.2%;
  border-radius: 0px;
  z-index: 100;
  width: 100%;
  overflow: hidden;
  flex-wrap: wrap;
}

.side-menu.is-open {
  transform: translateX(0);
}

.icon{
  width: 10rem;
  margin: 0 0 0 1rem;
}

.menu-item {
  width: fit-content;
  padding: 10px 2vh 10px 2vh; /* Vertical spacing */
  color: rgb(0, 0, 0);
  font-size: 1.3rem;
  justify-content: center;
  cursor: pointer;
  border-radius: 0px;
  transition: all 0.2s ease;
  
}
.selected{
  border-bottom: rgb(0, 187, 255) 4px solid;
  animation: none;
}
/* Optional: Slight hover effect to feel interactive */
.menu-item:hover {
  background-color: #e4e4e4;
  transform: translateY(-5);
}

.dropdown {
  position: absolute;
  top: 100%;
  margin-right: 3%;
  right: 0;
  border: 1px rgb(132, 130, 130) solid;
  z-index: 110;
}

.dropdown-content {
  background: #ffffff;
  padding: 20px;
  width: 220px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}
.email {
  margin: 5px 0 15px;
  font-size: 14px;
}

.username{
  margin: 0 15px 15px 0;
}
hr {
  border: none;
  border-top: 1px solid #888;
  margin: 15px 0;
}

/* Logout */
.logout {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  align-content: center;
  display: flex;
  gap: 10px;
  text-align: left;
  width: 100%;
}
</style>