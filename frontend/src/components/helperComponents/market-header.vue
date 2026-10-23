<template>
  <header ref="root" class="mh" :style="{ '--accent': accent }">
    <!-- Row 1: utility bar (collapses on scroll, hidden below 1024px) -->
    <div class="row row-utility">
      <div class="inner">
        <nav class="utility" :aria-label="$t('nav.header.utilityNav')">
          <span class="deliver">
            <MapPin class="ico-sm" aria-hidden="true" />
            {{ $t('nav.header.deliverTo') }} <strong>{{ $t('nav.header.city') }}</strong>
          </span>
          <router-link to="/orderslist" class="u-link">{{ $t('nav.header.trackOrder') }}</router-link>
          <button type="button" class="u-link" @click="$emit('help')">{{ $t('nav.header.helpCenter') }}</button>
        </nav>
        <div class="utility utility-end">
          <router-link to="/signup" class="sell-link">{{ $t('nav.header.sell') }}</router-link>
          <span class="u-divider" aria-hidden="true"></span>
          <button type="button" class="lang-btn" :aria-label="$t('common.switchLanguage')" @click="toggleLocale">
            <svg v-if="locale === 'ar'" class="flag" viewBox="0 0 20 14" aria-hidden="true">
              <rect width="20" height="14" fill="#fff" />
              <g fill="#b22234">
                <rect y="0" width="20" height="2" /><rect y="4" width="20" height="2" />
                <rect y="8" width="20" height="2" /><rect y="12" width="20" height="2" />
              </g>
              <rect width="9" height="8" fill="#3c3b6e" />
            </svg>
            <svg v-else class="flag" viewBox="0 0 20 14" aria-hidden="true">
              <rect width="20" height="3.5" fill="#E70013" />
              <rect y="3.5" width="20" height="7" fill="#000" />
              <rect y="10.5" width="20" height="3.5" fill="#239E46" />
              <circle cx="9.4" cy="7" r="2.2" fill="#fff" />
              <circle cx="10" cy="7" r="1.8" fill="#000" />
              <circle cx="11.6" cy="7" r="0.7" fill="#fff" />
            </svg>
            <span>{{ nextLocale.toUpperCase() }}</span>
            <ChevronDown class="ico-xs" aria-hidden="true" />
          </button>
          <span class="u-divider" aria-hidden="true"></span>
          <span class="currency">{{ $t('common.currency') }}</span>
        </div>
      </div>
    </div>

    <!-- Row 2: logo, search, actions (always visible) -->
    <div class="row row-main">
      <div class="inner main-grid">
        <router-link to="/" class="logo" :aria-label="$t('nav.header.home')">
          <span class="logo-tile" aria-hidden="true"><ShoppingBag class="ico" /></span>
          <span class="wordmark">
            <span class="brand">CJ Bazar</span>
            <span class="tagline">{{ $t('nav.header.tagline') }}</span>
          </span>
        </router-link>

        <form role="search" class="search" @submit.prevent="submitSearch">
          <label class="sr-only" for="mh-search-category">{{ $t('nav.header.categoryLabel') }}</label>
          <select id="mh-search-category" v-model="searchCategory" class="search-cat">
            <option value="">{{ $t('nav.header.allCategories') }}</option>
            <option v-for="c in shownCategories" :key="c.id" :value="c.id">{{ labelOf(c) }}</option>
          </select>
          <label class="sr-only" for="mh-search-input">{{ $t('nav.header.searchLabel') }}</label>
          <input id="mh-search-input" ref="searchInput" v-model="searchQuery" type="search" class="search-input"
            :placeholder="$t('nav.header.searchPlaceholder')" autocomplete="off" />
          <button type="submit" class="search-submit" :aria-label="$t('nav.header.submitSearch')">
            <Search class="ico" aria-hidden="true" />
          </button>
        </form>

        <div class="actions">
          <button type="button" class="act act-mobile" :aria-label="$t('nav.header.searchLabel')" @click="focusSearch">
            <Search class="ico" aria-hidden="true" />
          </button>

          <template v-if="!isSeller">
            <router-link to="/wishlist" class="act act-desktop" :aria-label="$t('nav.header.wishlist')">
              <Heart class="ico" aria-hidden="true" />
              <span class="act-label">{{ $t('nav.header.wishlist') }}</span>
            </router-link>
            <button type="button" class="act"
              :aria-label="cartCount > 0 ? $t('nav.header.cartWithCount', { n: cartCount }) : $t('nav.header.cart')"
              @click.stop="$emit('open-cart')">
              <span class="cart-ico">
                <ShoppingCart class="ico" aria-hidden="true" />
                <span v-if="cartCount > 0" class="badge" aria-hidden="true">{{ cartCount > 99 ? '99+' : cartCount }}</span>
              </span>
              <span class="act-label">{{ $t('nav.header.cart') }}</span>
            </button>
          </template>
          <div v-else-if="user && user.balance !== undefined" class="balance act-desktop">
            <span class="balance-label">{{ $t('nav.balance') }}</span>
            <span class="balance-value">{{ formattedBalance }}</span>
          </div>

          <span class="a-divider act-desktop" aria-hidden="true"></span>

          <template v-if="!user">
            <router-link to="/login" class="login act-desktop">{{ $t('nav.header.login') }}</router-link>
            <router-link to="/signup" class="signup act-desktop">{{ $t('nav.header.signup') }}</router-link>
          </template>
          <div v-else ref="account" class="account act-desktop">
            <button type="button" class="avatar-btn" :aria-label="$t('nav.accountMenu')" aria-haspopup="menu"
              :aria-expanded="accountOpen" @click="accountOpen = !accountOpen">
              <img v-if="user.avatar" :src="user.avatar" alt="" class="avatar" />
              <span v-else class="avatar avatar-initial" aria-hidden="true">{{ initial }}</span>
              <ChevronDown class="ico-xs" aria-hidden="true" />
            </button>
            <div v-if="accountOpen" class="menu-panel account-panel" role="menu">
              <div class="account-head">
                <p class="account-name">{{ user.name }}</p>
                <p v-if="user.email" class="account-email">{{ user.email }}</p>
              </div>
              <router-link to="/orderslist" class="menu-item" role="menuitem" @click="accountOpen = false">
                <Package2 class="ico-sm" aria-hidden="true" />{{ $t('nav.header.orders') }}
              </router-link>
              <router-link v-if="isSeller" to="/dashboard" class="menu-item" role="menuitem" @click="accountOpen = false">
                <Store class="ico-sm" aria-hidden="true" />{{ $t('nav.header.myStore') }}
              </router-link>
              <router-link to="/settings" class="menu-item" role="menuitem" @click="accountOpen = false">
                <Settings class="ico-sm" aria-hidden="true" />{{ $t('nav.header.settings') }}
              </router-link>
              <button type="button" class="menu-item menu-logout" role="menuitem" @click="logout">
                <LogOut class="ico-sm" aria-hidden="true" />{{ $t('nav.header.logout') }}
              </button>
            </div>
          </div>

          <button type="button" class="act act-mobile" :aria-label="$t('nav.header.openMenu')"
            :aria-expanded="drawerOpen" aria-controls="mh-drawer" @click="openDrawer">
            <Menu class="ico" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>

    <!-- Row 3: categories bar (collapses on scroll, scrolls sideways below 1024px, moves into the drawer below 768px) -->
    <div class="row row-cats">
      <nav class="inner cats" :aria-label="$t('nav.header.categoriesNav')">
        <button ref="megaToggle" type="button" class="all-cats" aria-haspopup="true" :aria-expanded="megaOpen"
          aria-controls="mh-mega" @click="megaOpen = !megaOpen">
          <Menu class="ico-sm" aria-hidden="true" />{{ $t('nav.header.allCategories') }}
        </button>
        <router-link to="/products" class="cat cat-highlight">{{ $t('nav.header.allProducts') }}</router-link>
        <router-link v-for="c in shownCategories" :key="c.id" :to="categoryLink(c)" class="cat">{{ labelOf(c) }}</router-link>
        <!-- The store directory is customer-only (router meta requiresCustomer). -->
        <router-link v-if="isCustomer" to="/sellers" class="cat cat-end">
          <List class="ico-sm" aria-hidden="true" />{{ $t('nav.header.browseStores') }}
        </router-link>
      </nav>
    </div>

    <!-- Mega-menu stub -->
    <div v-if="megaOpen" id="mh-mega" ref="mega" class="mega">
      <div class="inner">
        <p class="mega-title">{{ $t('nav.header.shopByCategory') }}</p>
        <ul class="mega-grid">
          <li v-for="c in shownCategories" :key="c.id">
            <router-link :to="categoryLink(c)" class="mega-link" @click="megaOpen = false">{{ labelOf(c) }}</router-link>
          </li>
        </ul>
      </div>
    </div>

    <!-- Mobile drawer -->
    <div v-if="drawerOpen" class="drawer-backdrop" @click="closeDrawer"></div>
    <div v-if="drawerOpen" id="mh-drawer" class="drawer" role="dialog" aria-modal="true"
      :aria-label="$t('nav.header.menu')">
      <div class="drawer-head">
        <span class="brand">CJ Bazar</span>
        <button ref="drawerClose" type="button" class="act" :aria-label="$t('nav.header.closeMenu')" @click="closeDrawer">
          <X class="ico" aria-hidden="true" />
        </button>
      </div>

      <div v-if="!user" class="drawer-auth">
        <router-link to="/login" class="login" @click="closeDrawer">{{ $t('nav.header.login') }}</router-link>
        <router-link to="/signup" class="signup" @click="closeDrawer">{{ $t('nav.header.signup') }}</router-link>
      </div>
      <nav v-else class="drawer-section" :aria-label="$t('nav.accountMenu')">
        <p class="drawer-title">{{ user.name }}</p>
        <router-link to="/orderslist" class="drawer-link" @click="closeDrawer">
          <Package2 class="ico-sm" aria-hidden="true" />{{ $t('nav.header.orders') }}
        </router-link>
        <router-link v-if="isSeller" to="/dashboard" class="drawer-link" @click="closeDrawer">
          <Store class="ico-sm" aria-hidden="true" />{{ $t('nav.header.myStore') }}
        </router-link>
        <router-link v-else to="/wishlist" class="drawer-link" @click="closeDrawer">
          <Heart class="ico-sm" aria-hidden="true" />{{ $t('nav.header.wishlist') }}
        </router-link>
        <router-link to="/settings" class="drawer-link" @click="closeDrawer">
          <Settings class="ico-sm" aria-hidden="true" />{{ $t('nav.header.settings') }}
        </router-link>
        <button type="button" class="drawer-link menu-logout" @click="logout">
          <LogOut class="ico-sm" aria-hidden="true" />{{ $t('nav.header.logout') }}
        </button>
      </nav>

      <nav class="drawer-section" :aria-label="$t('nav.header.categoriesNav')">
        <p class="drawer-title">{{ $t('nav.header.shopByCategory') }}</p>
        <router-link to="/products" class="drawer-link cat-highlight" @click="closeDrawer">{{ $t('nav.header.allProducts') }}</router-link>
        <router-link v-for="c in shownCategories" :key="c.id" :to="categoryLink(c)" class="drawer-link" @click="closeDrawer">
          {{ labelOf(c) }}
        </router-link>
        <router-link v-if="isCustomer" to="/sellers" class="drawer-link" @click="closeDrawer">
          <List class="ico-sm" aria-hidden="true" />{{ $t('nav.header.browseStores') }}
        </router-link>
      </nav>

      <nav class="drawer-section" :aria-label="$t('nav.header.utilityNav')">
        <span class="drawer-link drawer-static">
          <MapPin class="ico-sm" aria-hidden="true" />
          {{ $t('nav.header.deliverTo') }} <strong>{{ $t('nav.header.city') }}</strong>
        </span>
        <router-link to="/orderslist" class="drawer-link" @click="closeDrawer">{{ $t('nav.header.trackOrder') }}</router-link>
        <button type="button" class="drawer-link" @click="closeDrawer(); $emit('help')">{{ $t('nav.header.helpCenter') }}</button>
        <router-link to="/signup" class="drawer-link sell-link" @click="closeDrawer">{{ $t('nav.header.sell') }}</router-link>
        <div class="drawer-row">
          <button type="button" class="lang-btn" :aria-label="$t('common.switchLanguage')" @click="toggleLocale">
            <span>{{ nextLocale.toUpperCase() }}</span>
            <ChevronDown class="ico-xs" aria-hidden="true" />
          </button>
          <span class="currency">{{ $t('common.currency') }}</span>
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
import { MapPin, ChevronDown, ShoppingBag, Search, Heart, ShoppingCart, Menu, X, List, Package2, Store, Settings, LogOut } from '@lucide/vue';

