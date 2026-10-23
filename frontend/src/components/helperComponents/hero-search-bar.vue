<template>
  <div class="hero-search-wrap">
    <form class="hero-search" role="search" @submit.prevent="submit">
      <svg class="hero-search__icon" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <label class="hero-search__sr" for="hero-search-q">Search</label>
      <input id="hero-search-q" v-model="query" class="hero-search__input" type="search" name="q" :placeholder="placeholder" autocomplete="off">
      <button class="hero-search__btn" type="submit">Search</button>
    </form>
    <nav class="hero-tabs" aria-label="Browse">
      <router-link class="hero-tab" to="/products">Products</router-link>
      <router-link class="hero-tab" to="/sellers">Stores</router-link>
      <a class="hero-tab" href="#categories" @click.prevent="toCategories">Categories</a>
    </nav>
  </div>
</template>

<script>
import { scrollToTarget } from '@/services/smooth-scroll';

export default {
  name: 'HeroSearchBar',
  data() {
    return { query: '', placeholder: 'Search for products, brands or stores…' };
  },
  methods: {
    submit() {
      this.$router.push({ path: '/search', query: { q: this.query.trim() } });
    },
    toCategories() {
      scrollToTarget(document.getElementById('categories'));
    },
  },
};
</script>

<style scoped>
.hero-search-wrap{width:100%;max-width:820px;display:flex;flex-direction:column;align-items:center}
.hero-tabs{display:flex;gap:8px;margin-top:18px}
.hero-tab{padding:10px 26px;border-radius:999px;background:rgba(255,255,255,.12);color:#fff;font-size:20px;font-weight:700;transition:background 150ms,color 150ms}
.hero-tab:hover{background:#fff;color:#111827}
@media (max-width:860px){.hero-tab{padding:8px 16px;font-size:16px}}
.hero-search{display:flex;align-items:center;gap:8px;box-sizing:border-box;width:100%;max-width:820px;height:64px;padding:8px 8px 8px 22px;background:#FFFFFF;border:0;border-radius:999px;box-shadow:0 20px 50px rgba(0,0,0,.40);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;text-align:left}
.hero-search:focus-within{box-shadow:0 0 0 2px rgba(47,91,234,.4),0 20px 50px rgba(0,0,0,.40)}
.hero-search__icon{flex:none}
.hero-search__sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.hero-search__input{flex:1;min-width:0;height:100%;border:0;outline:0;background:none;box-shadow:none;padding:0;font:inherit;font-size:16px;color:#111827;-webkit-appearance:none;appearance:none}
.hero-search__input:focus,.hero-search__input:focus-visible{outline:0;box-shadow:none}
.hero-search__input::placeholder{color:#9CA3AF;opacity:1}
.hero-search__input::-webkit-search-cancel-button{-webkit-appearance:none}
.hero-search__btn{flex:none;height:46px;padding:0 24px;border:0;border-radius:999px;background:#2F5BEA;color:#FFFFFF;font:inherit;font-weight:600;font-size:15px;cursor:pointer;box-shadow:0 2px 6px rgba(17,24,39,.12),0 8px 20px rgba(47,91,234,.35);transition:background 150ms,box-shadow 150ms}
.hero-search__btn:hover{background:#2449C9;box-shadow:0 2px 6px rgba(17,24,39,.14),0 10px 26px rgba(47,91,234,.45)}
@media (max-width:860px){
  .hero-search{height:56px;padding:6px 6px 6px 16px}
  .hero-search__btn{height:42px;padding:0 16px}
}
</style>
