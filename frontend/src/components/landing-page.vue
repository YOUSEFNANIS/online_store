<template>
<div class="cj">
<a class="skip" href="#main">Skip to content</a>

<header class="hdr">
  <div class="wrap">
    <a class="brand" href="#" aria-label="Cj bazar home"><svg width="36" height="36" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#2F5BEA"/><path d="M12 15h16l-1.2 14a2 2 0 0 1-2 1.8h-9.6a2 2 0 0 1-2-1.8z" fill="#fff"/><path d="M16 17v-3a4 4 0 0 1 8 0v3" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg><span>Cj <b>bazar</b></span></a>
    <nav class="nav" aria-label="Main">
      <a href="#categories">Categories</a><a href="#stores">Stores</a><a href="#deals">Deals</a><a class="sell" href="#sell">Sell on Cj bazar</a>
    </nav>
    <div class="actions">
      <button class="ibtn" type="button" aria-label="Wishlist"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
      <router-link class="ibtn" to="/login" aria-label="Account"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></router-link>
      <button class="ibtn" type="button" aria-label="Cart, 3 items"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/></svg><span class="badge" aria-hidden="true">3</span></button>
    </div>
  </div>
</header>

<section class="hero" aria-labelledby="hero-title">
  <div class="rows" aria-hidden="true">
    <div class="track l"><div class="pcard"><img src="https://picsum.photos/seed/hp1/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Wireless Headphones</strong><span>Nova Tech</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp2/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Linen Summer Shirt</strong><span>Urban Thread</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp3/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Ceramic Pour-Over Set</strong><span>Casa Verde</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp4/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Running Shoes</strong><span>Peak Sports</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp5/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Smart Watch S2</strong><span>Nova Tech</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp6/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Vitamin C Serum</strong><span>Glow Lab</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp7/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Leather Backpack</strong><span>Urban Thread</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp8/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Cast Iron Skillet</strong><span>Casa Verde</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp1/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Wireless Headphones</strong><span>Nova Tech</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp2/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Linen Summer Shirt</strong><span>Urban Thread</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp3/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Ceramic Pour-Over Set</strong><span>Casa Verde</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp4/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Running Shoes</strong><span>Peak Sports</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp5/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Smart Watch S2</strong><span>Nova Tech</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp6/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Vitamin C Serum</strong><span>Glow Lab</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp7/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Leather Backpack</strong><span>Urban Thread</span></div></div><div class="pcard"><img src="https://picsum.photos/seed/hp8/420/500" width="210" height="250" alt="" loading="eager"><div class="pcard-txt"><strong>Cast Iron Skillet</strong><span>Casa Verde</span></div></div></div>
    <div class="track r"><div class="scard"><span class="logo-badge" style="background:#EEF2FF">NT</span><div><strong>Nova Tech</strong><span>Electronics · ★ 4.8</span></div></div><div class="scard"><span class="logo-badge" style="background:#FFF1F2">UT</span><div><strong>Urban Thread</strong><span>Fashion · ★ 4.7</span></div></div><div class="scard"><span class="logo-badge" style="background:#ECFDF5">CV</span><div><strong>Casa Verde</strong><span>Home & Kitchen · ★ 4.9</span></div></div><div class="scard"><span class="logo-badge" style="background:#FFFBEB">GL</span><div><strong>Glow Lab</strong><span>Beauty · ★ 4.6</span></div></div><div class="scard"><span class="logo-badge" style="background:#EEF2FF">PS</span><div><strong>Peak Sports</strong><span>Sports · ★ 4.7</span></div></div><div class="scard"><span class="logo-badge" style="background:#FFF1F2">LJ</span><div><strong>Little Joy</strong><span>Toys · ★ 4.8</span></div></div><div class="scard"><span class="logo-badge" style="background:#ECFDF5">PT</span><div><strong>Page Turner</strong><span>Books · ★ 4.9</span></div></div><div class="scard"><span class="logo-badge" style="background:#FFFBEB">FB</span><div><strong>Fresh Basket</strong><span>Grocery · ★ 4.5</span></div></div><div class="scard"><span class="logo-badge" style="background:#EEF2FF">NT</span><div><strong>Nova Tech</strong><span>Electronics · ★ 4.8</span></div></div><div class="scard"><span class="logo-badge" style="background:#FFF1F2">UT</span><div><strong>Urban Thread</strong><span>Fashion · ★ 4.7</span></div></div><div class="scard"><span class="logo-badge" style="background:#ECFDF5">CV</span><div><strong>Casa Verde</strong><span>Home & Kitchen · ★ 4.9</span></div></div><div class="scard"><span class="logo-badge" style="background:#FFFBEB">GL</span><div><strong>Glow Lab</strong><span>Beauty · ★ 4.6</span></div></div><div class="scard"><span class="logo-badge" style="background:#EEF2FF">PS</span><div><strong>Peak Sports</strong><span>Sports · ★ 4.7</span></div></div><div class="scard"><span class="logo-badge" style="background:#FFF1F2">LJ</span><div><strong>Little Joy</strong><span>Toys · ★ 4.8</span></div></div><div class="scard"><span class="logo-badge" style="background:#ECFDF5">PT</span><div><strong>Page Turner</strong><span>Books · ★ 4.9</span></div></div><div class="scard"><span class="logo-badge" style="background:#FFFBEB">FB</span><div><strong>Fresh Basket</strong><span>Grocery · ★ 4.5</span></div></div></div>
  </div>
  <div class="mask"></div>
  <div class="fg">
    <span class="pill">2,400+ stores · 180,000+ products</span>
    <h1 id="hero-title">Every store. Every product. <em>One bazar.</em></h1>
    <p class="sub">Shop independent stores with one cart, one checkout and one trusted marketplace.</p>
    <HeroSearchBar class="hero-search-slot" />
    <div class="trend"><span>Trending:</span><a href="#">Headphones</a><a href="#">Sneakers</a><a href="#">Air fryer</a><a href="#">Smart watch</a><a href="#">Backpacks</a></div>
  </div>