// Rows 1 and 3 collapse past COLLAPSE_AT and come back under EXPAND_AT; the gap stops flicker at the threshold.
const COLLAPSE_AT = 120;
const EXPAND_AT = 40;

export default {
  name: 'MarketHeader',
  components: { MapPin, ChevronDown, ShoppingBag, Search, Heart, ShoppingCart, Menu, X, List, Package2, Store, Settings, LogOut },
  props: {
    accent: { type: String, default: '#2563EB' },
    // { name, email, avatar, role: 'customer' | 'seller', balance }; null when logged out.
    user: { type: Object, default: null },
    cartCount: { type: Number, default: 0 },
    locale: { type: String, default: 'en' },
    // [{ id, name_en, name_ar, product_count }] or [{ id, name }]; product_count 0 hides a category.
    categories: { type: Array, default: () => [] },
  },
  emits: ['search', 'update:locale', 'logout', 'open-cart', 'help'],
  data() {
    return {
      searchQuery: '',
      searchCategory: '',
      accountOpen: false,
      megaOpen: false,
      drawerOpen: false,
    };
  },
  computed: {
    nextLocale() {
      return this.locale === 'ar' ? 'en' : 'ar';
    },
    isSeller() {
      return this.user?.role === 'seller';
    },
    shownCategories() {
      return this.categories.filter((c) => c.product_count === undefined || c.product_count > 0);
    },
    isCustomer() {
      return this.user?.role === 'customer';
    },
    initial() {
      return (this.user?.name || '?').trim().charAt(0).toUpperCase();
    },
    formattedBalance() {
      const b = Number(this.user?.balance);
      if (Number.isNaN(b)) return '— ' + this.$t('common.currency');
      return b.toLocaleString(this.locale === 'ar' ? 'ar-EG' : 'en-US', { maximumFractionDigits: 2 }) + ' ' + this.$t('common.currency');
    },
  },
  watch: {
    $route() {
      this.megaOpen = false;
      this.accountOpen = false;
    },
  },
  mounted() {
    window.addEventListener('scroll', this.onScroll, { passive: true });
    document.addEventListener('pointerdown', this.onOutside);
    document.addEventListener('keydown', this.onKeydown);
    // Publish the live header height so fixed and sticky page elements can sit right under it.
    this.resizeObserver = new ResizeObserver(([entry]) => {
      document.documentElement.style.setProperty('--app-bar-live-h', entry.borderBoxSize[0].blockSize + 'px');
    });
    this.resizeObserver.observe(this.$refs.root);
    this.onScroll();
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.onScroll);
    document.removeEventListener('pointerdown', this.onOutside);
    document.removeEventListener('keydown', this.onKeydown);
    this.resizeObserver.disconnect();
    document.documentElement.style.removeProperty('--app-bar-live-h');
  },
  methods: {
    labelOf(category) {
      return category[`name_${this.locale}`] || category.name_en || category.name;
    },
    categoryLink(category) {
      return { path: '/products', query: { category: category.id } };
    },
    onScroll() {
      const y = window.scrollY;
      const root = this.$refs.root;
      if (!root) return;

      const collapsed = root.classList.contains('is-collapsed');
      if (!collapsed && y > COLLAPSE_AT) {
        root.classList.add('is-collapsed');
        this.megaOpen = false;
      } else if (collapsed && y < EXPAND_AT) {
        root.classList.remove('is-collapsed');
      }
    },
    onOutside(event) {
      if (this.accountOpen && !this.$refs.account?.contains(event.target)) this.accountOpen = false;
      if (this.megaOpen && !this.$refs.mega?.contains(event.target) && !this.$refs.megaToggle?.contains(event.target)) {
        this.megaOpen = false;
      }
    },
    onKeydown(event) {
      if (event.key !== 'Escape') return;
      this.accountOpen = false;
      this.megaOpen = false;
      this.drawerOpen = false;
    },
    submitSearch() {
      this.$emit('search', { query: this.searchQuery.trim(), category: this.searchCategory });
    },
    focusSearch() {
      this.$refs.searchInput.focus();
    },
    toggleLocale() {
      const next = this.nextLocale;
      document.documentElement.lang = next;
      document.documentElement.dir = next === 'ar' ? 'rtl' : 'ltr';
      this.$emit('update:locale', next);
    },
    logout() {
      this.accountOpen = false;
      this.drawerOpen = false;
      this.$emit('logout');
    },
    openDrawer() {
      this.drawerOpen = true;
      this.$nextTick(() => this.$refs.drawerClose?.focus());
    },
    closeDrawer() {
      this.drawerOpen = false;
    },
  },
};
</script>

