<template>
  <div>
    <load-component v-if="loading" />
  <div v-else class="product-page">
    
    <div class="image-section">
      <div class="slider-wrapper">
        <button class="arrow-btn left" :aria-label="$t('productPage.previous')" @click="prevImage">❮</button>
        
        <transition name="fade" mode="out-in">
          <img 
            :key="activeIndex"
            :src="product.images[activeIndex]?.image" 
            class="main-display-image" 
          />
        </transition>

        <button class="arrow-btn right" :aria-label="$t('productPage.next')" @click="nextImage">❯</button>
      </div>

      <div class="dots-container">
        <span 
          v-for="(dot, i) in product.images" 
          :key="i" 
          class="dot" 
          :class="{ active: i === activeIndex }"
        ></span>
      </div>

      <div class="thumbnails-grid">
        <img 
          v-for="(img, i) in product.images" 
          :key="i" 
          :src="img.image" 
          class="thumb-item"
          :class="{ selected: i === activeIndex }"
          @click="activeIndex = i"
        />
      </div>
    </div>
    <div class="vertical-divider"></div>

    <div class="details-section">
      <h1 class="name-box">{{ product.name }}</h1>
      <div class="price-box">{{ $t('productPage.currency') }} {{ product.price }}</div>
      
      <hr class="soft-line" />

      <div class="description-box">
        <h2>{{ $t('productPage.description') }}</h2>
        <h3>{{ product.description }}</h3>
      </div>
      <div class="btn-group">
        <button class="btn btn-cta" @click="createOrder">{{ $t('productPage.orderNow') }}</button>
        <button class="btn btn-outline" @click="addToCart">{{ $t('productPage.addToCart') }}</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import api from '@/services/api';
export default {
    data(){
        return {
            product: {name: '',
                      description: '',
                      price: 0.0,
                      id: null,
                      images: []},
            activeIndex: 0,
            loading: false,
        }
    },
    mounted(){
      this.getdata();
    },
    
    methods: {
      async getdata(){
        this.loading = true;

        const url = 'http://127.0.0.1:8000/core/products/' + this.$route.params.productId + '/';
        const response = await api.get(url);
        this.product = response.data;
        console.log(this.product)
        this.loading = false;
      },
      nextImage() {
            this.activeIndex = (this.activeIndex + 1) % this.product.images.length;
        },
        prevImage() {
            this.activeIndex = (this.activeIndex - 1 + this.product.images.length) % this.product.images.length;
        },
      async addToCart(){
        
          const cart = await api.get('http://127.0.0.1:8000/core/cart/')
          const url = 'http://127.0.0.1:8000/core/cart/' + cart.data[0].id + '/cartitem/'
          console.log(url)
          const response = await api.post(url, {'product': this.product.id, 'quantity': 1, 'cart': cart.data[0].id})
      },
      async createOrder(){
          this.addToCart()
          this.$router.push('/order')
      }
    }
}
</script>


<style scoped>
.product-page {
  display: flex;
  width: auto;
  margin: 40px 7%;
  gap: 32px;
}

.btn-group { gap: 12px; display: flex; justify-content: center; flex-wrap: wrap; }
.btn-group .btn { flex: 1 1 160px; min-height: 44px; }

.image-section { display: flex; width: 60%; flex-direction: column; align-items: center; overflow: hidden; }

.slider-wrapper {
  position: relative;
  width: 100%;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.main-display-image { width: 100%; height: 400px; object-fit: contain; }

.arrow-btn {
  position: absolute; top: 50%; transform: translateY(-50%);
  min-width: 40px; min-height: 40px; padding: 0 10px;
  background: var(--color-surface); color: var(--color-text);
  border: 1px solid var(--color-border); border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  transition: border-color var(--transition), color var(--transition);
}
.arrow-btn:hover { border-color: var(--color-primary); color: var(--color-primary); }
.left { inset-inline-start: 10px; }
.right { inset-inline-end: 10px; }
[dir=rtl] .arrow-btn { transform: translateY(-50%) scaleX(-1); }

.dots-container { margin: 16px 0; display: flex; gap: 8px; }
.dot { width: 8px; height: 8px; background: var(--color-border); border-radius: 50%; }
.dot.active { background: var(--color-primary); }

.thumbnails-grid { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
.thumb-item {
  width: 60px; height: 60px; object-fit: cover; cursor: pointer;
  border: 2px solid var(--color-border); border-radius: var(--radius-sm);
  transition: border-color var(--transition);
}
.thumb-item:hover { border-color: var(--color-text-muted); }
.thumb-item.selected { border-color: var(--color-primary); }

.vertical-divider { width: 1px; background: var(--color-border); }

.details-section { flex: 1; text-align: start; }
.name-box { padding: 5px; margin: 0 0 5px; font-size: 1.75rem; color: var(--color-text); }
.price-box { padding: 5px; margin-bottom: 5px; font-size: 1.5rem; font-weight: 700; color: var(--color-text); }

.description-box {
  padding: 0 20px 20px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  margin-bottom: 24px;
}
.description-box h2 { font-size: 1.15rem; color: var(--color-text); }
.description-box h3 { font-size: 1rem; font-weight: 400; color: var(--color-text-muted); line-height: 1.7; }

.soft-line { border: 0; border-top: 1px solid var(--color-border); margin: 20px 0; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 800px) {
  .product-page { flex-direction: column; margin: 24px 16px; }
  .image-section { width: 100%; }
  .vertical-divider { display: none; }
  .main-display-image { height: 280px; }
}
</style>
