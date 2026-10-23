<template>
  <div class="store-page">
    <router-link to="/sellers" class="back">← {{ $t('storefront.back') }}</router-link>

    <p v-if="failed" class="state error" role="alert">{{ $t('storefront.failed') }}</p>
    <p v-else-if="!seller" class="state" role="status">{{ $t('storefront.loading') }}</p>
    <template v-else>
      <header class="store-head">
        <img v-if="seller.store_image && !logoBroken" :src="seller.store_image" alt="" class="logo" @error="logoBroken = true" />
        <span v-else class="logo fallback" aria-hidden="true">{{ (seller.store_name || '?').charAt(0).toUpperCase() }}</span>
        <div>
          <h1>{{ seller.store_name }}</h1>
          <p class="meta">{{ $t('storefront.productsCount', { count: seller.product_count }) }}</p>
          <star-rating :value="seller.rating_avg || 0" :count="seller.rating_count || 0" :empty-label="$t('reviews.noRatings')" />
          <div class="store-actions">
            <button v-if="role !== 'seller'" type="button" class="msg-btn" @click="contactSeller">{{ $t('messages.contactSeller') }}</button>
            <report-button :seller="seller.id" class="store-report" />
          </div>
        </div>
      </header>

      <h2 class="section-title">{{ $t('storefront.products') }}</h2>
      <p v-if="productsLoaded && !products.length" class="state">{{ $t('storefront.empty') }}</p>
      <ul v-else class="grid">
        <li v-for="p in products" :key="p.id">
          <router-link :to="'/products/' + p.id" class="product">
            <div class="thumb">
              <img v-if="p.images?.[0]?.image && !imgBroken[p.id]" :src="p.images[0].image" :alt="p.name" loading="lazy" @error="imgBroken[p.id] = true" />
            </div>
            <h3 :title="p.name">{{ p.name }}</h3>
            <star-rating v-if="p.rating_count" :value="p.rating_avg || 0" :count="p.rating_count" />
            <p class="price">{{ formatPrice(p.price) }} <span>{{ $t('storefront.currency') }}</span></p>
            <p v-if="p.inventory <= 0" class="oos">{{ $t('storefront.outOfStock') }}</p>
          </router-link>
        </li>
      </ul>

      <div v-if="pages > 1" class="pager">
        <button type="button" :disabled="page <= 1" @click="loadProducts(page - 1)">{{ $t('storefront.prev') }}</button>
        <span>{{ $t('storefront.pageOf', { page, total: pages }) }}</span>
        <button type="button" :disabled="page >= pages" @click="loadProducts(page + 1)">{{ $t('storefront.next') }}</button>
      </div>
    </template>

    <contact-seller-modal v-if="showContact" :seller="seller" @close="showContact = false" @sent="onSent" @error="showToast('error', $event)" />

    <transition name="toast">
      <div v-if="toast.show" class="toast" :class="toast.type" role="status" aria-live="polite">{{ toast.message }}</div>
    </transition>
  </div>
</template>

<script>
import api from '@/services/api';
import StarRating from '@/components/helperComponents/star-rating.vue';
import ReportButton from '@/components/helperComponents/report-button.vue';
import ContactSellerModal from '@/components/messages/contact-seller-modal.vue';
import { useRoleStore } from '@/stores/role';

