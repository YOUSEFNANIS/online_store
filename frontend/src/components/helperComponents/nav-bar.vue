<template>
  <div>
  <div class="navbar-wrapper">
    <nav class="navbar">
      <!-- Logo Button -->
      <router-link :to="'/'" class="logo-btn" >
        <img 
          src="@/assets/logo.svg" 
          :alt="$t('nav.logoAlt')" 
          class="logo-img"
        />
      </router-link>

        <div class="search-container">
          <Search class="search-icon" :size="18" />
          <input 
            type="text" 
            v-model="searchQuery" 
            @keyup.enter="debouncedSearch" 
            :placeholder="$t('nav.searchPlaceholder')"
            class="search-input"
          >
        </div>
        <div class="access-buttons">
          <lang-switcher class="nav-lang" />
          <div class="balance" v-if="role==='seller'" :aria-label="$t('nav.accountBalance')">
            <span class="balance-label">{{ $t('nav.balance') }}</span>
            <span class="balance-value">{{ formattedBalance }}</span>
          </div>

          <router-link :to="'/login'" v-else-if="role===null" class="login-btn">
            {{ $t('nav.login') }}
            <LogIn class="icon"/>
          </router-link>

          <ShoppingCart v-else-if="role==='customer'" class="cart"  @click.stop="showCart = !showCart"/>
        </div>
        <div>
        <button type="button" class="profile-btn" :aria-label="$t('nav.accountMenu')" :aria-expanded="showMenu"
            @click.stop="showMenu = !showMenu" ref="MenuContainer">
            <img :src="profile_image" class="profile-image" alt="">
          </button>
          <div v-if="showMenu" class="dropdown">

            <div class="dropdown-content">
              <h3 class="username">{{user_data.username}}</h3>
              <p class="email">{{user_data.email}}</p>
              <hr />

              <router-link to="/settings" class="dropdown-item" @click="showMenu = false">
                <User class="icon" aria-hidden="true"/>
                {{ $t('nav.profile') }}
              </router-link>
              <router-link to="/terms" class="dropdown-item" @click="showMenu = false">
                <FileText class="icon" aria-hidden="true"/>
                {{ $t('nav.terms') }}
              </router-link>
              <hr />

              <button class="logout" @click="LogOut">
                {{ $t('nav.logout') }}
                <LogOut/>
              </button>
            </div>
          </div>
        </div>
    </nav>
    <nav class="side-menu">
      

      <router-link v-if="role==='seller'" :class="tab === '/products/create' ? 'menu-item selected' : 'menu-item'" 
          :title="$t('nav.createProduct')" :to="'/products/create'">
        <CirclePlus class="icon" aria-hidden="true"/>
        <span class="menu-label">{{ $t('nav.newProduct') }}</span>
      </router-link>
      <router-link :to="'/products'" :title="$t('nav.productsList')" 
      :class="tab === '/products' ? 'menu-item selected' : 'menu-item'">
        <List class="icon" aria-hidden="true"/>
        <span class="menu-label">{{ $t('nav.products') }}</span>
      </router-link>
      <router-link v-if="role==='seller'" :to="'/inventory'" :title="$t('sellerTools.inventoryTitle')"
      :class="tab === '/inventory' ? 'menu-item selected' : 'menu-item'">
        <Boxes class="icon" aria-hidden="true"/>
        <span class="menu-label">{{ $t('sellerTools.inventoryNav') }}</span>
      </router-link>
      <router-link v-if="role==='seller'" :to="'/earnings'" :title="$t('earnings.title')"
      :class="tab === '/earnings' ? 'menu-item selected' : 'menu-item'">
        <Wallet class="icon" aria-hidden="true"/>
        <span class="menu-label">{{ $t('earnings.nav') }}</span>
      </router-link>
      <router-link v-if="role==='customer'" :to="'/wishlist'" :title="$t('wishlist.title')"
      :class="tab === '/wishlist' ? 'menu-item selected' : 'menu-item'">
        <Heart class="icon" aria-hidden="true"/>
        <span class="menu-label">{{ $t('wishlist.nav') }}</span>
      </router-link>
      <router-link v-if="role==='customer'" :to="'/sellers'" :title="$t('nav.sellersList')"
      :class="tab === '/sellers' ? 'menu-item selected' : 'menu-item'">
        <Store class="icon" aria-hidden="true"/>
        <span class="menu-label">{{ $t('nav.sellers') }}</span>
      </router-link>
      <router-link :to="'/orderslist'"  :title="$t('nav.ordersList')" 
      :class="tab === '/orderslist' ? 'menu-item selected' : 'menu-item'">
        <Package2 class="icon" aria-hidden="true"/>
        <span class="menu-label">{{ $t('nav.orders') }}</span>
      </router-link>
      
      <router-link v-if="role" :to="'/messages'" :title="$t('messages.title')"
      :class="tab === '/messages' ? 'menu-item selected' : 'menu-item'">
        <span class="msg-icon-wrap">
          <MessageSquare class="icon" aria-hidden="true"/>
          <span v-if="unreadMessages" class="msg-badge">{{ unreadMessages > 99 ? '99+' : unreadMessages }}</span>
        </span>
        <span class="menu-label">{{ $t('messages.navLabel') }}</span>
      </router-link>

      <router-link :to="'/settings'"  :title="$t('nav.settings')" 
      :class="tab === '/settings' ? 'menu-item selected' : 'menu-item'">
        <Settings class="icon" aria-hidden="true"/>
        <span class="menu-label">{{ $t('nav.settings') }}</span>
      </router-link>

    </nav>
  </div>
    <show-cart v-if="showCart" ref="cartContainer" @close="showCart=false"></show-cart>
