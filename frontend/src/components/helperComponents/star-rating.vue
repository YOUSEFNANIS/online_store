<template>
  <span v-if="count > 0" class="rating" :title="`${value} / 5`">
    <span class="stars" aria-hidden="true">
      <span class="stars-back">★★★★★</span>
      <span class="stars-front" :style="{ width: (value / 5) * 100 + '%' }">★★★★★</span>
    </span>
    <span class="num">{{ value }}</span>
    <span v-if="showCount" class="count">({{ count }})</span>
  </span>
  <span v-else-if="emptyLabel" class="rating none">{{ emptyLabel }}</span>
</template>

<script>
export default {
  name: 'StarRating',
  props: {
    value: { type: Number, default: 0 },
    count: { type: Number, default: 0 },
    showCount: { type: Boolean, default: true },
    emptyLabel: { type: String, default: '' },
  },
}
</script>

<style scoped>
.rating { display: inline-flex; align-items: center; gap: 4px; font-size: 0.85rem; color: var(--color-text-muted); }
.stars { position: relative; display: inline-block; letter-spacing: 1px; line-height: 1; }
.stars-back { color: #d1d5db; }
.stars-front { position: absolute; inset-block: 0; inset-inline-start: 0; overflow: hidden; white-space: nowrap; color: #f59e0b; }
.num { font-weight: 600; color: var(--color-text); }
.none { font-style: italic; }
</style>
