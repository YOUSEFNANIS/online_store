<template>
  <section v-if="products.length" class="related">
    <h2>{{ $t('catalog.related') }}</h2>
    <ul class="grid">
      <li v-for="p in products" :key="p.id"><product-card :product="p" /></li>
    </ul>
  </section>
</template>

<script>
import api from '@/services/api';
import ProductCard from './product-card.vue';

export default {
  name: 'RelatedProducts',
  components: { ProductCard },
  props: { productId: { type: [Number, String], default: null } },
  data() { return { products: [] } },
  watch: { productId: { immediate: true, handler() { this.load() } } },
  methods: {
    async load() {
      if (!this.productId) return
      try {
        this.products = (await api.get(`/core/products/${this.productId}/related/`)).data
      } catch (e) {
        this.products = []
      }
    },
  },
}
</script>

<style scoped>
.related { margin-top: 32px; }
.related h2 { margin: 0 0 16px; font-size: 1.15rem; }
.grid { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 1rem; }
@media (max-width: 480px) { .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.75rem; } }
</style>