</div>
</template>

<script>
import { useRoleStore } from '@/stores/role'
import { useWishlistStore } from '@/stores/wishlist'
import api, { API_URL } from '@/services/api';
import { ShoppingCart, Search, LogOut ,Settings, Package2, LogIn, CirclePlus, List, User, FileText, MessageSquare, Store, Heart, Wallet, Boxes } from '@lucide/vue';
import LangSwitcher from './lang-switcher.vue';
import userIcon from '@/assets/user.svg';

export default {
  name: "Navbar",
  components: {LangSwitcher, ShoppingCart, Search, LogOut, Settings, Package2,CirclePlus , LogIn, List, User, FileText, MessageSquare, Store, Heart, Wallet, Boxes},
  beforeUnmount() {
    document.removeEventListener('click', this.handleCartOutsideClick);
    document.removeEventListener('click', this.handleMenuOutsideClick);
    window.removeEventListener('messages-read', this.fetchUnread);
    clearInterval(this.unreadTimer);
  },
  mounted() {
    document.addEventListener('click', this.handleCartOutsideClick);
    document.addEventListener('click', this.handleMenuOutsideClick);
    window.addEventListener('messages-read', this.fetchUnread);
    this.fetchUnread();
    this.unreadTimer = setInterval(this.fetchUnread, 60000);
    this.retrieveData()
    console.log(this.user_data)
  },
  watch: {
    role() { this.fetchUnread() },
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
    formattedBalance(){
      const b = Number(this.user_data?.balance)
      if (this.user_data?.balance === undefined || Number.isNaN(b)) return '— ' + this.$t('common.currency')
      return b.toLocaleString(this.$i18n.locale === 'ar' ? 'ar-EG' : 'en-US', { maximumFractionDigits: 2 }) + ' ' + this.$t('common.currency')
    },
    profile_image(){
      return this.user_data?.profile_image || userIcon;
    }
  },

  data(){
    return {
      user_data: {},
      unreadMessages: 0,
      unreadTimer: null,
      isOpen: false,
      showCart: false,
      isCustomer: false,
      debounceTimer: null,
      searchQuery: null,
      showMenu: false
    }
  },
  methods: {
    async fetchUnread() {
      if (!this.role) { this.unreadMessages = 0; return }
      try {
        const res = await api.get('messaging/conversations/unread-count/', { skipGlobalError: true })
        this.unreadMessages = res.data.unread
      } catch (e) {
        this.unreadMessages = 0
      }
    },
    handleCartOutsideClick(event) {
      if (this.showCart && this.$refs.cartContainer?.$el && !this.$refs.cartContainer.$el.contains(event.target)) {
    this.showCart = false;
  }
    },
    handleMenuOutsideClick(event) {
      if (this.showMenu && this.$refs.MenuContainer && !this.$refs.MenuContainer.contains(event.target)) {
        this.showMenu = false;
      }
    },

    debouncedSearch(){
      this.$emit('search', this.searchQuery)
    },
      async LogOut(){
      try{
        this.$router.push('/login')
        const response = await api.post('/signup/logout/')
        this.roleStore.logout()
        useWishlistStore().reset()
      }
      catch(error){
        console.log(error)
      }
    },

    async retrieveData(){
      try {
        const url = '/signup/get_id/me/'
        const response = await api.get(url)
        this.user_data['username'] = response.data['first_name'] + ' ' + response.data['last_name']
        if (response.data['profile_image']!==null){
          this.user_data['profile_image'] = API_URL + response.data['profile_image']
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
.navbar-wrapper {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.navbar {
  position: fixed;
  top: 0;
  inset-inline-start: 0;
  width: 100%;
  height: 60px;
  background-color: var(--color-nav);
  justify-content: space-between;
  align-items: center;
  display: inline-flex;
  padding: 0 0.5%;
  z-index: 1000;
  box-shadow: var(--shadow-sm);
}
.logo-btn {
  display: flex;
  align-items: center;
  margin-inline-end: 5%;
  margin-inline-start: 1%;
  border-radius: var(--radius-sm);
  transition: opacity var(--transition);
}
.logo-btn:hover { opacity: 0.85; }
.logo-img {
  height: 2.5rem;
  width: auto;
}
.search-container {
  display: flex;
  align-items: center;
  margin: auto;
  background-color: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 999px;
  padding: 0 16px;
  height: 40px;
  width: 95%;
  max-width: 600px;
  overflow: hidden;
  transition: border-color var(--transition), box-shadow var(--transition);
}
.search-container:focus-within {
  border-color: #fff;
  box-shadow: var(--focus-ring);
}
.search-icon {
  color: #fff;
  margin-inline-end: 10px;
  flex-shrink: 0;
}
.search-input,
.search-input:focus {
  border: none;
  outline: none;
  box-shadow: none;
  background: transparent;
  font-size: 1rem;
  color: #fff;
  width: 100%;
  padding: 0;
}
.search-input::placeholder {
  color: #D1D5DB;
  opacity: 1;
}
.access-buttons {
  font-size: 1rem;
  cursor: pointer;
  margin-inline-start: auto;
  gap: 0.75rem;
  align-items: center;
  display: flex;
  justify-content: center;
  color: #fff;
  position: relative;
}
.balance {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: end;
  line-height: 1.2;
  margin: 0;
  padding: 0.3rem 0.9rem;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.08);
  white-space: nowrap;
}
.balance-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #D1D5DB;
}
.balance-value {
  font-size: 1rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
.cart {
  width: 45%;
  min-width: 30px;
  position: relative;
  height: 90%;
  object-fit: cover;
  padding: 8px 20px;
  color: #fff;
  border-radius: var(--radius-sm);
  transition: background var(--transition);
}
.cart:hover { background: rgba(255, 255, 255, 0.12); }
.login-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 40px;
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: var(--radius-sm);
  transition: background var(--transition);
}
.login-btn:hover { background: rgba(255, 255, 255, 0.12); color: #fff; }
.profile-btn {
  display: block;
  padding: 0;
  margin-block: 0;
  margin-inline: 1rem 1.25rem;
  border: none;
  background: none;
  border-radius: 50%;
}
.profile-image {
  display: block;
  width: 2.5rem;
  height: 2.5rem;
  padding: 0.35rem;
  background-color: var(--color-border);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  object-fit: cover;
  transition: border-color var(--transition);
}
.profile-btn:hover .profile-image { border-color: #fff; }
.navbar :focus-visible { box-shadow: 0 0 0 3px #fff; }

.side-menu {
  position: fixed;
  top: 60px;
  height: 50px;
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  justify-content: center;
  align-items: center;
  display: flex;
  padding: 0.2%;
  z-index: 100;
  width: 100%;
  overflow: hidden;
  flex-wrap: wrap;
}
.icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}
.login-btn .icon { margin-inline-start: 2px; }
.side-menu { gap: 0.25rem; }
.menu-item {
  width: fit-content;
  min-height: 48px;
  padding: 0 1rem;
  gap: 0.5rem;
  display: flex;
  align-items: center;
  color: var(--color-text-muted);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}
.selected {
  color: var(--color-primary);
  border-bottom: 3px solid var(--color-primary);
}
.msg-icon-wrap { position: relative; display: inline-flex; }
.msg-badge {
  position: absolute; top: -6px; inset-inline-end: -8px; min-width: 16px; padding: 0 4px;
  font-size: 0.65rem; font-weight: 700; line-height: 16px; text-align: center;
  color: #fff; background: var(--color-error); border-radius: 999px;
}
.menu-item:hover { background-color: var(--color-bg); color: var(--color-primary); }
.selected { color: var(--color-primary); }
@media (max-width: 640px) {
  .menu-label { display: none; }
  .menu-item { padding: 0 1.25rem; }
  .balance-label { display: none; }
  .profile-btn { margin: 0 0.5rem; }
  .logo-btn { margin-inline-end: 2%; }
}

.dropdown {
  position: absolute;
  top: 100%;
  margin-inline-end: 3%;
  inset-inline-end: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  z-index: 110;
}
.dropdown-content {
  background: var(--color-surface);
  color: var(--color-text);
  padding: 16px;
  width: 220px;
}
.email {
  margin: 4px 0 12px;
  font-size: 0.875rem;
  color: var(--color-text-muted);
}
.username { margin: 0; font-size: 1rem; }
hr {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: 12px 0;
}
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 40px;
  padding: 0 4px;
  color: var(--color-text);
  font-size: 1rem;
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: background var(--transition), color var(--transition);
}
.dropdown-item:hover { background: var(--color-bg); color: var(--color-primary); }
.logout {
  background: none;
  border: none;
  color: var(--color-text);
  font-size: 1rem;
  min-height: 40px;
  align-items: center;
  display: flex;
  gap: 10px;
  text-align: start;
  width: 100%;
  border-radius: var(--radius-sm);
  transition: background var(--transition), color var(--transition);
}
.logout:hover { background: var(--color-error-soft); color: var(--color-error); }
</style>
