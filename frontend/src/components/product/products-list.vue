<template>
  <div class="products-page">
    <load-component v-if="!hasLoaded" />
    <section v-else class="catalog" :class="{ busy: loading }">
      <div class="layout">
        <aside class="sidebar" :class="{ open: showSidebar }">
          <div class="sidebar-head">
            <h2><SlidersHorizontal :size="16" /> {{ $t('productsList.filters') }}</h2>
            <button v-if="activeFilters" type="button" class="link-btn" @click="resetFilters">{{ $t('productsList.clearAll') }}</button>
          </div>

          <div class="group">
            <button type="button" class="group-title" @click="open.price = !open.price">
              {{ $t('productsList.priceGroup') }}
              <ChevronDown :size="16" :class="{ flip: open.price }" />
            </button>
            <div v-show="open.price" class="group-body">
              <ul class="quick">
                <li v-for="r in priceRanges" :key="r.label">
                  <label>
                    <input type="radio" name="range" :checked="isRange(r)" @change="setRange(r)" />
                    {{ r.label }}
                  </label>
                </li>
              </ul>
              <form class="price-row" @submit.prevent="applyFilters">
                <input v-model="filters.min_price" type="number" min="0" step="0.01" :placeholder="$t('productsList.min')" :aria-label="$t('productsList.minPrice')" />
                <span>–</span>
                <input v-model="filters.max_price" type="number" min="0" step="0.01" :placeholder="$t('productsList.max')" :aria-label="$t('productsList.maxPrice')" />
                <button type="submit" class="btn-ok">{{ $t('productsList.ok') }}</button>
              </form>
            </div>
          </div>

          <div class="group">
            <button type="button" class="group-title" @click="open.avail = !open.avail">
              {{ $t('productsList.availability') }}
              <ChevronDown :size="16" :class="{ flip: open.avail }" />
            </button>
            <div v-show="open.avail" class="group-body">
              <label class="check">
                <input v-model="filters.in_stock" type="checkbox" @change="applyFilters" />
                <span>{{ $t('productsList.inStockOnly') }}</span>
              </label>
            </div>
          </div>
          <div v-if="catalog.categories.length" class="group">
            <button type="button" class="group-title" @click="open.cat = !open.cat">
              {{ $t('catalog.category') }}
              <ChevronDown :size="16" :class="{ flip: open.cat }" />
            </button>
            <div v-show="open.cat" class="group-body">
              <ul class="quick">
                <li>
                  <label><input v-model="filters.category" type="radio" name="cat" value="" @change="applyFilters" /> {{ $t('catalog.allCategories') }}</label>
                </li>
                <li v-for="c in catalog.categories" :key="c.id">
                  <label><input v-model="filters.category" type="radio" name="cat" :value="c.id" @change="applyFilters" /> {{ catalog.nameOf(c, $i18n.locale) }}</label>
                </li>
              </ul>
            </div>
          </div>
        </aside>

        <div class="results">
          <div class="toolbar">
            <div class="toolbar-left">
              <button type="button" class="filter-toggle" @click="showSidebar = !showSidebar">
                <SlidersHorizontal :size="16" /> {{ $t('productsList.filters') }}<span v-if="activeFilters" class="badge">{{ activeFilters }}</span>
              </button>
              <p class="count">
                <strong>{{ total }}</strong> {{ $t('productsList.productsCount', total) }}<template v-if="searchTerm"> {{ $t('productsList.forQuery', { query: searchTerm }) }}</template>
              </p>
            </div>
            <div class="toolbar-right">
              <label class="sort">
                <span>{{ $t('productsList.sortBy') }}</span>
                <select v-model="filters.ordering" @change="applyFilters">
                  <option value="-id">{{ $t('productsList.sort.newest') }}</option>
                  <option value="price">{{ $t('productsList.sort.priceAsc') }}</option>
                  <option value="-price">{{ $t('productsList.sort.priceDesc') }}</option>
                  <option value="name">{{ $t('productsList.sort.nameAsc') }}</option>
                  <option value="-name">{{ $t('productsList.sort.nameDesc') }}</option>
                </select>
              </label>
              <div class="view-toggle" role="group" :aria-label="$t('productsList.view')">
                <button type="button" :class="{ on: view === 'grid' }" :aria-label="$t('productsList.gridView')" @click="view = 'grid'"><LayoutGrid :size="18" /></button>
                <button type="button" :class="{ on: view === 'list' }" :aria-label="$t('productsList.listView')" @click="view = 'list'"><List :size="18" /></button>
              </div>
            </div>
          </div>

          <div v-if="chips.length" class="chips">
            <button v-for="c in chips" :key="c.key" type="button" class="chip" @click="c.clear()">
              {{ c.label }} <X :size="12" />
            </button>
            <button type="button" class="link-btn" @click="resetFilters">{{ $t('productsList.clearAll') }}</button>
          </div>

      <div v-if="products.length" class="products-grid" :class="{ list: view === 'list' }">
        <router-link
          v-for="product in products"
          :key="product.id"
          :to="`/products/${product.id}`"
          class="product-card"
        >
          <div class="thumb-wrap">
            <img
              v-if="thumb(product) && !failed[product.id]"
              :src="thumb(product)"
              :alt="product.name"
              class="product-thumbnail"
              loading="lazy"
              @error="failed[product.id] = true"
            />
            <div v-else class="thumb-placeholder" aria-hidden="true">
              <ImageOff :size="36" :stroke-width="1.5" />
            </div>
            <wishlist-heart :product-id="product.id" class="heart-pos" />
          </div>
          <div class="product-info">
            <h2 class="product-name" :title="product.name">{{ product.name }}</h2>
            <p class="product-price">
              {{ formatPrice(product.price) }} <span class="currency">{{ $t('productsList.currency') }}</span>
            </p>
            <star-rating v-if="product.rating_count" :value="product.rating_avg || 0" :count="product.rating_count" />
          </div>
        </router-link>
      </div>

      <div v-else class="empty-state">
        <PackageSearch :size="48" :stroke-width="1.5" />
        <h2>{{ $t('productsList.emptyTitle') }}</h2>
        <p>{{ $t('productsList.emptyText') }}</p>
      </div>

      <nav v-if="totalPages > 1" class="pagination" :aria-label="$t('productsList.pagination')">
        <button
          class="pagination-btn nav"
          :disabled="currentPage <= 1"
          :aria-label="$t('productsList.prevPage')"
          @click="setPageParam(currentPage - 1)"
        >
          <ChevronLeft :size="18" class="dir-icon" />
        </button>
        <button
          v-for="i in visiblePages"
          :key="i.key"
          :class="['pagination-btn', { active: i.n === currentPage, gap: i.gap }]"
          :disabled="i.gap"
          :aria-current="i.n === currentPage ? 'page' : null"
          @click="setPageParam(i.n)"
        >
          {{ i.gap ? '…' : i.n }}
        </button>
        <button
          class="pagination-btn nav"
          :disabled="currentPage >= totalPages"
          :aria-label="$t('productsList.nextPage')"
          @click="setPageParam(currentPage + 1)"
        >
          <ChevronRight :size="18" class="dir-icon" />
        </button>
      </nav>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import api from '@/services/api';