</section>

<div class="trust"><div class="wrap"><ul>
  <li><span class="i"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/></svg></span>Fast delivery</li>
  <li><span class="i"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg></span>Buyer protection</li>
  <li><span class="i"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-15-6.7L3 13"/></svg></span>Easy returns</li>
  <li><span class="i"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg></span>Pay on delivery or by card</li>
</ul></div></div>

<main id="main" @click="toggleHeart">
<section class="s" id="categories"><div class="wrap">
  <div class="sh"><h2>Shop by category</h2><a class="all" href="#">All categories →</a></div>
  <ul class="cats"><li><a class="cat" href="#"><span class="c" style="background:#EEF2FF"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/></svg></span><strong>Electronics</strong><span class="n">12,480 items</span></a></li><li><a class="cat" href="#"><span class="c" style="background:#FFF1F2"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/></svg></span><strong>Fashion</strong><span class="n">34,210 items</span></a></li><li><a class="cat" href="#"><span class="c" style="background:#ECFDF5"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg></span><strong>Home & Kitchen</strong><span class="n">21,950 items</span></a></li><li><a class="cat" href="#"><span class="c" style="background:#FFFBEB"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 17v4M17 19h4"/></svg></span><strong>Beauty</strong><span class="n">9,320 items</span></a></li><li><a class="cat" href="#"><span class="c" style="background:#EEF2FF"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20M2 12h20"/></svg></span><strong>Sports</strong><span class="n">7,845 items</span></a></li><li><a class="cat" href="#"><span class="c" style="background:#FFF1F2"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 16V8l-9-5-9 5v8l9 5z"/><path d="M3.3 7 12 12l8.7-5M12 22V12"/></svg></span><strong>Toys & Kids</strong><span class="n">6,110 items</span></a></li><li><a class="cat" href="#"><span class="c" style="background:#ECFDF5"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M20 17v4H6.5A2.5 2.5 0 0 1 4 18.5"/></svg></span><strong>Books</strong><span class="n">15,600 items</span></a></li><li><a class="cat" href="#"><span class="c" style="background:#FFFBEB"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 8h14l-1.5 11a2 2 0 0 1-2 1.7h-7a2 2 0 0 1-2-1.7z"/><path d="M9 8l3-5 3 5"/></svg></span><strong>Grocery</strong><span class="n">4,925 items</span></a></li></ul>
