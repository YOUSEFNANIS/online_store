<template>
  <div class="sellers-page">
    <header class="head">
      <h1>{{ $t('sellersList.title') }}</h1>
      <span v-if="loaded && !failed && count" class="count">{{ count }}</span>
    </header>

    <p v-if="failed" class="state error" role="alert">{{ $t('sellersList.failed') }}</p>
    <p v-else-if="!loaded" class="state" role="status">{{ $t('sellersList.loading') }}</p>
    <p v-else-if="!sellers.length" class="state">{{ $t('sellersList.empty') }}</p>
    <template v-else>
      <ul class="grid">
        <li v-for="s in sellers" :key="s.id">
        <router-link :to="'/sellers/' + s.id" class="card">
          <img
            v-if="s.profile_image && !broken[s.id]"
            :src="s.profile_image"
            alt=""
            class="avatar"
            @error="broken[s.id] = true"
          />
          <span v-else class="avatar fallback" aria-hidden="true">{{ (s.store_name || '?').charAt(0).toUpperCase() }}</span>
          <h2 class="store" :title="s.store_name">{{ s.store_name }}</h2>
          <p class="name">{{ s.name }}</p>
          <star-rating v-if="s.rating_count" :value="s.rating_avg || 0" :count="s.rating_count" class="card-rating" />
        </router-link>
        </li>
      </ul>
      <div v-if="pages > 1" class="pager">
        <button type="button" :disabled="page <= 1" @click="load(page - 1)">{{ $t('sellersList.prev') }}</button>
        <span>{{ $t('sellersList.pageOf', { page, total: pages }) }}</span>
        <button type="button" :disabled="page >= pages" @click="load(page + 1)">{{ $t('sellersList.next') }}</button>
      </div>
    </template>
  </div>
</template>

<script>
import api from '@/services/api';
import StarRating from '@/components/helperComponents/star-rating.vue';

export default {
  name: 'SellersList',
  components: { StarRating },
  data() {
    return { sellers: [], page: 1, pages: 1, count: 0, loaded: false, failed: false, broken: {} }
  },
  mounted() {
    this.load(1)
  },
  methods: {
    async load(page) {
      try {
        const response = await api.get('/signup/sellers/', { params: { page } })
        this.sellers = response.data.results
        this.page = page
        this.pages = response.data.total_pages || 1
        this.count = response.data.count || 0
        this.failed = false
      } catch (error) {
        this.failed = true
      }
      this.loaded = true
    },
  },
}
</script>

<style scoped>
.sellers-page { display: block; width: min(1000px, 92%); height: auto; margin: 130px auto 2rem; }
.head { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem; }
.head h1 { margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--color-text); }
.count {
  padding: 0.1rem 0.6rem;
  border-radius: 999px;
  background: var(--color-border);
  color: var(--color-text-muted);
  font-size: 0.85rem;
  font-variant-numeric: tabular-nums;
}
.state { margin: 0; color: var(--color-text-muted); }
.state.error { color: var(--color-error); }

.grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}
.card {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  column-gap: 1rem;
  padding: 1rem 1.25rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.15s, border-color 0.15s;
  text-decoration: none;
  color: inherit;
}
.card:hover { box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08); border-color: #c7d6f7; }
.avatar {
  grid-row: 1 / span 2;
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  object-fit: cover;
  border: 1px solid var(--color-border);
}
.fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e8efff;
  color: #1a56db;
  font-size: 1.5rem;
  font-weight: 700;
}
.store {
  margin: 0;
  align-self: end;
  min-width: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.card-rating { grid-column: 2; margin-top: 2px; }
.name { margin: 0.2rem 0 0; align-self: start; font-size: 0.85rem; color: var(--color-text-muted); }

.pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: var(--color-text-muted);
}
.pager button {
  padding: 0.4rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  cursor: pointer;
}
.pager button:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 480px) {
  .grid { grid-template-columns: 1fr; gap: 0.75rem; }
}
</style>
