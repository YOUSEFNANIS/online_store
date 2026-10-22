<template>
    <div>
      <nav-bar v-if="showNavBar" @search="getSearchQueryResults"></nav-bar>
      <transition name="slide-fade">
      <div v-if="banner" class="success-banner">
          {{ $t('app.saved') }}
      </div>
      </transition>
      <transition name="slide-fade">
      <div v-if="errorMessage" class="error-banner" role="alert" @click="errorMessage = ''">
          {{ errorMessage }}
          <button class="error-close" :aria-label="$t('app.dismiss')" @click.stop="errorMessage = ''">&times;</button>
      </div>
      </transition>
      <router-view class="page-content"  @saved="showBanner"></router-view>
      
      <verify-banner v-if="showNavBar"></verify-banner>
      <chat-bot></chat-bot>
    </div>
</template>

<script>
import chatBot from './chat-bot.vue'
import NavBar from './components/helperComponents/nav-bar.vue';
import VerifyBanner from './components/users/verify-banner.vue';
import ShowCart from './show-cart.vue';
import { useRoleStore } from '@/stores/role'

export default {
  components: {
    chatBot,
    NavBar,
    VerifyBanner,
    ShowCart
  },
  data(){
    return {
      banner: false,
      errorMessage: '',
      errorTimer: null,
    }
  },
  mounted(){
    window.addEventListener('api-error', this.showError)
  },
  beforeUnmount(){
    window.removeEventListener('api-error', this.showError)
  },
  computed:{
    roleStore() {
      return useRoleStore()
    },
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
    
    showError(event){
      this.errorMessage = event.detail
      clearTimeout(this.errorTimer)
      this.errorTimer = setTimeout(() => { this.errorMessage = '' }, 5000)
    },
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
a {
  text-decoration: none;
  font-weight: 600;
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

.success-banner,
.error-banner {
  position: fixed;
  top: 9.6%; /* below navbar */
  inset-inline-start: 0;
  width: 100%;
  text-align: center;
  padding: 14px 0;
  font-size: 1rem;
  font-weight: 600;
  z-index: 100;
  box-shadow: var(--shadow-md);
}
.success-banner {
  background-color: var(--color-success-soft);
  color: #14532D;
  border-bottom: 2px solid var(--color-success);
}
.error-banner {
  background-color: var(--color-error-soft);
  color: #991B1B;
  border-bottom: 2px solid var(--color-error);
  cursor: pointer;
}
.error-close {
  position: absolute;
  inset-inline-end: 16px;
  top: 6px;
  border: none;
  background: none;
  font-size: 26px;
  color: inherit;
  cursor: pointer;
}

.remove-btn{
  border:none;
  background:none;
  font-size:18px;
  cursor:pointer;
  color: var(--color-text-muted);
}
.remove-btn:hover { color: var(--color-error); }

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.slide-fade-enter-to,
.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.pagination {
  display: flex;
  margin: auto;
  padding-bottom: 25px;
  gap: 8px;
  align-items: center;
}
.pagination-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background-color: var(--color-surface);
  color: var(--color-text);
  font-weight: 600;
  transition: var(--transition);
}
.pagination-btn:hover:not(:disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}
.pagination-btn.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}
</style>