</div></section>

<section class="s" id="deals"><div class="wrap">
  <div class="sh"><h2>Electronics</h2><span class="chip">Top deals</span><a class="all" href="#">See all<span class="sr"> Electronics</span> →</a></div>
  <ul class="grid"><li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p00/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-sale">-20%</span></a>
<button class="heart" type="button" aria-label="Add Wireless Noise-Cancelling Headphones to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Wireless Noise-Cancelling Headphones</a></h3><p class="store"><span class="dot" style="background:#2F5BEA" aria-hidden="true">N</span>Nova Tech</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.8<span class="muted"> (2,310)</span></p>
<p class="price"><strong>$89.00</strong><s>$112.00</s></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p01/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-sale">-19%</span></a>
<button class="heart" type="button" aria-label="Add 4K Action Camera with Waterproof Case to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">4K Action Camera with Waterproof Case</a></h3><p class="store"><span class="dot" style="background:#0E7490" aria-hidden="true">N</span>Nova Tech</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.6<span class="muted"> (984)</span></p>
<p class="price"><strong>$129.00</strong><s>$159.00</s></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p02/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-best">Bestseller</span></a>
<button class="heart" type="button" aria-label="Add Portable Bluetooth Speaker to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Portable Bluetooth Speaker</a></h3><p class="store"><span class="dot" style="background:#7C3AED" aria-hidden="true">S</span>Sound Hub</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.7<span class="muted"> (1,520)</span></p>
<p class="price"><strong>$34.90</strong></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p03/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-sale">-20%</span></a>
<button class="heart" type="button" aria-label="Add Mechanical Gaming Keyboard RGB to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Mechanical Gaming Keyboard RGB</a></h3><p class="store"><span class="dot" style="background:#B45309" aria-hidden="true">P</span>Pixel Gear</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.5<span class="muted"> (640)</span></p>
<p class="price"><strong>$59.00</strong><s>$74.00</s></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p04/400/400" width="400" height="400" alt="" loading="lazy"></a>
<button class="heart" type="button" aria-label="Add Fast Charging Power Bank 20,000mAh to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Fast Charging Power Bank 20,000mAh</a></h3><p class="store"><span class="dot" style="background:#047857" aria-hidden="true">S</span>Sound Hub</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.8<span class="muted"> (3,105)</span></p>
<p class="price"><strong>$27.50</strong></p></div></li></ul>
</div></section>
<section class="s"><div class="wrap">
  <div class="sh"><h2>Fashion</h2><span class="chip">New season</span><a class="all" href="#">See all<span class="sr"> Fashion</span> →</a></div>
  <ul class="grid"><li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p10/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-new">New</span></a>
