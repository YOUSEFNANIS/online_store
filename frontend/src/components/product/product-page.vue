<template>
  <div class="product-wrapper">
    <load-component v-if="loading" />
    <div v-else class="product-page">
      <router-link to="/products" class="back-link">
        <span class="back-arrow" aria-hidden="true">←</span>
        {{ $t('productPage.back') }}
      </router-link>

      <div class="product-card">
        <section class="image-section">
          <div class="slider-wrapper">
            <transition name="fade" mode="out-in">
              <img
                v-if="currentImage && !failed[activeIndex]"
                :key="activeIndex"
                :src="currentImage"
                :alt="product.name"
                class="main-display-image"
                @error="failed[activeIndex] = true"
              />
              <div v-else key="placeholder" class="image-placeholder">
                <span class="placeholder-icon" aria-hidden="true">🖼</span>
                <span>{{ $t('productPage.noImage') }}</span>
              </div>
            </transition>

            <template v-if="product.images.length > 1">
              <button class="arrow-btn left" :aria-label="$t('productPage.previous')" @click="prevImage">❮</button>
              <button class="arrow-btn right" :aria-label="$t('productPage.next')" @click="nextImage">❯</button>
            </template>
          </div>

          <div v-if="product.images.length > 1" class="thumbnails-grid">
            <button
              v-for="(img, i) in product.images"
              :key="i"
              type="button"
              class="thumb-btn"
              :class="{ selected: i === activeIndex }"
              @click="activeIndex = i"
            >
              <img :src="img.image" alt="" class="thumb-item" @error="$event.target.style.visibility = 'hidden'" />
            </button>
          </div>
        </section>

        <section class="details-section">
          <h1 class="name-box">{{ product.name }}</h1>
          <star-rating :value="product.rating_avg || 0" :count="product.rating_count || 0" :empty-label="$t('reviews.noRatings')" />
          <div class="price-box">
            <span class="price-value">{{ formattedPrice }}</span>
            <span class="price-currency">{{ $t('productPage.currency') }}</span>
          </div>

          <div class="description-box">
            <h2>{{ $t('productPage.description') }}</h2>
            <p>{{ product.description }}</p>
          </div>

          <div class="btn-group">
            <button class="btn btn-cta" @click="createOrder">{{ $t('productPage.orderNow') }}</button>
            <button class="btn btn-outline" :disabled="adding" @click="addToCart">
              {{ added ? '✓ ' + $t('productPage.added') : $t('productPage.addToCart') }}
            </button>
            <wishlist-heart :product-id="product.id" />
            <button v-if="role !== 'seller'" class="btn btn-outline" @click="contactSeller">
              {{ $t('messages.contactSeller') }}
            </button>
          </div>
          <div v-if="role !== 'seller'" class="report-row">
            <report-button :product="product.id" />
          </div>
        </section>
      </div>

      <product-reviews
        :product-id="product.id"
        :average="product.rating_avg || 0"
        :count="product.rating_count || 0"
        @changed="refreshProduct"
      />

      <related-products :product-id="product.id" />
    </div>

    <contact-seller-modal
      v-if="showContact"
      :product="product"
      @close="showContact = false"
      @sent="onInquirySent"
      @error="showToast('error', $event)"
    />

    <transition name="toast">
      <div v-if="toast.show" class="toast" :class="toast.type" role="status" aria-live="polite">
        <span aria-hidden="true">{{ toast.type === 'error' ? '✕' : '✓' }}</span>
        {{ toast.message }}
      </div>
    </transition>
  </div>
</template>

<script>
import api from '@/services/api';
import { useRoleStore } from '@/stores/role';
import ContactSellerModal from '@/components/messages/contact-seller-modal.vue';
import StarRating from '@/components/helperComponents/star-rating.vue';
import ProductReviews from '@/components/product/product-reviews.vue';
import RelatedProducts from '@/components/product/related-products.vue';
import WishlistHeart from '@/components/helperComponents/wishlist-heart.vue';
import ReportButton from '@/components/helperComponents/report-button.vue';
export default {
    components: { ContactSellerModal, StarRating, ProductReviews, ReportButton, RelatedProducts, WishlistHeart },
    data(){
        return {
            product: {name: '',
                      description: '',
                      price: 0.0,
                      id: null,
                      images: []},
            activeIndex: 0,
            loading: true,
            failed: {},
            showContact: false,
            adding: false,
            added: false,
            toast: {show: false, type: 'success', message: ''},
            toastTimer: null,
            addedTimer: null,
        }
    },
    computed: {
      role() {
        return useRoleStore().role
      },
      currentImage() {
        return this.product.images[this.activeIndex]?.image || null
      },
      formattedPrice() {
        return Number(this.product.price).toLocaleString('en-US', { maximumFractionDigits: 2 })
      },
    },
    mounted(){
      this.getdata();
    },

    methods: {
      async getdata(){
        this.loading = true;

        const url = '/core/products/' + this.$route.params.productId + '/';
        const response = await api.get(url);
        this.product = response.data;
        this.loading = false;
      },
      async refreshProduct() {
        const response = await api.get('/core/products/' + this.$route.params.productId + '/');
        this.product = response.data;
      },
      nextImage() {
            this.activeIndex = (this.activeIndex + 1) % this.product.images.length;
        },
        prevImage() {
            this.activeIndex = (this.activeIndex - 1 + this.product.images.length) % this.product.images.length;
        },
      showToast(type, message) {
          clearTimeout(this.toastTimer);
          this.toast = {show: true, type, message};
          this.toastTimer = setTimeout(() => { this.toast.show = false }, 2500);
      },
      async addToCart(){
          if (this.adding) return false;
          this.adding = true;
          try {
              const cart = await api.get('/core/cart/')
              const url = '/core/cart/' + cart.data[0].id + '/cartitem/'
              await api.post(url, {'product': this.product.id, 'quantity': 1, 'cart': cart.data[0].id})
              this.added = true;
              clearTimeout(this.addedTimer);
              this.addedTimer = setTimeout(() => { this.added = false }, 1500);
              this.showToast('success', this.$t('productPage.addedToCart'));
              return true;
          } catch (e) {
              console.error('addToCart failed', e)
              // DRF wraps ValidationError values in lists: {code: ['cart_full']}
              const full = [].concat(e.response?.data?.code ?? []).includes('cart_full')
              this.showToast('error', this.$t(full ? 'productPage.cartFull' : 'productPage.addFailed'));
              return false;
          } finally {
              this.adding = false;
          }
      },
      contactSeller() {
          if (this.role !== 'customer') {
              this.showToast('error', this.$t('messages.loginRequired'));
              this.$router.push('/login');
              return;
          }
          this.showContact = true;
      },
      onInquirySent() {
          this.showContact = false;
          window.dispatchEvent(new CustomEvent('messages-read'));
          this.showToast('success', this.$t('messages.sent'));
      },
      async createOrder(){
          if (await this.addToCart()) this.$router.push('/order')
      }
    },
    beforeUnmount() {
      clearTimeout(this.toastTimer);
      clearTimeout(this.addedTimer);
    }
}
</script>


