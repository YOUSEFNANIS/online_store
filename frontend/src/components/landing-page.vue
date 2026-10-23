<template>
<div class="cj">
<a class="skip" href="#main">Skip to content</a>

<section class="hero" aria-labelledby="hero-title">
  <div v-if="heroProducts.length" class="rows" aria-hidden="true">
    <div class="track l" :style="{ '--dur': heroLoop.length / 2 * 20 + 's' }">
      <router-link v-for="(p, i) in heroLoop" :key="'p' + i" class="pcard" :to="'/products/' + p.id" tabindex="-1"><img :src="p.images[0].image" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>{{ p.name }}</strong><span>{{ p.store_name }}</span></div></router-link>
    </div>
    <div v-if="stores.length" class="track r" :style="{ '--dur': storesLoop.length / 2 * 28 + 's' }">
      <router-link v-for="(s, i) in storesLoop" :key="'s' + i" class="scard" :to="'/sellers/' + s.id" tabindex="-1"><span class="logo-badge" :style="{ background: badgeColor(s.id) }"><img v-if="s.store_image" :src="s.store_image" alt="">
      <template v-else>{{ initials(s.store_name) }}</template></span><div><strong>{{ s.store_name }}</strong><span>{{ storeMeta(s) }}</span></div></router-link>
    </div>
  </div>
  <div class="mask"></div>
  <div class="fg">
    <span v-if="stats" class="pill">{{ fmt(stats.stores) }} stores · {{ fmt(stats.products) }} products</span>
    <h1 id="hero-title">Every store. Every product. <em>One bazar.</em></h1>
    <HeroSearchBar class="hero-search-slot" />
  </div>
</section>

<div class="trust"><div class="wrap"><ul>
  <li><span class="i"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/></svg></span>Fast delivery</li>
  <li><span class="i"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg></span>Buyer protection</li>
  <li><span class="i"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-15-6.7L3 13"/></svg></span>Easy returns</li>
  <li><span class="i"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg></span>Pay on delivery</li>
</ul></div></div>

<main id="main">
<section v-for="section in sections" :key="section.category" class="s"><div class="wrap">
  <div class="sh"><h2>{{ categoryName(section.category) }}</h2><span class="chip">New arrivals</span><router-link class="all" :to="{ path: '/products', query: { category: section.category } }">See all<span class="sr"> {{ categoryName(section.category) }}</span> →</router-link></div>
  <div class="mq" @mouseenter="paused = true" @mouseleave="paused = false"><ul class="mtrack" :class="{ jump: pulseOf(section.products) === 0 }" :style="{ '--pos': pulseOf(section.products) }"><li v-for="(p, i) in sectionLoop(section.products)" :key="i" class="card" :aria-hidden="i >= section.products.length ? 'true' : null">
    <router-link class="card-img" :to="'/products/' + p.id" tabindex="-1" aria-hidden="true"><img v-if="p.images.length" :src="p.images[0].image" width="400" height="400" alt="" loading="lazy"></router-link>
    <wishlist-heart :product-id="p.id" class="heart-pos" />
    <div class="card-body"><h3><router-link :to="'/products/' + p.id">{{ p.name }}</router-link></h3><p class="store"><span class="dot" :style="{ background: badgeColor(p.seller_id, true) }" aria-hidden="true">{{ initials(p.store_name).charAt(0) }}</span>{{ p.store_name }}</p>
    <p v-if="p.rating_count" class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor"/></svg></span><span class="sr">Rated </span>{{ p.rating_avg }}<span class="muted"> ({{ fmt(p.rating_count) }})</span></p>
    <p class="price"><strong>{{ formatPrice(p.price) }}</strong><span class="cur">{{ $t('storefront.currency') }}</span></p></div></li></ul></div>
</div></section>

<section v-if="stores.length" class="s" id="stores"><div class="wrap">
  <div class="sh"><h2>Popular stores</h2><router-link class="all" to="/sellers">All stores →</router-link></div>
  <ul class="stores"><li v-for="s in stores" :key="s.id"><router-link class="srow" :to="'/sellers/' + s.id"><span class="logo-badge" :style="{ background: badgeColor(s.id) }"><img v-if="s.store_image" :src="s.store_image" alt="">
  <template v-else>{{ initials(s.store_name) }}</template></span><div><strong>{{ s.store_name }}</strong><span class="m">{{ storeMeta(s) }}</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></router-link></li></ul>
</div></section>

<div class="wrap"><section id="sell" class="cta">
  <div><h2>Open your store on Cj bazar</h2><p>Reach thousands of buyers. No setup fees, no monthly fees.</p></div>
  <router-link class="btn" to="/signup">Start selling — it's free</router-link>
</section></div>
</main>