<style scoped>
.mh {
  --bg: #0B1220;
  --row-divider: #131C2E;
  --outer-border: #1E293B;
  --text: #E2E8F0;
  --muted: #94A3B8;
  --dim: #64748B;
  --surface: #111A2E;
  --surface-border: #243047;
  --raised: #16213A;
  --orange: #F97316;
  --link: #60A5FA;

  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  font-family: 'Inter', var(--font-sans, system-ui), sans-serif;
  color: var(--text);
  background: var(--bg);
  border-block-end: 1px solid var(--outer-border);
}
.mh *, .mh *::before, .mh *::after { box-sizing: border-box; }
/* :where() keeps these resets at zero specificity so component classes always win */
:where(.mh) a { font-weight: inherit; color: inherit; text-decoration: none; }
:where(.mh) button { font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; }
.mh :focus-visible { outline: 2px solid var(--link); outline-offset: 2px; border-radius: 6px; }

.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
.ico { width: 20px; height: 20px; flex-shrink: 0; }
.ico-sm { width: 16px; height: 16px; flex-shrink: 0; }
.ico-xs { width: 12px; height: 12px; flex-shrink: 0; }

.inner {
  max-width: 1440px;
  margin-inline: auto;
  padding-inline: 48px;
  height: 100%;
  display: flex;
  align-items: center;
}
.row + .row { border-block-start: 1px solid var(--row-divider); }

