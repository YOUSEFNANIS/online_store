<template>
  <span class="report-wrap">
    <button type="button" class="report-btn" @click="open">⚑ {{ $t('report.button') }}</button>

    <div v-if="show" class="backdrop" @click.self="show = false">
      <div class="dialog" role="dialog" aria-modal="true" :aria-label="$t('report.title')">
        <h2>{{ $t('report.title') }}</h2>
        <p v-if="done" class="ok" role="status">{{ $t('report.thanks') }}</p>
        <template v-else>
          <label for="report-reason">{{ $t('report.reason') }}</label>
          <select id="report-reason" v-model="reason">
            <option v-for="r in reasons" :key="r" :value="r">{{ $t('report.reasons.' + r) }}</option>
          </select>
          <label for="report-details">{{ $t('report.details') }}</label>
          <textarea id="report-details" v-model="details" rows="4" maxlength="1000"></textarea>
          <p v-if="error" class="err" role="alert">{{ error }}</p>
        </template>
        <div class="actions">
          <button v-if="!done" type="button" class="btn btn-primary" :disabled="sending" @click="send">{{ $t('report.send') }}</button>
          <button type="button" class="btn btn-outline" @click="show = false">{{ $t('report.close') }}</button>
        </div>
      </div>
    </div>
  </span>
</template>

<script>
import api from '@/services/api';
import { useRoleStore } from '@/stores/role';

export default {
  name: 'ReportButton',
  // Pass exactly one of product / seller (ids).
  props: { product: { type: Number, default: null }, seller: { type: Number, default: null } },
  data() {
    return {
      show: false, reason: 'spam', details: '', sending: false, done: false, error: '',
      reasons: ['spam', 'fraud', 'inappropriate', 'counterfeit', 'other'],
    }
  },
  methods: {
    open() {
      if (!useRoleStore().role) {
        this.$router.push('/login')
        return
      }
      this.done = false
      this.error = ''
      this.show = true
    },
    async send() {
      this.sending = true
      this.error = ''
      try {
        const body = { reason: this.reason, details: this.details }
        if (this.product) body.product = this.product
        if (this.seller) body.seller = this.seller
        await api.post('/core/reports/', body)
        this.done = true
        this.details = ''
      } catch (e) {
        const data = e.response?.data
        this.error = data?.non_field_errors?.[0] || data?.detail || this.$t('report.failed')
      } finally {
        this.sending = false
      }
    },
  },
}
</script>

<style scoped>
.report-btn { background: none; border: none; padding: 0; color: var(--color-text-muted); font-size: 0.85rem; cursor: pointer; }
.report-btn:hover { color: var(--color-error); text-decoration: underline; }
.backdrop { position: fixed; inset: 0; z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 16px; background: rgba(0, 0, 0, 0.45); }
.dialog { width: min(440px, 100%); padding: 24px; background: var(--color-surface); border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); color: var(--color-text); }
.dialog h2 { margin: 0 0 16px; font-size: 1.15rem; }
.dialog label { display: block; margin: 12px 0 6px; font-size: 0.85rem; font-weight: 600; color: var(--color-text-muted); }
.dialog select, .dialog textarea { width: 100%; box-sizing: border-box; }
.actions { display: flex; gap: 8px; margin-top: 20px; }
.ok { color: var(--color-success, #166534); }
.err { margin: 10px 0 0; color: var(--color-error); font-size: 0.9rem; }
</style>
