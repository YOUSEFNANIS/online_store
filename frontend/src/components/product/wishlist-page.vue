<template>
  <div class="wl-page">
    <h1>{{ $t('wishlist.title') }}</h1>
    <p v-if="failed" class="state error" role="alert">{{ $t('wishlist.failed') }}</p>
    <p v-else-if="!loaded" class="state" role="status">{{ $t('wishlist.loading') }}</p>
    <div v-else-if="!products.length" class="empty">
      <p>{{ $t('wishlist.empty') }}</p>
      <router-link to="/products" class="btn btn-primary">{{ $t('wishlist.browse') }}</router-link>
    </div>
    <template v-else>
      <ul class="grid">
        <li v-for="p in products" :key="p.id"><product-card :product="p" /></li>
      </ul>
      <div v-if="pages > 1" class="pager">
        <button type="button" :disabled="page <= 1" @click="load(page - 1)">{{ $t('storefront.prev') }}</button>
        <span>{{ $t('storefront.pageOf', { page, total: pages }) }}</span>
        <button type="button" :disabled="page >= pages" @click="load(page + 1)">{{ $t('storefront.next') }}</button>
      </div>
    </template>
  </div>
</template>

<script>
import api from '@/services/api';
import ProductCard from './product-card.vue';
import { useWishlistStore } from '@/stores/wishlist';

export default {
  name: 'WishlistPage',
  components: { ProductCard },
  data() { return { products: [], page: 1, pages: 1, loaded: false, failed: false } },
  computed: { saved() { return useWishlistStore().ids } },
  watch: {
    // Un-hearting a card removes it from this page right away.
    saved(ids) { this.products = this.products.filter((p) => ids.includes(p.id)) },
  },
  mounted() { this.load(1) },
  methods: {
    async load(page) {
      try {
        const { data } = await api.get('/core/wishlist/', { params: { page } })
        this.products = data.results
        this.page = page
        this.pages = data.total_pages || 1
        this.failed = false
      } catch (e) {
        this.failed = true
      }
      this.loaded = true
    },
  },
}
</script>

<style scoped>
.wl-page { display: block; width: min(1100px, 92%); height: auto; margin: 130px auto 2rem; }
h1 { margin: 0 0 1.25rem; font-size: 1.5rem; font-weight: 700; color: var(--color-text); }
.state { margin: 0; color: var(--color-text-muted); }
.state.error { color: var(--color-error); }
.empty { padding: 2rem; text-align: center; color: var(--color-text-muted); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); }
.grid { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 1rem; }
.pager { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-top: 1.5rem; font-size: 0.9rem; color: var(--color-text-muted); }
.pager button { padding: 0.4rem 1rem; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); cursor: pointer; }
.pager button:disabled { opacity: 0.5; cursor: not-allowed; }
@media (max-width: 480px) { .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.75rem; } }
</style>