/* Rows 1 and 3 collapse to zero height on scroll */
.row-utility, .row-cats { overflow: hidden; transition: height 0.2s ease, border-color 0.2s ease; }
.row-utility { height: 36px; font-size: 12px; }
.row-cats { height: 47px; font-size: 13px; font-weight: 500; }
.is-collapsed .row-utility, .is-collapsed .row-cats { height: 0; border-color: transparent; }
.is-collapsed .row-main { border-color: transparent; }
@media (prefers-reduced-motion: reduce) {
  .row-utility, .row-cats { transition: none; }
}

/* Row 1 */
.row-utility .inner { justify-content: space-between; }
.utility { display: flex; align-items: center; gap: 20px; color: var(--muted); }
.utility-end { gap: 14px; }
.deliver { display: inline-flex; align-items: center; gap: 6px; }
.deliver strong { color: var(--text); font-weight: 600; }
.u-link:hover { color: var(--text); }
.sell-link { color: var(--link); font-weight: 700; }
.sell-link:hover { text-decoration: underline; }
.u-divider { width: 1px; height: 14px; background: var(--surface-border); }
.lang-btn { display: inline-flex; align-items: center; gap: 6px; font-weight: 600; color: var(--text); }
.flag { width: 18px; height: 12px; border-radius: 2px; flex-shrink: 0; }
.currency { font-weight: 600; color: var(--text); }