export default {
  name: 'SellerStorefront',
  components: { StarRating, ReportButton, ContactSellerModal },
  computed: {
    role() { return useRoleStore().role },
  },
  data() {
    return { seller: null, products: [], page: 1, pages: 1, productsLoaded: false, failed: false, logoBroken: false, imgBroken: {}, showContact: false, toast: { show: false, type: 'success', message: '' }, toastTimer: null }
  },
  watch: {
    '$route.params.sellerId': { immediate: true, handler() { this.init() } },
  },
  beforeUnmount() { clearTimeout(this.toastTimer) },
  methods: {
    async init() {
      this.seller = null
      this.failed = false
      this.logoBroken = false
      try {
        const response = await api.get(`/signup/sellers/${this.$route.params.sellerId}/`)
        this.seller = response.data
      } catch (error) {
        this.failed = true
        return
      }
      await this.loadProducts(1)
    },
    async loadProducts(page) {
      try {
        const response = await api.get('/core/products/', { params: { seller: this.$route.params.sellerId, page } })
        this.products = response.data.results
        this.page = page
        this.pages = response.data.total_pages || 1
        this.imgBroken = {}
      } catch (error) {
        this.failed = true
      }
      this.productsLoaded = true
    },
    contactSeller() {
      if (this.role !== 'customer') {
        this.showToast('error', this.$t('messages.loginRequired'))
        this.$router.push('/login')
        return
      }
      this.showContact = true
    },
    onSent() {
      this.showContact = false
      window.dispatchEvent(new CustomEvent('messages-read'))
      this.showToast('success', this.$t('messages.sent'))
    },
    showToast(type, message) {
      clearTimeout(this.toastTimer)
      this.toast = { show: true, type, message }
      this.toastTimer = setTimeout(() => { this.toast.show = false }, 2500)
    },
    formatPrice(price) {
      const n = Number(price)
      return Number.isNaN(n) ? price : new Intl.NumberFormat(this.$i18n.locale + '-u-nu-latn', { minimumFractionDigits: 2, maximumFractionDigits: 2, useGrouping: false }).format(n)
    },
  },
}
</script>

<style scoped>
.store-page { display: block; width: min(1100px, 92%); height: auto; margin: 130px auto 2rem; }
.back { display: inline-block; margin-bottom: 1rem; color: var(--color-text-muted); text-decoration: none; font-size: 0.9rem; }
.back:hover { color: var(--color-text); }
.state { margin: 0; color: var(--color-text-muted); }
.state.error { color: var(--color-error); }

.store-head {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.store-head h1 { margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--color-text); }
.store-actions { display: flex; align-items: center; gap: 0.75rem; margin-top: 8px; flex-wrap: wrap; }
.msg-btn { padding: 0.4rem 1rem; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); cursor: pointer; }
.msg-btn:hover { border-color: #c7d6f7; }
.toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); z-index: 1200; padding: 0.6rem 1.2rem; border-radius: var(--radius-md); background: #1f8a4c; color: #fff; }
.toast.error { background: #c0392b; }
.toast-enter-active, .toast-leave-active { transition: opacity 0.25s; }
.toast-enter-from, .toast-leave-to { opacity: 0; }
.meta { margin: 0.2rem 0 0; font-size: 0.85rem; color: var(--color-text-muted); }
.logo { width: 88px; height: 88px; border-radius: var(--radius-md); object-fit: cover; border: 1px solid var(--color-border); flex-shrink: 0; }
.fallback { display: flex; align-items: center; justify-content: center; background: #e8efff; color: #1a56db; font-size: 2rem; font-weight: 700; }

.section-title { margin: 1.75rem 0 1rem; font-size: 1.15rem; font-weight: 600; color: var(--color-text); }
.grid { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 1rem; }
.product {
  display: block;
  height: 100%;
  padding: 0.75rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.15s, border-color 0.15s;
}
.product:hover { box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08); border-color: #c7d6f7; }
.thumb { aspect-ratio: 1; border-radius: var(--radius-md); background: var(--color-border); overflow: hidden; margin-bottom: 0.6rem; }
.thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.product h3 { margin: 0; font-size: 0.95rem; font-weight: 500; color: var(--color-text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.price { margin: 0.3rem 0 0; font-weight: 700; color: var(--color-text); font-variant-numeric: tabular-nums; }
.price span { font-weight: 400; font-size: 0.8rem; color: var(--color-text-muted); }
.oos { margin: 0.25rem 0 0; font-size: 0.8rem; color: var(--color-error); }

.pager { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-top: 1.5rem; font-size: 0.9rem; color: var(--color-text-muted); }
.pager button { padding: 0.4rem 1rem; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); cursor: pointer; }
.pager button:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 480px) {
  .store-head { flex-direction: column; text-align: center; }
  .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.75rem; }
}
</style>
