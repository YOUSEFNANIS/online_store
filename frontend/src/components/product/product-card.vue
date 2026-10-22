<template>
  <router-link :to="'/products/' + product.id" class="card">
    <div class="thumb">
      <img v-if="image && !broken" :src="image" :alt="product.name" loading="lazy" @error="broken = true" />
      <wishlist-heart :product-id="product.id" class="heart-pos" />
    </div>
    <h3 :title="product.name">{{ product.name }}</h3>
    <star-rating v-if="product.rating_count" :value="product.rating_avg || 0" :count="product.rating_count" />
    <p class="price">{{ formatPrice(product.price) }} <span>{{ $t('storefront.currency') }}</span></p>
    <p v-if="product.inventory <= 0" class="oos">{{ $t('storefront.outOfStock') }}</p>
  </router-link>
</template>

<script>
import StarRating from '@/components/helperComponents/star-rating.vue';
import WishlistHeart from '@/components/helperComponents/wishlist-heart.vue';

export default {
  name: 'ProductCard',
  components: { StarRating, WishlistHeart },
  props: { product: { type: Object, required: true } },
  data() { return { broken: false } },
  computed: {
    image() { return this.product.images?.[0]?.image || null },
  },
  methods: {
    formatPrice(price) {
      const n = Number(price)
      return Number.isNaN(n) ? price : new Intl.NumberFormat(this.$i18n.locale + '-u-nu-latn', { minimumFractionDigits: 2, maximumFractionDigits: 2, useGrouping: false }).format(n)
    },
  },
}
</script>

<style scoped>
.card { display: block; height: 100%; padding: 0.75rem; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); text-decoration: none; color: inherit; transition: box-shadow 0.15s, border-color 0.15s; }
.card:hover { box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08); border-color: #c7d6f7; }
.thumb { position: relative; aspect-ratio: 1; border-radius: var(--radius-md); background: var(--color-border); overflow: hidden; margin-bottom: 0.6rem; }
.thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.heart-pos { position: absolute; top: 8px; inset-inline-end: 8px; }
h3 { margin: 0; font-size: 0.95rem; font-weight: 500; color: var(--color-text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.price { margin: 0.3rem 0 0; font-weight: 700; color: var(--color-text); font-variant-numeric: tabular-nums; }
.price span { font-weight: 400; font-size: 0.8rem; color: var(--color-text-muted); }
.oos { margin: 0.25rem 0 0; font-size: 0.8rem; color: var(--color-error); }
</style>