import { scrollToTarget } from '@/services/smooth-scroll';
import loadComponent from '../helperComponents/load-component.vue';
import WishlistHeart from '../helperComponents/wishlist-heart.vue';
import { useCatalogStore } from '@/stores/catalog';
import StarRating from '@/components/helperComponents/star-rating.vue';
import { ImageOff, PackageSearch, ChevronLeft, ChevronRight, X, SlidersHorizontal, ChevronDown, LayoutGrid, List } from '@lucide/vue';

const defaultFilters = () => ({ ordering: '-id', min_price: '', max_price: '', in_stock: false, category: '' });

export default {
  components: { loadComponent, WishlistHeart, StarRating, ImageOff, PackageSearch, ChevronLeft, ChevronRight, X, SlidersHorizontal, ChevronDown, LayoutGrid, List },

  data() {
    return {
      products: [],
      loading: false,
      hasLoaded: false,
      totalPages: 0,
      currentPage: 1,
      searchTerm: null,
      failed: {},
      debounceTimer: null,
      filters: { ...defaultFilters(), category: Number(this.$route.query.category) || '' },
      total: 0,
      view: 'grid',
      showSidebar: false,
      open: { price: true, avail: true, cat: true },
    };
  },

  computed: {
    catalog() { return useCatalogStore(); },
    priceRanges() {
      return [
        { label: this.$t('productsList.ranges.any'), min: '', max: '' },
        { label: this.$t('productsList.ranges.under', { n: 50 }), min: '', max: 50 },
        { label: this.$t('productsList.ranges.between', { a: 50, b: 150 }), min: 50, max: 150 },
        { label: this.$t('productsList.ranges.between', { a: 150, b: 500 }), min: 150, max: 500 },
        { label: this.$t('productsList.ranges.over', { n: 500 }), min: 500, max: '' },
      ];
    },
    activeFilters() {
      const f = this.filters;
      const has = (v) => v !== '' && v !== null;
      return (has(f.min_price) || has(f.max_price) ? 1 : 0) + (f.in_stock ? 1 : 0) + (has(f.category) ? 1 : 0);
    },
    chips() {
      const f = this.filters;
      const out = [];
      const has = (v) => v !== '' && v !== null;
      if (has(f.min_price) || has(f.max_price)) {
        const label = has(f.min_price) && has(f.max_price) ? this.$t('productsList.chipRange', { min: f.min_price, max: f.max_price })
          : has(f.min_price) ? this.$t('productsList.chipFrom', { min: f.min_price }) : this.$t('productsList.chipUpTo', { max: f.max_price });
        out.push({ key: 'price', label, clear: () => { f.min_price = ''; f.max_price = ''; this.applyFilters(); } });
      }
      if (has(f.category)) {
        const c = this.catalog.categories.find((x) => x.id === f.category);
        if (c) out.push({ key: 'category', label: this.catalog.nameOf(c, this.$i18n.locale), clear: () => { f.category = ''; this.applyFilters(); } });
      }
      if (f.in_stock) out.push({ key: 'stock', label: this.$t('productsList.chipInStock'), clear: () => { f.in_stock = false; this.applyFilters(); } });
      return out;
    },
    // 1 … 4 5 [6] 7 8 … 13
    visiblePages() {
      const total = this.totalPages;
      const cur = this.currentPage;
      const pages = [];
      for (let n = 1; n <= total; n++) {
        if (n === 1 || n === total || Math.abs(n - cur) <= 1) {
          pages.push({ n, key: n, gap: false });
        } else if (pages[pages.length - 1] && !pages[pages.length - 1].gap) {
          pages.push({ n: 0, key: `gap-${n}`, gap: true });
        }
      }
      return pages;
    },
  },

  watch: {
    // Landing-page category links land here with ?category=<id>.
    '$route.query.category'(category) {
      const id = Number(category) || '';
      if (id === this.filters.category) return;
      this.filters.category = id;
      this.applyFilters();
    },
    '$route.query.searchQuery': {
      immediate: true,
      handler(searchQuery) {
        if (!searchQuery) {
          this.searchTerm = null;
          this.currentPage = 1;
          this.getdata();
        } else {
          this.debouncedSearch(searchQuery);
        }
      },
    },
  },

  created() {
    this.catalog.load();
  },

  beforeUnmount() {
    clearTimeout(this.debounceTimer);
  },

  methods: {
    thumb(product) {
      return product.images?.[0]?.image || null;
    },
    formatPrice(price) {
      const n = Number(price);
      return Number.isNaN(n) ? price : new Intl.NumberFormat(this.$i18n.locale + '-u-nu-latn', { minimumFractionDigits: 2, maximumFractionDigits: 2, useGrouping: false }).format(n);
    },
    debouncedSearch(searchQuery) {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.searchTerm = searchQuery;
        this.currentPage = 1;
        this.getdata();
      }, 300);
    },
    isRange(r) {
      return String(this.filters.min_price) === String(r.min) && String(this.filters.max_price) === String(r.max);
    },
    setRange(r) {
      this.filters.min_price = r.min;
      this.filters.max_price = r.max;
      this.applyFilters();
    },
    applyFilters() {
      this.currentPage = 1;
      this.getdata();
    },
    resetFilters() {
      this.filters = defaultFilters();
      this.applyFilters();
    },
    setPageParam(navPage) {
      if (navPage < 1 || navPage > this.totalPages || navPage === this.currentPage) return;
      this.currentPage = navPage;
      this.getdata();
      scrollToTarget(0);
    },
    async getdata() {
      this.loading = true;
      try {
        const params = { page: this.currentPage };
        if (this.searchTerm) params.search = this.searchTerm;
        const f = this.filters;
        params.ordering = f.ordering;
        if (f.min_price !== '' && f.min_price !== null) params.min_price = f.min_price;
        if (f.max_price !== '' && f.max_price !== null) params.max_price = f.max_price;
        if (f.in_stock) params.in_stock = true;
        if (f.category !== '' && f.category !== null) params.category = f.category;
        const response = await api.get('/core/products/', { params });
        this.totalPages = response.data['total_pages'];
        this.total = response.data['count'] ?? response.data['results'].length;
        this.products = response.data['results'];
        this.failed = {};
      } catch (error) {
        console.log(error);
      } finally {
        this.loading = false;
        this.hasLoaded = true;
      }
    },
  },
};
</script>