<style scoped>
.product-wrapper { width: 100%; }
.product-page {
  width: 100%;
  max-width: 1100px;
  margin: 24px auto 48px;
  padding: 0 16px;
}

.back-link {
  display: inline-flex; align-items: center; gap: 6px;
  margin-bottom: 16px;
  color: var(--color-text-muted); font-size: 0.95rem;
}
.back-link:hover { color: var(--color-primary); }
[dir=rtl] .back-arrow { display: inline-block; transform: scaleX(-1); }

.product-card {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
  gap: 40px;
  padding: 28px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.image-section { display: flex; flex-direction: column; gap: 14px; min-width: 0; }

.slider-wrapper {
  position: relative;
  aspect-ratio: 1 / 1;
  max-height: 520px;
  width: 100%;
  display: flex; align-items: center; justify-content: center;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.main-display-image { width: 100%; height: 100%; object-fit: contain; }
.image-placeholder {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  color: var(--color-text-muted); font-size: 0.95rem;
}
.placeholder-icon { font-size: 3rem; opacity: 0.5; }

.arrow-btn {
  position: absolute; top: 50%; transform: translateY(-50%);
  width: 40px; height: 40px; padding: 0;
  display: flex; align-items: center; justify-content: center;
  background: rgba(255, 255, 255, 0.92); color: var(--color-text);
  border: 1px solid var(--color-border); border-radius: 50%;
  box-shadow: var(--shadow-md);
  transition: border-color var(--transition), color var(--transition);
}
.arrow-btn:hover { border-color: var(--color-primary); color: var(--color-primary); }
.left { inset-inline-start: 12px; }
.right { inset-inline-end: 12px; }
[dir=rtl] .arrow-btn { transform: translateY(-50%) scaleX(-1); }

.thumbnails-grid { display: flex; gap: 10px; flex-wrap: wrap; }
.thumb-btn {
  padding: 0; width: 64px; height: 64px; overflow: hidden;
  background: var(--color-bg);
  border: 2px solid var(--color-border); border-radius: var(--radius-sm);
  transition: border-color var(--transition);
}
.thumb-btn:hover { border-color: var(--color-text-muted); }
.thumb-btn.selected { border-color: var(--color-primary); }
.thumb-item { width: 100%; height: 100%; object-fit: cover; display: block; }

.details-section { display: flex; flex-direction: column; gap: 20px; text-align: start; min-width: 0; }
.report-row { margin-top: 16px; }
.name-box { margin: 0; font-size: 2rem; line-height: 1.25; color: var(--color-text); overflow-wrap: anywhere; }
.price-box {
  display: flex; align-items: baseline; gap: 8px;
  padding-bottom: 20px; border-bottom: 1px solid var(--color-border);
  color: var(--color-primary);
}
.price-value { font-size: 2rem; font-weight: 700; font-variant-numeric: tabular-nums; }
.price-currency { font-size: 1.05rem; font-weight: 600; color: var(--color-text-muted); }

.description-box {
  padding: 18px 20px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}
.description-box h2 { margin: 0 0 8px; font-size: 1.05rem; color: var(--color-text); }
.description-box p { margin: 0; color: var(--color-text-muted); line-height: 1.8; overflow-wrap: anywhere; white-space: pre-line; }

.btn-group { display: flex; flex-direction: column; gap: 12px; margin-top: auto; }
.btn-group .btn { width: 100%; min-height: 48px; font-size: 1.05rem; }

.toast {
  position: fixed; bottom: 24px; inset-inline-start: 50%;
  transform: translateX(-50%);
  z-index: 1000; display: flex; align-items: center; gap: 8px;
  padding: 12px 20px; max-width: calc(100vw - 32px);
  background: #1f7a4d; color: #fff;
  border-radius: var(--radius-md); box-shadow: var(--shadow-md);
  font-size: 0.95rem;
}
[dir=rtl] .toast { transform: translateX(50%); }
.toast.error { background: #c0392b; }
.toast-enter-active, .toast-leave-active { transition: opacity 0.25s, margin-bottom 0.25s; }
.toast-enter-from, .toast-leave-to { opacity: 0; margin-bottom: -12px; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 860px) {
  .product-card { grid-template-columns: 1fr; gap: 24px; padding: 16px; }
  .slider-wrapper { aspect-ratio: 4 / 3; }
  .name-box, .price-value { font-size: 1.5rem; }
}
</style>