<footer><div class="wrap">
  <router-link class="brand" to="/" aria-label="Cj bazar home"><svg width="30" height="30" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#2F5BEA"/><path d="M12 15h16l-1.2 14a2 2 0 0 1-2 1.8h-9.6a2 2 0 0 1-2-1.8z" fill="#fff"/><path d="M16 17v-3a4 4 0 0 1 8 0v3" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg><span>Cj <b>bazar</b></span></router-link>
  <span class="copy">© 2026 Cj bazar</span>
  <nav aria-label="Footer"><router-link to="/products">Products</router-link><router-link to="/sellers">Stores</router-link><router-link to="/signup">Sell on Cj bazar</router-link><router-link to="/terms">Terms</router-link></nav>
</div></footer>
</div>
</template>

<script>
import api from '@/services/api';
import HeroSearchBar from '@/components/helperComponents/hero-search-bar.vue';
import WishlistHeart from '@/components/helperComponents/wishlist-heart.vue';
import { useCatalogStore } from '@/stores/catalog';
import { BookOpen, Car, Dumbbell, House, Package, Shirt, ShoppingBasket, Smartphone, Sparkles, ToyBrick } from '@lucide/vue';

// Icon per seeded category slug (see seed_categories); unknown slugs fall back to a box.
const CATEGORY_ICONS = {
  electronics: Smartphone, fashion: Shirt, 'home-garden': House, beauty: Sparkles, sports: Dumbbell,
  toys: ToyBrick, food: ShoppingBasket, books: BookOpen, automotive: Car,
};
const SOFT = ['#EEF2FF', '#FFF1F2', '#ECFDF5', '#FFFBEB'];
const STRONG = ['#2F5BEA', '#0E7490', '#7C3AED', '#B45309', '#047857'];
const MIN_TRACK = 14; // 14 product cards (226px) outspan a 2560px screen, so the loop never shows a gap
const PULSE_MS = 4500;

// Repeat a short list until one half of the marquee is wide enough, then double it for the seamless loop.
const loopOf = (items, min = MIN_TRACK) => {
  if (!items.length) return [];
  const half = [];
  while (half.length < min) half.push(...items);
  return [...half, ...half];
};

export default {
  name: 'MarketplaceLanding',
  components: { HeroSearchBar, WishlistHeart },
  data() {
    return {
      stats: null, categories: [], trending: [], sections: [], heroProducts: [], stores: [],
      pulse: 0, paused: false, pulseTimer: null,
    };
  },
  computed: {
    catalog() { return useCatalogStore(); },
    heroLoop() { return loopOf(this.heroProducts); },
    storesLoop() { return loopOf(this.stores); },
  },
  async created() {
    this.catalog.load();
    try {
      const { hero_products, ...home } = (await api.get('/core/home/')).data;
      Object.assign(this, home, { heroProducts: hero_products });
    } catch (e) { /* the page still renders its static parts */ }
  },
  mounted() {
    this.pulseTimer = setInterval(() => { if (!this.paused) this.pulse++; }, PULSE_MS);
  },
  beforeUnmount() {
    clearInterval(this.pulseTimer);
  },
  methods: {
    fmt(n) { return new Intl.NumberFormat(this.$i18n.locale + '-u-nu-latn').format(n); },
    formatPrice(price) {
      const n = Number(price);
      return Number.isNaN(n) ? price : new Intl.NumberFormat(this.$i18n.locale + '-u-nu-latn', { minimumFractionDigits: 2, maximumFractionDigits: 2, useGrouping: false }).format(n);
    },
    sectionLoop(products) { return loopOf(products, 6); },
    // One card per pulse; position `half` looks the same as 0, so the wrap back to 0 is an invisible jump.
    pulseOf(products) { return this.pulse % (this.sectionLoop(products).length / 2 + 1); },
    categoryIcon(slug) { return CATEGORY_ICONS[slug] || Package; },
    categoryName(id) {
      const c = this.categories.find((x) => x.id === id);
      return c ? this.catalog.nameOf(c, this.$i18n.locale) : '';
    },
    badgeColor(id, strong = false) {
      const palette = strong ? STRONG : SOFT;
      return palette[id % palette.length];
    },
    initials(name) {
      const words = (name || '?').trim().split(/\s+/);
      return (words.length > 1 ? words[0][0] + words[1][0] : words[0].slice(0, 2)).toUpperCase();
    },
    storeMeta(s) {
      const items = `${this.fmt(s.product_count)} ${s.product_count === 1 ? 'product' : 'products'}`;
      return s.rating_count ? `${items} · ★ ${s.rating_avg}` : items;
    },
  },
};
</script>