<button class="heart" type="button" aria-label="Add Linen Summer Shirt, Relaxed Fit to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Linen Summer Shirt, Relaxed Fit</a></h3><p class="store"><span class="dot" style="background:#2F5BEA" aria-hidden="true">U</span>Urban Thread</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.7<span class="muted"> (412)</span></p>
<p class="price"><strong>$32.00</strong></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p11/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-sale">-20%</span></a>
<button class="heart" type="button" aria-label="Add Classic Denim Jacket to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Classic Denim Jacket</a></h3><p class="store"><span class="dot" style="background:#0E7490" aria-hidden="true">U</span>Urban Thread</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.6<span class="muted"> (876)</span></p>
<p class="price"><strong>$68.00</strong><s>$85.00</s></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p12/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-new">New</span></a>
<button class="heart" type="button" aria-label="Add Minimal Leather Crossbody Bag to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Minimal Leather Crossbody Bag</a></h3><p class="store"><span class="dot" style="background:#7C3AED" aria-hidden="true">A</span>Atelier 9</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.8<span class="muted"> (290)</span></p>
<p class="price"><strong>$74.00</strong></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p13/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-sale">-21%</span></a>
<button class="heart" type="button" aria-label="Add Everyday White Sneakers to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Everyday White Sneakers</a></h3><p class="store"><span class="dot" style="background:#B45309" aria-hidden="true">P</span>Peak Sports</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.7<span class="muted"> (2,045)</span></p>
<p class="price"><strong>$49.00</strong><s>$62.00</s></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p14/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-new">New</span></a>
<button class="heart" type="button" aria-label="Add Merino Wool Scarf to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Merino Wool Scarf</a></h3><p class="store"><span class="dot" style="background:#047857" aria-hidden="true">A</span>Atelier 9</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.9<span class="muted"> (188)</span></p>
<p class="price"><strong>$26.00</strong></p></div></li></ul>
</div></section>
<section class="s"><div class="wrap">
  <div class="sh"><h2>Home & Kitchen</h2><span class="chip">Most popular</span><a class="all" href="#">See all<span class="sr"> Home & Kitchen</span> →</a></div>
  <ul class="grid"><li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p20/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-best">Bestseller</span></a>
<button class="heart" type="button" aria-label="Add Cast Iron Skillet 26cm to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Cast Iron Skillet 26cm</a></h3><p class="store"><span class="dot" style="background:#2F5BEA" aria-hidden="true">C</span>Casa Verde</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.9<span class="muted"> (1,730)</span></p>
<p class="price"><strong>$38.00</strong><s>$46.00</s></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p21/400/400" width="400" height="400" alt="" loading="lazy"></a>
<button class="heart" type="button" aria-label="Add Ceramic Pour-Over Coffee Set to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Ceramic Pour-Over Coffee Set</a></h3><p class="store"><span class="dot" style="background:#0E7490" aria-hidden="true">C</span>Casa Verde</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.7<span class="muted"> (560)</span></p>
<p class="price"><strong>$29.00</strong></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p22/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-sale">-20%</span></a>
<button class="heart" type="button" aria-label="Add Bamboo Storage Organizer Set to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Bamboo Storage Organizer Set</a></h3><p class="store"><span class="dot" style="background:#7C3AED" aria-hidden="true">N</span>Nest & Co</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.5<span class="muted"> (902)</span></p>
<p class="price"><strong>$21.50</strong><s>$27.00</s></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p23/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-best">Bestseller</span></a>
<button class="heart" type="button" aria-label="Add Stainless Steel Water Bottle 1L to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Stainless Steel Water Bottle 1L</a></h3><p class="store"><span class="dot" style="background:#B45309" aria-hidden="true">N</span>Nest & Co</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.8<span class="muted"> (4,120)</span></p>
<p class="price"><strong>$18.00</strong></p></div></li>
<li class="card"><a class="card-img" href="#" tabindex="-1" aria-hidden="true"><img src="https://picsum.photos/seed/p24/400/400" width="400" height="400" alt="" loading="lazy"><span class="tag tag-sale">-20%</span></a>
<button class="heart" type="button" aria-label="Add Soft Cotton Bedding Set, Queen to wishlist" aria-pressed="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg></button>
<div class="card-body"><h3><a href="#">Soft Cotton Bedding Set, Queen</a></h3><p class="store"><span class="dot" style="background:#047857" aria-hidden="true">C</span>Casa Verde</p>
<p class="rating"><span class="star"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/></svg></span><span class="sr">Rated </span>4.6<span class="muted"> (745)</span></p>
<p class="price"><strong>$79.00</strong><s>$99.00</s></p></div></li></ul>
</div></section>

