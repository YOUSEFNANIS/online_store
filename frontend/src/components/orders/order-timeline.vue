<template>
  <ol class="timeline">
    <li v-for="(e, i) in history" :key="i" :class="{ current: i === history.length - 1 }">
      <span class="dot" aria-hidden="true"></span>
      <span class="label">{{ $t('orderFlow.statuses.' + e.status) }}</span>
      <span class="when">{{ formatDate(e.at) }}</span>
    </li>
  </ol>
</template>

<script>
export default {
  name: 'OrderTimeline',
  props: { history: { type: Array, default: () => [] } },
  methods: {
    formatDate(iso) {
      const d = new Date(iso)
      return Number.isNaN(d.getTime()) ? '' : d.toLocaleString(this.$i18n.locale, { dateStyle: 'medium', timeStyle: 'short' })
    },
  },
}
</script>

<style scoped>
.timeline { list-style: none; margin: 0 0 20px; padding: 0; }
.timeline li { position: relative; display: flex; align-items: baseline; gap: 10px; padding: 0 0 14px; padding-inline-start: 22px; color: var(--color-text-muted); }
.timeline li::before { content: ''; position: absolute; inset-inline-start: 4px; top: 14px; bottom: -2px; width: 2px; background: var(--color-border); }
.timeline li:last-child::before { display: none; }
.dot { position: absolute; inset-inline-start: 0; top: 5px; width: 10px; height: 10px; border-radius: 50%; background: var(--color-border); }
.current .dot { background: #1a56db; }
.current .label { color: var(--color-text); font-weight: 600; }
.when { font-size: 0.8rem; margin-inline-start: auto; white-space: nowrap; }
</style>
