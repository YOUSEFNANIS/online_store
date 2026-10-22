<template>
  <section class="reviews">
    <h2>{{ $t('reviews.title') }}</h2>

    <div v-if="count > 0" class="summary">
      <span class="big">{{ average }}</span>
      <div>
        <star-rating :value="average" :count="count" :show-count="false" />
        <p class="muted">{{ $t('reviews.basedOn', { count }) }}</p>
      </div>
    </div>

    <div v-if="mine.can_review" class="form">
      <h3>{{ $t('reviews.writeTitle') }}</h3>
      <div class="pick" role="radiogroup" :aria-label="$t('reviews.rating')">
        <button
          v-for="n in 5"
          :key="n"
          type="button"
          role="radio"
          :aria-checked="n === rating"
          :class="{ on: n <= rating }"
          :aria-label="n + ' / 5'"
          @click="rating = n"
        >★</button>
      </div>
      <textarea v-model="text" rows="3" maxlength="1000" :placeholder="$t('reviews.placeholder')"></textarea>
      <p v-if="error" class="err" role="alert">{{ error }}</p>
      <button type="button" class="btn btn-primary" :disabled="!rating || sending" @click="submit">{{ $t('reviews.submit') }}</button>
    </div>
    <p v-else-if="role === 'customer' && !mine.review && loaded" class="muted">{{ $t('reviews.afterDelivery') }}</p>

    <p v-if="loaded && !reviews.length" class="muted">{{ $t('reviews.empty') }}</p>
    <ul v-else class="list">
      <li v-for="r in reviews" :key="r.id">
        <div class="row">
          <strong>{{ r.customer_name }}</strong>
          <star-rating :value="r.rating" :count="1" :show-count="false" />
          <span class="muted date">{{ formatDate(r.created) }}</span>
        </div>
        <p v-if="r.text" class="body">{{ r.text }}</p>
        <button v-if="r.mine" type="button" class="link" @click="remove(r)">{{ $t('reviews.delete') }}</button>
      </li>
    </ul>
    <button v-if="next" type="button" class="btn btn-outline" @click="load(page + 1)">{{ $t('reviews.more') }}</button>
  </section>
</template>

<script>
import api from '@/services/api';
import { useRoleStore } from '@/stores/role';
import StarRating from '@/components/helperComponents/star-rating.vue';

export default {
  name: 'ProductReviews',
  components: { StarRating },
  // average / count come from the product (exact values); the list itself is paged.
  props: {
    productId: { type: [Number, String], required: true },
    average: { type: Number, default: 0 },
    count: { type: Number, default: 0 },
  },
  emits: ['changed'],
  data() {
    return { reviews: [], page: 1, next: false, loaded: false, mine: { can_review: false, review: null }, rating: 0, text: '', sending: false, error: '' }
  },
  computed: {
    role() { return useRoleStore().role },
    base() { return `/core/products/${this.productId}/reviews/` },
  },
  mounted() {
    this.load(1)
    this.loadMine()
  },
  methods: {
    async load(page) {
      try {
        const { data } = await api.get(this.base, { params: { page } })
        this.reviews = page === 1 ? data.results : [...this.reviews, ...data.results]
        this.page = page
        this.next = !!data.next
      } catch (e) { /* the empty state is shown */ }
      this.loaded = true
    },
    async loadMine() {
      if (!this.role) return
      try { this.mine = (await api.get(this.base + 'mine/')).data } catch (e) { /* hidden */ }
    },
    async submit() {
      this.sending = true
      this.error = ''
      try {
        await api.post(this.base, { rating: this.rating, text: this.text })
        this.rating = 0
        this.text = ''
        await Promise.all([this.load(1), this.loadMine()])
        this.$emit('changed')
      } catch (e) {
        this.error = e.response?.data?.detail || this.$t('reviews.failed')
      } finally {
        this.sending = false
      }
    },
    async remove(r) {
      if (!window.confirm(this.$t('reviews.confirmDelete'))) return
      try {
        await api.delete(`${this.base}${r.id}/`)
        await Promise.all([this.load(1), this.loadMine()])
        this.$emit('changed')
      } catch (e) { /* the global error banner shows it */ }
    },
    formatDate(iso) {
      return new Date(iso).toLocaleDateString(this.$i18n.locale, { dateStyle: 'medium' })
    },
  },
}
</script>

<style scoped>
.reviews { margin-top: 32px; padding: 24px; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }
.reviews h2 { margin: 0 0 16px; font-size: 1.15rem; }
.muted { margin: 0; color: var(--color-text-muted); font-size: 0.9rem; }
.summary { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.big { font-size: 2.5rem; font-weight: 700; line-height: 1; }
.form { margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--color-border); }
.form h3 { margin: 0 0 8px; font-size: 1rem; }
.form textarea { width: 100%; box-sizing: border-box; margin: 8px 0; }
.pick button { background: none; border: none; padding: 0 2px; font-size: 1.8rem; line-height: 1; color: #d1d5db; cursor: pointer; }
.pick button.on { color: #f59e0b; }
.err { margin: 0 0 8px; color: var(--color-error); font-size: 0.9rem; }
.list { list-style: none; margin: 0 0 16px; padding: 0; }
.list li { padding: 14px 0; border-top: 1px solid var(--color-border); }
.list li:first-child { border-top: none; }
.row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.date { margin-inline-start: auto; }
.body { margin: 8px 0 0; white-space: pre-wrap; overflow-wrap: anywhere; }
.link { margin-top: 6px; padding: 0; background: none; border: none; color: var(--color-text-muted); font-size: 0.85rem; cursor: pointer; text-decoration: underline; }
</style>