<section class="s" id="stores"><div class="wrap">
  <div class="sh"><h2>Popular stores</h2><a class="all" href="#">All stores →</a></div>
  <ul class="stores"><li><a class="srow" href="#"><span class="logo-badge" style="background:#EEF2FF">NT</span><div><strong>Nova Tech</strong><span class="m">Electronics · ★ 4.8</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a></li><li><a class="srow" href="#"><span class="logo-badge" style="background:#FFF1F2">UT</span><div><strong>Urban Thread</strong><span class="m">Fashion · ★ 4.7</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a></li><li><a class="srow" href="#"><span class="logo-badge" style="background:#ECFDF5">CV</span><div><strong>Casa Verde</strong><span class="m">Home & Kitchen · ★ 4.9</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a></li><li><a class="srow" href="#"><span class="logo-badge" style="background:#FFFBEB">GL</span><div><strong>Glow Lab</strong><span class="m">Beauty · ★ 4.6</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a></li><li><a class="srow" href="#"><span class="logo-badge" style="background:#EEF2FF">PS</span><div><strong>Peak Sports</strong><span class="m">Sports · ★ 4.7</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a></li><li><a class="srow" href="#"><span class="logo-badge" style="background:#FFF1F2">LJ</span><div><strong>Little Joy</strong><span class="m">Toys · ★ 4.8</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a></li><li><a class="srow" href="#"><span class="logo-badge" style="background:#ECFDF5">PT</span><div><strong>Page Turner</strong><span class="m">Books · ★ 4.9</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a></li><li><a class="srow" href="#"><span class="logo-badge" style="background:#FFFBEB">FB</span><div><strong>Fresh Basket</strong><span class="m">Grocery · ★ 4.5</span></div><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></a></li></ul>
</div></section>

<div class="wrap"><section id="sell" class="cta">
  <div><h2>Open your store on Cj bazar</h2><p>Reach thousands of buyers. No setup fees, no monthly fees.</p></div>
  <router-link class="btn" to="/signup">Start selling — it's free</router-link>
</section></div>
</main>

<footer><div class="wrap">
  <a class="brand" href="#" aria-label="Cj bazar home"><svg width="30" height="30" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#2F5BEA"/><path d="M12 15h16l-1.2 14a2 2 0 0 1-2 1.8h-9.6a2 2 0 0 1-2-1.8z" fill="#fff"/><path d="M16 17v-3a4 4 0 0 1 8 0v3" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg><span>Cj <b>bazar</b></span></a>
  <span class="copy">© 2026 Cj bazar</span>
  <nav aria-label="Footer"><a href="#">About</a><a href="#">Help center</a><a href="#">Shipping</a><a href="#">Returns</a><a href="#">Privacy</a><a href="#">Terms</a></nav>
</div></footer>
</div>
</template>

<script>
import HeroSearchBar from '@/components/helperComponents/hero-search-bar.vue';