<style scoped>
.cj{--accent:#2F5BEA;--accent-dark:#2447C4;--accent-soft:#EEF2FF;--dark:#0B1220;--text:#111827;--muted:#6B7280;--border:#EAECF0;--radius:14px}
*{box-sizing:border-box}
.cj{display:block;width:100%;height:auto;margin:var(--app-bar-h) 0 0;overflow-x:clip;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--text);background:#fff;line-height:1.5;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
a{color:inherit;text-decoration:none;font-weight:inherit}
a:hover{color:inherit}
ul{list-style:none;margin:0;padding:0}
h1,h2,h3,p{margin:0}
button,input,select{font:inherit;color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.wrap{max-width:1240px;margin:0 auto;padding:0 24px}
.muted{color:var(--muted)}
.skip{position:absolute;left:-999px;top:8px;background:var(--accent);color:#fff;padding:8px 14px;border-radius:8px;z-index:100}
.skip:focus{left:8px}

/* Anchor targets stop below the fixed app navbar instead of under it. */
#main,#stores,#sell{scroll-margin-top:calc(var(--app-bar-live-h, var(--app-bar-h)) + 16px)}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:22px;letter-spacing:-.02em}
.brand b{color:var(--accent)}

/* hero */
.hero{position:relative;height:620px;overflow:hidden;background:var(--dark);isolation:isolate;padding:0}
.rows{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:18px}
.track{display:flex;width:max-content;will-change:transform}
.track.l{animation:left var(--dur,400s) linear infinite}
.track.r{animation:right var(--dur,400s) linear infinite}
/* identity.css shrinks every animation to 0.01ms under reduced motion, which makes an infinite loop flicker; keep the slow drift instead */
@media (prefers-reduced-motion:reduce){.track{animation-duration:var(--dur,400s)!important}}
@keyframes left{from{transform:translate3d(0,0,0)}to{transform:translate3d(-50%,0,0)}}
@keyframes right{from{transform:translate3d(-50%,0,0)}to{transform:translate3d(0,0,0)}}
.pcard{position:relative;flex:none;width:210px;height:250px;margin-right:16px;border-radius:16px;overflow:hidden;background:#1F2937}
.pcard img{width:100%;height:100%;object-fit:cover}
.pcard-txt{position:absolute;inset:auto 0 0;padding:36px 14px 12px;background:linear-gradient(transparent,rgba(0,0,0,.82));color:#fff;display:flex;flex-direction:column}
.pcard-txt strong{font-size:14px;font-weight:600;line-height:1.3}
.pcard-txt span{font-size:12px;color:#D1D5DB}
.scard{flex:none;width:300px;height:170px;margin-right:16px;border-radius:16px;background:#fff;display:flex;align-items:center;gap:16px;padding:0 24px}
.scard strong{display:block;font-size:17px}
.scard span:not(.logo-badge){font-size:13px;color:var(--muted)}
.logo-badge{flex:none;width:64px;height:64px;border-radius:16px;display:grid;place-items:center;font-weight:800;font-size:22px;color:var(--accent)}
.mask{position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(180deg,rgba(11,18,32,.95),rgba(11,18,32,0) 22%,rgba(11,18,32,0) 78%,rgba(11,18,32,.95)),rgba(8,12,24,.72)}
.fg{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 24px;color:#fff}
.pill{display:inline-block;padding:6px 14px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);font-size:13px;font-weight:600}
.fg h1{margin-top:18px;font-size:52px;line-height:1.1;font-weight:800;letter-spacing:-.03em;max-width:860px}
.fg h1 em{font-style:normal;color:#8FA9FF}
.sub{margin-top:14px;font-size:18px;color:#D1D5DB;max-width:620px}
.hero-search-slot{margin-top:28px}
.trend{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px;justify-content:center;align-items:center;font-size:14px;color:#D1D5DB}
.trend a{padding:5px 12px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff}
.trend a:hover{background:#fff;color:var(--text)}

/* trust */
.trust{border-bottom:1px solid var(--border)}
.trust ul{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:22px 0}
.trust li{display:flex;align-items:center;gap:12px;font-weight:600;font-size:14px}
.trust li span.i{flex:none;width:44px;height:44px;border-radius:50%;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center}
.trust li:nth-child(1) span.i{background:#FFF1E5;color:#EA7A0C}
.trust li:nth-child(2) span.i{background:#E6F7EE;color:#16A34A}
.trust li:nth-child(3) span.i{background:#F3EBFF;color:#8B5CF6}
.trust li:nth-child(4) span.i{background:#E6F4FA;color:#0891B2}

/* sections */
section.s{padding:48px 0 0}
.sh{display:flex;align-items:center;gap:12px;margin-bottom:22px}
.sh h2{font-size:26px;font-weight:800;letter-spacing:-.02em}
.sh .chip{font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent-dark)}
.sh .all{margin-left:auto;font-weight:600;color:var(--accent-dark);font-size:15px;white-space:nowrap}
.sh .all:hover{text-decoration:underline}
.cats{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(110px,1fr);gap:12px;overflow-x:auto;scrollbar-width:thin}
.cat{display:flex;flex-direction:column;align-items:center;gap:8px;padding:18px 8px;border-radius:var(--radius);border:1px solid transparent;text-align:center;transition:background .15s,border-color .15s}
.cat:hover{background:var(--accent-soft);border-color:#D6E0FF}
.cat .c{width:56px;height:56px;border-radius:50%;display:grid;place-items:center;color:var(--accent)}
.cat strong{font-size:14px}
.cat span.n{font-size:12px;color:var(--muted)}
.mq{overflow:hidden;padding:4px 0 12px}
.mtrack{--step:238px;display:flex;width:max-content;transform:translateX(calc(var(--step) * var(--pos) * -1));transition:transform 2.2s cubic-bezier(.45,0,.2,1);will-change:transform}
.mtrack.jump{transition:none}
.mtrack .card{flex:none;width:220px;margin-right:18px}
.card{position:relative;background:#fff;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:transform .18s,box-shadow .18s}
.card:hover,.card:focus-within{transform:translateY(-2px);box-shadow:0 10px 24px rgba(16,24,40,.1)}
.card-img{display:block;position:relative;aspect-ratio:1;background:#F3F4F6}
.card-img img{width:100%;height:100%;object-fit:cover}
.heart-pos{position:absolute;top:8px;right:8px;z-index:1}
.card-body{padding:12px 14px 14px}
.card h3{font-size:14px;font-weight:600;line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.7em}
.card h3 a:hover{color:var(--accent-dark)}
.store{margin-top:8px;display:flex;align-items:center;gap:6px;font-size:13px;color:var(--muted)}
.dot{width:18px;height:18px;border-radius:50%;color:#fff;font-size:10px;font-weight:700;display:grid;place-items:center}
.rating{margin-top:4px;display:flex;align-items:center;gap:4px;font-size:13px;font-weight:600}
.star{color:#D97706;display:inline-flex}.star svg{width:15px;height:15px}
.rating .muted{font-weight:400}
.price{margin-top:8px;display:flex;align-items:baseline;gap:8px}
.price strong{font-size:18px;font-weight:800}
.price .cur{font-size:13px;color:var(--muted)}
.logo-badge{overflow:hidden}
.logo-badge img{width:100%;height:100%;object-fit:cover}
.stores{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.srow{display:flex;align-items:center;gap:14px;padding:16px;border:1px solid var(--border);border-radius:var(--radius);transition:border-color .15s,box-shadow .15s}
.srow:hover{border-color:var(--accent);box-shadow:0 6px 18px rgba(47,91,234,.12)}
.srow .logo-badge{width:52px;height:52px;font-size:18px;border-radius:14px}
.srow div{flex:1;min-width:0}
.srow strong{display:block}
.srow span.m{font-size:13px;color:var(--muted)}
.srow svg{flex:none;color:var(--muted)}

/* cta + footer */
.cta{margin-top:64px;background:var(--dark);color:#fff;border-radius:24px;padding:48px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.cta h2{font-size:32px;font-weight:800;letter-spacing:-.02em}
.cta p{margin-top:6px;color:#D1D5DB}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 28px;border-radius:12px;background:var(--accent);color:#fff;font-weight:700;white-space:nowrap}
.btn:hover{background:var(--accent-dark)}
footer{margin-top:64px;border-top:1px solid var(--border);padding:28px 0 calc(28px + env(safe-area-inset-bottom))}
footer .wrap{display:flex;align-items:center;gap:24px;flex-wrap:wrap}
footer .copy{color:var(--muted);font-size:14px}
footer nav{margin-left:auto;display:flex;gap:20px;flex-wrap:wrap;font-size:14px;color:#374151}
footer nav a:hover{color:var(--accent-dark);text-decoration:underline}

@media (max-width:1100px){.stores{grid-template-columns:repeat(2,1fr)}}
@media (max-width:860px){
  .hero{height:auto;min-height:620px;display:flex}
  .fg{height:auto;flex:1;padding:56px 16px}
  .sh .all{font-size:14px}
  .fg h1{font-size:34px}
  .sub{font-size:16px}
  .trust ul{grid-template-columns:repeat(2,1fr)}
  .mtrack{--step:182px}
  .mtrack .card{width:170px;margin-right:12px}
  .cta{flex-direction:column;align-items:flex-start;padding:32px 24px}
  footer nav{margin-left:0}
}
@media (max-width:480px){.brand{font-size:20px}.pcard{width:170px;height:210px}.scard{width:260px;height:150px}.cta h2{font-size:24px}.cta .btn{width:100%}.cats{gap:4px}.cat strong{font-size:13px}.wrap{padding:0 16px}.stores{grid-template-columns:1fr}.sh h2{font-size:22px}.sh{flex-wrap:wrap}}
</style>
