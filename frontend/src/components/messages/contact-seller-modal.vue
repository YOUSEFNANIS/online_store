<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal" role="dialog" aria-modal="true" :aria-label="$t('messages.contactSeller')">
      <header class="modal-header">
        <h2>{{ $t('messages.modalTitle', { store: product ? product.store_name : seller.store_name }) }}</h2>
        <button type="button" class="close-btn" :aria-label="$t('messages.cancel')" @click="$emit('close')">✕</button>
      </header>

      <div v-if="product" class="product-summary">
        <img v-if="image" :src="image" alt="" class="summary-img" />
        <div class="summary-info">
          <span class="summary-name">{{ product.name }}</span>
          <span class="summary-price">{{ Number(product.price).toLocaleString('en-US', { maximumFractionDigits: 2 }) }} {{ $t('productPage.currency') }}</span>
        </div>
      </div>

      <div class="quick-replies">
        <span class="quick-label">{{ $t('messages.quickReplies') }}</span>
        <button v-for="q in ['q1', 'q2', 'q3']" :key="q" type="button" class="chip" @click="addQuick($t('messages.' + q))">
          {{ $t('messages.' + q) }}
        </button>
      </div>

      <textarea
        v-model="body"
        class="body-input"
        rows="5"
        maxlength="2000"
        :placeholder="$t('messages.inquiryPlaceholder')"
      ></textarea>
      <div class="counter">{{ body.length }}/2000</div>

      <footer class="modal-footer">
        <button type="button" class="btn btn-outline" @click="$emit('close')">{{ $t('messages.cancel') }}</button>
        <button type="button" class="btn btn-cta" :disabled="sending || !body.trim()" @click="send">
          {{ $t('messages.sendInquiry') }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  props: {
    product: { type: Object, default: null },
    seller: { type: Object, default: null },
  },
  emits: ['close', 'sent', 'error'],
  data() {
    return { body: '', sending: false }
  },
  computed: {
    image() {
      return this.product?.images?.[0]?.image || null
    },
  },
  methods: {
    addQuick(text) {
      this.body = this.body.trim() ? this.body.trim() + '\n' + text : text
    },
    async send() {
      if (this.sending || !this.body.trim()) return
      this.sending = true
      try {
        const res = await api.post('messaging/conversations/', { ...(this.product ? { product: this.product.id } : { seller: this.seller.id }), body: this.body.trim() }, { skipGlobalError: true })
        this.$emit('sent', res.data.id)
      } catch (e) {
        console.error('send inquiry failed', e)
        this.$emit('error', this.$t('messages.sendFailed'))
      } finally {
        this.sending = false
      }
    },
  },
}
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0; z-index: 1100;
  display: flex; align-items: center; justify-content: center;
  padding: 16px; background: rgba(17, 24, 39, 0.5);
}
.modal {
  width: 100%; max-width: 520px; max-height: 100%; overflow-y: auto;
  display: flex; flex-direction: column; gap: 14px; padding: 20px;
  background: var(--color-surface); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg);
  text-align: start;
}
.modal-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.modal-header h2 { margin: 0; font-size: 1.15rem; overflow-wrap: anywhere; }
.close-btn { background: none; border: none; font-size: 1.1rem; color: var(--color-text-muted); cursor: pointer; }
.close-btn:hover { color: var(--color-text); }

.product-summary {
  display: flex; align-items: center; gap: 12px; padding: 10px;
  background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-md);
}
.summary-img { width: 56px; height: 56px; object-fit: cover; border-radius: var(--radius-sm); }
.summary-info { display: flex; flex-direction: column; min-width: 0; }
.summary-name { font-weight: 600; overflow-wrap: anywhere; }
.summary-price { color: var(--color-primary); font-weight: 600; font-size: 0.95rem; }

.quick-replies { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.quick-label { font-size: 0.85rem; color: var(--color-text-muted); }
.chip {
  padding: 4px 12px; font-size: 0.85rem; cursor: pointer;
  background: var(--color-primary-soft); color: var(--color-primary);
  border: 1px solid transparent; border-radius: 999px;
}
.chip:hover { border-color: var(--color-primary); }

.body-input {
  width: 100%; resize: vertical; padding: 10px 12px; font: inherit;
  border: 1px solid var(--color-border); border-radius: var(--radius-md);
}
.body-input:focus { outline: none; border-color: var(--color-primary); box-shadow: var(--focus-ring); }
.counter { margin-top: -10px; font-size: 0.8rem; color: var(--color-text-muted); text-align: end; }

.modal-footer { display: flex; justify-content: flex-end; gap: 10px; }
</style>