export default {
  name: 'MarketplaceLanding',
  components: { HeroSearchBar },
  methods: {
    toggleHeart(e) {
      const b = e.target.closest('.heart');
      if (b) b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.cj{--accent:#2F5BEA;--accent-dark:#2447C4;--accent-soft:#EEF2FF;--dark:#0B1220;--text:#111827;--muted:#6B7280;--border:#EAECF0;--radius:14px}
*{box-sizing:border-box}
.cj{display:block;width:100%;height:auto;margin:0;overflow-x:clip;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--text);background:#fff;line-height:1.5;-webkit-font-smoothing:antialiased}
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

/* header */
.hdr{position:sticky;top:0;z-index:50;height:68px;background:#fff;border-bottom:1px solid var(--border)}
.hdr .wrap{height:100%;display:flex;align-items:center;gap:32px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:22px;letter-spacing:-.02em}
.brand b{color:var(--accent)}
.nav{display:flex;gap:4px;flex:1}
.nav a{padding:8px 12px;border-radius:10px;font-weight:500;font-size:15px}
.nav a:hover{background:var(--accent-soft);color:var(--accent)}
.nav a.sell{color:var(--accent);font-weight:600}
.actions{display:flex;gap:4px;margin-left:auto}
.ibtn{position:relative;width:44px;height:44px;display:grid;place-items:center;border:0;background:none;border-radius:12px;cursor:pointer;color:var(--text)}
.ibtn:hover{background:var(--accent-soft);color:var(--accent)}
.badge{position:absolute;top:4px;right:2px;min-width:18px;height:18px;padding:0 5px;border-radius:9px;background:var(--accent);color:#fff;font-size:11px;font-weight:700;display:grid;place-items:center}

/* hero */
.hero{position:relative;height:620px;overflow:hidden;background:var(--dark);isolation:isolate;padding:0}
.rows{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:18px}
.track{display:flex;width:max-content;will-change:transform}
.track.l{animation:left 48s linear infinite}
.track.r{animation:right 56s linear infinite}
@keyframes left{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@keyframes right{from{transform:translateX(-50%)}to{transform:translateX(0)}}
.hero:hover .track{animation-play-state:paused}
@media (prefers-reduced-motion:reduce){.track{animation-play-state:paused!important}}
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

/* sections */
section.s{padding:48px 0 0}
.sh{display:flex;align-items:center;gap:12px;margin-bottom:22px}
.sh h2{font-size:26px;font-weight:800;letter-spacing:-.02em}
.sh .chip{font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent-dark)}
.sh .all{margin-left:auto;font-weight:600;color:var(--accent-dark);font-size:15px;white-space:nowrap}
.sh .all:hover{text-decoration:underline}
.cats{display:grid;grid-template-columns:repeat(8,1fr);gap:12px}
.cat{display:flex;flex-direction:column;align-items:center;gap:8px;padding:18px 8px;border-radius:var(--radius);border:1px solid transparent;text-align:center;transition:background .15s,border-color .15s}
.cat:hover{background:var(--accent-soft);border-color:#D6E0FF}
.cat .c{width:56px;height:56px;border-radius:50%;display:grid;place-items:center;color:var(--accent)}
.cat strong{font-size:14px}
.cat span.n{font-size:12px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:18px}
.card{position:relative;background:#fff;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:transform .18s,box-shadow .18s}
.card:hover,.card:focus-within{transform:translateY(-2px);box-shadow:0 10px 24px rgba(16,24,40,.1)}
.card-img{display:block;position:relative;aspect-ratio:1;background:#F3F4F6}
.card-img img{width:100%;height:100%;object-fit:cover}
.tag{position:absolute;top:10px;left:10px;font-size:12px;font-weight:700;padding:3px 9px;border-radius:8px}
.tag-sale{background:#C81E1E;color:#fff}.tag-new{background:var(--accent-dark);color:#fff}.tag-best{background:#FDE68A;color:#78350F}
.heart{position:absolute;top:8px;right:8px;width:36px;height:36px;border-radius:50%;border:0;background:rgba(255,255,255,.95);display:grid;place-items:center;cursor:pointer;color:var(--text);box-shadow:0 1px 4px rgba(0,0,0,.15)}
.heart svg{width:18px;height:18px}
.heart:hover{color:#C81E1E}
.heart[aria-pressed=true]{color:#C81E1E}.heart[aria-pressed=true] svg{fill:currentColor}
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
.price s{font-size:13px;color:var(--muted)}
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

@media (max-width:1100px){.grid{grid-template-columns:repeat(3,1fr)}.stores{grid-template-columns:repeat(2,1fr)}}
@media (max-width:860px){
  .nav{display:none}
  .hero{height:auto;min-height:620px;display:flex}
  .fg{height:auto;flex:1;padding:56px 16px}
  .sh .all{font-size:14px}
  .hdr .wrap{gap:12px}
  .fg h1{font-size:34px}
  .sub{font-size:16px}
  .trust ul{grid-template-columns:repeat(2,1fr)}
  .cats{grid-template-columns:repeat(4,1fr)}
  .grid{grid-template-columns:repeat(2,1fr);gap:12px}
  .cta{flex-direction:column;align-items:flex-start;padding:32px 24px}
  footer nav{margin-left:0}
}
@media (max-width:480px){.brand{font-size:20px}.ibtn{width:40px}.pcard{width:170px;height:210px}.scard{width:260px;height:150px}.cta h2{font-size:24px}.cta .btn{width:100%}.cats{gap:4px}.cat strong{font-size:13px}.wrap{padding:0 16px}.stores{grid-template-columns:1fr}.sh h2{font-size:22px}.sh{flex-wrap:wrap}}
</style>