<style scoped>
.thumb-wrap { position: relative; }
.heart-pos { position: absolute; top: 8px; inset-inline-end: 8px; z-index: 1; }
/* override global .page-content flex layout applied to router-view root */
.products-page {
  display: block;
  width: 100%;
  height: auto;
  /* Reserve the final viewport footprint while the catalog request is pending.
     This keeps the footer below the fold instead of shifting it after products render. */
  min-height: calc(100vh - var(--app-bar-h) - 70px);
  min-height: calc(100svh - var(--app-bar-h) - 70px);
  margin-top: calc(var(--app-bar-h) + 70px); /* fixed navbar + side menu (50px) + gap */
  padding-bottom: 96px; /* clear the floating chat button */
}

.catalog {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 20px;
}

.catalog.busy .products-grid { opacity: 0.5; pointer-events: none; transition: opacity 0.15s ease; }

.layout { display: grid; grid-template-columns: 260px 1fr; gap: 24px; align-items: start; }
.sidebar {
  position: sticky; top: calc(var(--app-bar-live-h, var(--app-bar-h)) + 66px);
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius-lg); padding: 4px 16px 8px; box-shadow: var(--shadow-sm);
}
.sidebar-head { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--color-border); }
[dir=rtl] .dir-icon { transform: scaleX(-1); }
.sidebar-head h2 { margin: 0; font-size: 1rem; display: flex; align-items: center; gap: 8px; }
.link-btn { background: none; border: none; color: var(--color-primary); font-weight: 600; cursor: pointer; padding: 0; font-size: 0.85rem; }
.link-btn:hover { text-decoration: underline; }
.group { border-bottom: 1px solid var(--color-border); padding: 4px 0; }
.group:last-child { border-bottom: none; }
.group-title {
  width: 100%; display: flex; justify-content: space-between; align-items: center;
  background: none; border: none; padding: 12px 0; font-weight: 700; font-size: 0.95rem;
  color: var(--color-text); cursor: pointer;
}
.group-title svg { transition: transform 0.2s ease; }
.group-title svg.flip { transform: rotate(180deg); }
.group-body { padding-bottom: 12px; }
.quick { list-style: none; margin: 0 0 12px; padding: 0; display: flex; flex-direction: column; gap: 8px; }
.quick label, .check { display: flex; align-items: center; gap: 8px; cursor: pointer; font-weight: 500; color: var(--color-text); }
.quick input, .check input { width: 16px; height: 16px; accent-color: var(--color-primary); }
.price-row { display: flex; align-items: center; gap: 6px; }
.price-row input {
  width: 0; flex: 1; min-width: 0; height: 34px; padding: 0 8px;
  border: 1px solid var(--color-border); border-radius: var(--radius-sm); font: inherit; background: var(--color-surface); color: var(--color-text);
}
.price-row input:focus { outline: none; border-color: var(--color-primary); box-shadow: var(--focus-ring); }
.btn-ok {
  height: 34px; padding: 0 12px; border-radius: 999px; cursor: pointer; font-weight: 700;
  background: var(--color-surface); color: var(--color-text); border: 1px solid var(--color-text);
}
.btn-ok:hover { background: var(--color-text); color: #fff; }

.results { min-width: 0; }
.toolbar {
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;
  padding: 10px 16px; margin-bottom: 14px;
  background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg);
}
.toolbar-left, .toolbar-right { display: flex; align-items: center; gap: 14px; }
.count { margin: 0; color: var(--color-text-muted); }
.count strong { color: var(--color-text); }
.sort { display: flex; align-items: center; gap: 8px; color: var(--color-text-muted); font-size: 0.9rem; }
.sort select {
  height: 36px; padding: 0 10px; border: 1px solid var(--color-border); border-radius: var(--radius-md);
  background: var(--color-surface); color: var(--color-text); font: inherit; font-weight: 600;
}
.sort select:focus { outline: none; border-color: var(--color-primary); box-shadow: var(--focus-ring); }
.view-toggle { display: inline-flex; border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }
.view-toggle button { width: 38px; height: 34px; display: grid; place-items: center; background: var(--color-surface); border: none; color: var(--color-text-muted); cursor: pointer; }
.view-toggle button.on { background: var(--color-primary-soft); color: var(--color-primary); }
.filter-toggle { display: none; align-items: center; gap: 6px; height: 36px; padding: 0 12px; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); font-weight: 600; cursor: pointer; }
.badge { background: var(--color-primary); color: #fff; border-radius: 999px; font-size: 0.7rem; padding: 1px 6px; }

.chips { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-bottom: 16px; }
.chip {
  display: inline-flex; align-items: center; gap: 6px; padding: 5px 10px; border-radius: 999px; cursor: pointer;
  background: var(--color-primary-soft); color: var(--color-primary); border: 1px solid transparent; font-weight: 600; font-size: 0.85rem;
}
.chip:hover { border-color: var(--color-primary); }

@media (max-width: 860px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { display: none; position: static; }
  .sidebar.open { display: block; }
  .filter-toggle { display: inline-flex; }
  .sort span { display: none; }
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
}

.products-grid.list { grid-template-columns: 1fr; }
.products-grid.list .product-card { flex-direction: row; }
.products-grid.list .thumb-wrap { width: 180px; flex-shrink: 0; aspect-ratio: 1 / 1; }
.products-grid.list .product-info { display: flex; flex-direction: column; justify-content: center; flex: 1; min-width: 0; }
.products-grid.list .product-name { font-size: 1.1rem; }

.product-card {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  color: var(--color-text);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.product-card:hover,
.product-card:focus-visible {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-primary);
  color: var(--color-text);
  outline: none;
}
.product-card:focus-visible { box-shadow: var(--focus-ring); }

.thumb-wrap {
  position: relative;
  aspect-ratio: 1 / 1;
  background: var(--color-bg);
  overflow: hidden;
}
.product-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.35s ease;
}
.product-card:hover .product-thumbnail { transform: scale(1.05); }
.thumb-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  background: linear-gradient(135deg, var(--color-bg), var(--color-primary-soft));
}

