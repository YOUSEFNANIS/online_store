<template>
  <div class="earn">
    <header>
      <h1>{{ $t('earnings.title') }}</h1>
      <p>{{ $t('earnings.rule', { threshold: fmt(summary?.threshold), rate: pct(summary?.commission_rate) }) }}</p>
    </header>

    <p v-if="failed" class="state error" role="alert">{{ $t('earnings.failed') }}</p>
    <template v-else>
      <section class="stats">
        <div class="stat">
          <span class="label">{{ $t('earnings.balance') }}</span>
          <span class="value">{{ summary ? fmt(summary.balance) : '—' }} <small>{{ $t('earnings.currency') }}</small></span>
        </div>
        <div class="stat">
          <span class="label">{{ $t('earnings.nextPayout') }}</span>
          <span class="value small">{{ summary ? formatDate(summary.next_payout) : '—' }}</span>
          <span v-if="summary" class="hint">{{ Number(summary.balance) > Number(summary.threshold) ? $t('earnings.willBePaid') : $t('earnings.belowThreshold', { threshold: fmt(summary.threshold) }) }}</span>
        </div>
        <div class="stat">
          <span class="label">{{ $t('earnings.lastPayout') }}</span>
          <span class="value small">{{ summary?.last_payout ? fmt(summary.last_payout.amount) + ' ' + $t('earnings.currency') : $t('earnings.none') }}</span>
          <span v-if="summary?.last_payout" class="hint">{{ formatDate(summary.last_payout.paid_at) }}</span>
        </div>
      </section>

      <section class="card">
        <div class="hist-head">
          <h2>{{ $t('earnings.history') }}</h2>
          <button type="button" class="btn btn-outline" @click="exportCsv">{{ $t('sellerTools.exportEarnings') }}</button>
        </div>
        <p v-if="loaded && !entries.length" class="state">{{ $t('earnings.empty') }}</p>
        <table v-else class="table">
          <thead>
            <tr>
              <th>{{ $t('earnings.date') }}</th>
              <th>{{ $t('earnings.type') }}</th>
              <th>{{ $t('earnings.order') }}</th>
              <th class="num">{{ $t('earnings.amount') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in entries" :key="e.id">
              <td :data-label="$t('earnings.date')">{{ formatDate(e.created) }}</td>
              <td :data-label="$t('earnings.type')">{{ $t('earnings.kinds.' + e.kind) }}</td>
              <td :data-label="$t('earnings.order')">{{ e.order ? '#' + e.order : '—' }}</td>
              <td :data-label="$t('earnings.amount')" class="num" :class="{ neg: Number(e.amount) < 0 }">{{ fmt(e.amount, true) }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="pages > 1" class="pager">
          <button type="button" :disabled="page <= 1" @click="load(page - 1)">{{ $t('storefront.prev') }}</button>
          <span>{{ $t('storefront.pageOf', { page, total: pages }) }}</span>
          <button type="button" :disabled="page >= pages" @click="load(page + 1)">{{ $t('storefront.next') }}</button>
        </div>
      </section>
    </template>
  </div>
</template>

<script>
import api from '@/services/api';
import { downloadFile } from '@/services/download';

export default {
  name: 'SellerEarnings',
  data() { return { summary: null, entries: [], page: 1, pages: 1, loaded: false, failed: false } },
  async mounted() {
    try {
      this.summary = (await api.get('/core/earnings/summary/')).data
      await this.load(1)
    } catch (e) {
      this.failed = true
    }
  },
  methods: {
    async exportCsv() {
      try { await downloadFile('/core/seller/export/earnings/', 'earnings.csv') } catch (e) { /* the global error banner shows it */ }
    },
    async load(page) {
      const { data } = await api.get('/core/earnings/', { params: { page } })
      this.entries = data.results
      this.page = page
      this.pages = data.total_pages || 1
      this.loaded = true
    },
    fmt(n, signed = false) {
      if (n === undefined || n === null) return ''
      return new Intl.NumberFormat(this.$i18n.locale + '-u-nu-latn', { minimumFractionDigits: 2, maximumFractionDigits: 2, signDisplay: signed ? 'exceptZero' : 'auto' }).format(Number(n))
    },
    pct(rate) {
      return rate === undefined ? '' : Math.round(Number(rate) * 1000) / 10
    },
    formatDate(value) {
      return value ? new Date(value).toLocaleDateString(this.$i18n.locale, { dateStyle: 'medium' }) : ''
    },
  },
}
</script>

<style scoped>
.earn { display: block; width: min(1000px, 92%); height: auto; margin: 130px auto 2rem; }
header h1 { margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--color-text); }
header p { margin: 0.25rem 0 1.25rem; color: var(--color-text-muted); font-size: 0.95rem; }
.state { margin: 0; color: var(--color-text-muted); }
.state.error { color: var(--color-error); }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.stat { display: flex; flex-direction: column; gap: 0.25rem; padding: 1rem 1.25rem; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); }
.label { font-size: 0.85rem; color: var(--color-text-muted); }
.value { font-size: 1.75rem; font-weight: 700; color: var(--color-text); font-variant-numeric: tabular-nums; }
.value.small { font-size: 1.15rem; }
.value small { font-size: 0.9rem; font-weight: 400; color: var(--color-text-muted); }
.hint { font-size: 0.8rem; color: var(--color-text-muted); }
.card { padding: 1.25rem; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); }
.hist-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 0.75rem; }
.hist-head h2 { margin: 0; }
.card h2 { margin: 0 0 0.75rem; font-size: 1rem; font-weight: 600; }
.table { width: 100%; border-collapse: collapse; text-align: start; }
.table th { padding: 8px 10px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--color-text-muted); text-align: start; border-bottom: 1px solid var(--color-border); }
.table td { padding: 10px; border-top: 1px solid var(--color-border); font-size: 0.92rem; }
.table tbody tr:first-child td { border-top: none; }
.num { text-align: end; font-variant-numeric: tabular-nums; white-space: nowrap; }
.neg { color: var(--color-error); }
.pager { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-top: 1rem; font-size: 0.9rem; color: var(--color-text-muted); }
.pager button { padding: 0.4rem 1rem; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); cursor: pointer; }
.pager button:disabled { opacity: 0.5; cursor: not-allowed; }
@media (max-width: 600px) {
  .table thead { display: none; }
  .table td { display: flex; justify-content: space-between; gap: 12px; }
  .table td::before { content: attr(data-label); color: var(--color-text-muted); }
}
</style>
