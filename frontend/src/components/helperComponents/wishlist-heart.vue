<template>
  <button
    v-if="role !== 'seller'"
    type="button"
    class="heart"
    :class="{ on: saved }"
    :aria-pressed="saved"
    :aria-label="saved ? $t('wishlist.remove') : $t('wishlist.add')"
    :title="saved ? $t('wishlist.remove') : $t('wishlist.add')"
    @click.prevent.stop="click"
  >{{ saved ? '♥' : '♡' }}</button>
</template>

<script>
import { useRoleStore } from '@/stores/role';
import { useWishlistStore } from '@/stores/wishlist';

export default {
  name: 'WishlistHeart',
  props: { productId: { type: Number, required: true } },
  computed: {
    role() { return useRoleStore().role },
    store() { return useWishlistStore() },
    saved() { return this.store.has(this.productId) },
  },
  mounted() { this.store.load() },
  methods: {
    click() {
      if (this.role !== 'customer') {
        this.$router.push('/login')
        return
      }
      this.store.toggle(this.productId)
    },
  },
}
</script>

<style scoped>
.heart { display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px; padding: 0; border: 1px solid var(--color-border); border-radius: 50%; background: rgba(255, 255, 255, 0.92); color: var(--color-text-muted); font-size: 1.2rem; line-height: 1; cursor: pointer; }
.heart:hover { color: #e11d48; }
.heart.on { color: #e11d48; border-color: #fecdd3; }
</style>