.product-info { padding: 14px 16px 16px; text-align: start; }
.product-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.product-price {
  margin: 6px 0 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-primary);
}
.currency { font-size: 0.8rem; font-weight: 600; color: var(--color-text-muted); }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 64px 16px;
  text-align: center;
  color: var(--color-text-muted);
}
.empty-state h2 { margin: 8px 0 0; color: var(--color-text); font-size: 1.25rem; }
.empty-state p { margin: 0; }

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin: 36px 0 0;
  padding: 0;
}
.pagination-btn {
  width: auto;
  height: 40px;
  min-width: 40px;
  padding: 0 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
  font-weight: 600;
  cursor: pointer;
  transition: border-color var(--transition), color var(--transition), background var(--transition);
}
.pagination-btn:hover:not(:disabled):not(.active) {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: var(--color-primary-soft);
}
.pagination-btn:focus-visible { outline: none; box-shadow: var(--focus-ring); }
.pagination-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}
.pagination-btn:disabled { cursor: default; opacity: 0.45; }
.pagination-btn.gap { border-color: transparent; background: transparent; opacity: 1; color: var(--color-text-muted); }

@media (max-width: 600px) {
  .catalog { padding: 0 12px; }
  .products-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .product-info { padding: 10px 12px 12px; }
  .product-name { font-size: 0.92rem; }
  .product-price { font-size: 1rem; }
}
</style>
