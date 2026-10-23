<template>
  <div>
  <div class="app-bar">
    <market-header
      :user="headerUser"
      :cart-count="cartCount"
      :locale="$i18n.locale"
      :categories="catalog.categories"
      @search="onSearch"
      @update:locale="changeLocale"
      @logout="LogOut"
      @open-cart="openCart"
      @help="openHelp"
    />
    <nav v-if="tab !== '/'" class="side-menu">
      

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
    <show-cart v-if="showCart" ref="cartContainer" @close="closeCart"></show-cart>
</div>
</template>

<script>
import { useRoleStore } from '@/stores/role'
import { useWishlistStore } from '@/stores/wishlist'
import { useCatalogStore } from '@/stores/catalog'
import { setLocale } from '@/i18n'
import api, { API_URL } from '@/services/api';
import { Settings, Package2, CirclePlus, List, MessageSquare, Store, Heart, Wallet, Boxes } from '@lucide/vue';
import MarketHeader from './market-header.vue';

export default {
  name: "Navbar",
  emits: ['search'],
  components: { MarketHeader, Settings, Package2, CirclePlus, List, MessageSquare, Store, Heart, Wallet, Boxes },
  beforeUnmount() {
    document.removeEventListener('click', this.handleCartOutsideClick);
    window.removeEventListener('messages-read', this.fetchUnread);
    window.removeEventListener('cart-updated', this.fetchCartCount);
    clearInterval(this.unreadTimer);
  },
  mounted() {
    document.addEventListener('click', this.handleCartOutsideClick);
    window.addEventListener('messages-read', this.fetchUnread);
    window.addEventListener('cart-updated', this.fetchCartCount);
    this.fetchUnread();
    this.unreadTimer = setInterval(this.fetchUnread, 60000);
    this.catalog.load();
    this.retrieveData();
    this.fetchCartCount();
  },
  watch: {
    role() {
      this.fetchUnread();
      this.retrieveData();
      this.fetchCartCount();
    },
  },
  computed: {
    roleStore() {
      return useRoleStore()
    },
    catalog() {
      return useCatalogStore()
    },
    tab(){
      return this.$route.path
    },
    role() {
      return this.roleStore.role
    },
    headerUser() {
      if (!this.role) return null
      return { ...this.user_data, role: this.role }
    },
  },

  data(){
    return {
      user_data: {},
      unreadMessages: 0,
      unreadTimer: null,
      cartCount: 0,
      showCart: false,
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
    async fetchCartCount() {
      if (this.role !== 'customer') { this.cartCount = 0; return }
      try {
        const res = await api.get('/core/cart/', { skipGlobalError: true })
        const items = res.data[0]?.cart_item_set || []
        this.cartCount = items.reduce((sum, item) => sum + (Number(item.quantity) || 0), 0)
      } catch (e) {
        this.cartCount = 0
      }
    },
    handleCartOutsideClick(event) {
      if (this.showCart && this.$refs.cartContainer?.$el && !this.$refs.cartContainer.$el.contains(event.target)) {
        this.closeCart();
      }
    },
    openCart() {
      if (this.role !== 'customer') { this.$router.push('/login'); return }
      this.showCart = !this.showCart
    },
    closeCart() {
      this.showCart = false
      this.fetchCartCount()
    },
    openHelp() {
      window.dispatchEvent(new CustomEvent('open-help'))
    },
    changeLocale(locale) {
      setLocale(locale)
    },
    onSearch({ query, category }) {
      if (category) {
        this.$router.push({ path: '/products', query: { category, ...(query ? { searchQuery: query } : {}) } })
      } else {
        this.$emit('search', query)
      }
    },
    async LogOut(){
      try{
        this.$router.push('/login')
        await api.post('/signup/logout/')
        this.roleStore.logout()
        useWishlistStore().reset()
      }
      catch(error){
        console.log(error)
      }
    },

    async retrieveData(){
      if (!this.role) { this.user_data = {}; return }
      try {
        const response = await api.get('/signup/get_id/me/')
        this.user_data = {
          name: response.data['first_name'] + ' ' + response.data['last_name'],
          email: response.data['email'],
          avatar: response.data['profile_image'] !== null ? API_URL + response.data['profile_image'] : null,
          balance: response.data['balance'] ?? undefined,
        }
      }
      catch(error){
        console.log(error)
      }
    }
  },
}
</script>

<style scoped>
/* Header plus the side menu, pinned to the top; page offsets come from --app-bar-h / --app-bar-live-h (App.vue). */
.app-bar {
  position: fixed;
  top: 0;
  inset-inline: 0;
  z-index: 1000;
}
.side-menu {
  height: 50px;
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  justify-content: center;
  align-items: center;
  display: flex;
  padding: 0.2%;
  gap: 0.25rem;
  width: 100%;
  overflow: hidden;
  flex-wrap: wrap;
}
.icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}
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
}
</style>