/* Row 2 */
.row-main { height: 80px; }
.main-grid {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  grid-template-areas: "logo search actions";
  column-gap: 32px;
}
.logo { grid-area: logo; display: flex; align-items: center; gap: 12px; }
.logo-tile {
  width: 40px; height: 40px; border-radius: 12px;
  display: grid; place-items: center;
  background: var(--accent); color: #fff;
}
.wordmark { display: flex; flex-direction: column; line-height: 1.2; }
.brand { font-size: 19px; font-weight: 700; color: #fff; letter-spacing: -0.01em; }
.tagline { font-size: 11px; color: var(--dim); font-weight: 400; }

.search {
  grid-area: search;
  justify-self: center;
  width: 100%;
  max-width: 760px;
  height: 48px;
  display: flex;
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  overflow: hidden;
}
.search:focus-within { border-color: var(--accent); }
.search :focus-visible { outline: none; }
.search-cat {
  flex: none;
  max-width: 160px;
  padding-inline: 14px 8px;
  font: inherit;
  font-size: 13px;
  color: var(--text);
  background: var(--raised);
  border: 0;
  border-inline-end: 1px solid var(--surface-border);
  cursor: pointer;
}
.search-input {
  flex: 1;
  min-width: 0;
  padding-inline: 14px;
  font: inherit;
  font-size: 14px;
  color: var(--text);
  background: transparent;
  border: 0;
  outline: none;
}
.search-input::placeholder { color: var(--dim); opacity: 1; }
.search-submit {
  flex: none;
  width: 56px;
  display: grid;
  place-items: center;
  background: var(--accent);
  color: #fff;
}
.search-submit:hover { filter: brightness(1.1); }

.actions { grid-area: actions; display: flex; align-items: center; gap: 8px; }
.act {
  min-width: 44px; height: 44px;
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding-inline: 10px;
  border-radius: 10px;
  font-size: 13px; font-weight: 500;
}
.act:hover { background: var(--raised); }
.act-mobile { display: none; }
.cart-ico { position: relative; display: inline-flex; }
.badge {
  position: absolute;
  top: -8px;
  inset-inline-end: -10px;
  min-width: 18px; height: 18px;
  padding-inline: 5px;
  border-radius: 999px;
  font-size: 11px; font-weight: 700; line-height: 18px; text-align: center;
  color: #fff; background: var(--orange);
  border: 2px solid var(--bg);
  box-sizing: content-box;
}
.a-divider { width: 1px; height: 28px; background: var(--surface-border); margin-inline: 4px; }
.login {
  height: 44px; display: inline-flex; align-items: center;
  padding-inline: 12px; font-size: 14px; font-weight: 600; border-radius: 10px;
}
.login:hover { background: var(--raised); }
.signup {
  height: 40px; display: inline-flex; align-items: center; justify-content: center;
  padding-inline: 20px; border-radius: 8px;
  font-size: 14px; font-weight: 600; color: #fff; background: var(--accent);
}
.signup:hover { filter: brightness(1.1); }

.balance { display: flex; flex-direction: column; align-items: flex-end; line-height: 1.2; padding-inline: 8px; }
.balance-label { font-size: 11px; color: var(--dim); text-transform: uppercase; letter-spacing: 0.04em; }
.balance-value { font-size: 14px; font-weight: 700; font-variant-numeric: tabular-nums; }

.account { position: relative; }
.avatar-btn { height: 44px; display: inline-flex; align-items: center; gap: 6px; padding-inline: 4px; border-radius: 10px; }
.avatar-btn:hover { background: var(--raised); }
.avatar { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 1px solid var(--surface-border); }
.avatar-initial { display: grid; place-items: center; background: var(--raised); font-weight: 700; font-size: 14px; }

.menu-panel {
  position: absolute;
  top: calc(100% + 8px);
  inset-inline-end: 0;
  width: 240px;
  padding: 8px;
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
  z-index: 10;
}
.account-head { padding: 8px 10px 10px; margin-block-end: 6px; border-block-end: 1px solid var(--surface-border); }
.account-name { margin: 0; font-size: 14px; font-weight: 600; color: #fff; }
.account-email { margin: 2px 0 0; font-size: 12px; color: var(--muted); overflow: hidden; text-overflow: ellipsis; }
.menu-item {
  width: 100%;
  min-height: 40px;
  display: flex; align-items: center; gap: 10px;
  padding-inline: 10px;
  font-size: 14px; font-weight: 500; text-align: start;
  border-radius: 8px;
}
.menu-item:hover { background: var(--raised); }
.menu-logout:hover { color: #FCA5A5; }

/* Row 3 */
.cats { gap: 22px; white-space: nowrap; overflow-x: auto; scrollbar-width: none; }
.cats::-webkit-scrollbar { display: none; }
.all-cats, .cat, .cat-end { flex-shrink: 0; }
.all-cats {
  height: 33px;
  display: inline-flex; align-items: center; gap: 8px;
  padding-inline: 12px;
  background: var(--raised);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  font-weight: 600;
}
.all-cats:hover, .all-cats[aria-expanded="true"] { border-color: var(--accent); }
.cat { color: var(--text); }
.cat:hover { color: #fff; text-decoration: underline; text-underline-offset: 4px; }
.cat-highlight { color: var(--orange); font-weight: 700; }
.cat-end { margin-inline-start: auto; display: inline-flex; align-items: center; gap: 6px; color: var(--muted); }

/* Mega-menu stub */
.mega {
  position: absolute;
  top: 100%;
  inset-inline: 0;
  padding-block: 20px 24px;
  background: var(--surface);
  border-block: 1px solid var(--outer-border);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.45);
}
.mega .inner { display: block; height: auto; }
.mega-title { margin: 0 0 12px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--dim); }
.mega-grid { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 4px 16px; }
.mega-link { display: block; padding: 8px 10px; border-radius: 8px; font-size: 14px; font-weight: 500; }
.mega-link:hover { background: var(--raised); }

/* Drawer */
.drawer-backdrop { position: fixed; inset: 0; background: rgba(2, 6, 23, 0.6); z-index: 1; }
.drawer {
  position: fixed;
  inset-block: 0;
  inset-inline-start: 0;
  width: min(320px, 86vw);
  overflow-y: auto;
  padding-block-end: 24px;
  background: var(--bg);
  border-inline-end: 1px solid var(--outer-border);
  z-index: 2;
}
.drawer-head {
  height: 64px; display: flex; align-items: center; justify-content: space-between;
  padding-inline: 16px 8px; border-block-end: 1px solid var(--row-divider);
}
.drawer-auth { display: flex; gap: 8px; padding: 16px; border-block-end: 1px solid var(--row-divider); }
.drawer-auth .login, .drawer-auth .signup { flex: 1; justify-content: center; }
.drawer-auth .login { border: 1px solid var(--surface-border); }
.drawer-section { padding: 12px 8px; border-block-end: 1px solid var(--row-divider); }
.drawer-title { margin: 4px 10px 8px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--dim); }
.drawer-link {
  width: 100%; min-height: 44px;
  display: flex; align-items: center; gap: 10px;
  padding-inline: 10px; border-radius: 8px;
  font-size: 14px; font-weight: 500; text-align: start;
}
.drawer-link:hover { background: var(--raised); }
.drawer-static { color: var(--muted); }
.drawer-static:hover { background: none; }
.drawer-static strong { color: var(--text); }
.drawer-row { display: flex; align-items: center; justify-content: space-between; min-height: 44px; padding-inline: 10px; }

/* < 1024px: no utility bar, icon-only actions, sideways-scrolling categories */
@media (max-width: 1023px) {
  .inner { padding-inline: 24px; }
  .row-utility { display: none; }
  .row + .row-main { border-block-start: 0; }
  .act-label { display: none; }
  .main-grid { column-gap: 20px; }
  .tagline { display: none; }
  .cat-end { margin-inline-start: 8px; }
}

/* < 768px: logo + icons, search on its own row, categories move into the drawer */
@media (max-width: 767px) {
  .inner { padding-inline: 16px; }
  .row-main {
    height: auto;
    background-image: linear-gradient(var(--row-divider), var(--row-divider));
    background-size: 100% 1px;
    background-position: 0 64px;
    background-repeat: no-repeat;
  }
  .main-grid {
    grid-template-columns: minmax(0, 1fr) auto;
    grid-template-rows: 64px 61px;
    grid-template-areas: "logo actions" "search search";
    column-gap: 12px;
  }
  .search { align-self: center; height: 44px; margin-block-start: 1px; }
  .search-cat { display: none; }
  .actions { gap: 2px; }
  .act-desktop { display: none !important; }
  .act-mobile { display: inline-flex; }
  .act { padding-inline: 0; }
  .row-cats, .mega { display: none; }
}
/* The drawer docks on the start edge (right side in RTL) and only exists on phones. */
@media (min-width: 768px) {
  .drawer, .drawer-backdrop { display: none; }
}
</style>
