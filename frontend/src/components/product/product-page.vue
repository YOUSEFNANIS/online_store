<template>
  <div>
    <load-component v-if="loading" />
  <div v-else class="product-page">
    
    <div class="image-section">
      <div class="slider-wrapper">
        <button class="arrow-btn left" @click="prevImage">❮</button>
        
        <transition name="fade" mode="out-in">
          <img 
            :key="activeIndex"
            :src="product.images[activeIndex]?.image" 
            class="main-display-image" 
          />
        </transition>

        <button class="arrow-btn right" @click="nextImage">❯</button>
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
      <div class="price-box">دينار {{ product.price }}</div>
      
      <hr class="soft-line" />

      <div class="description-box">
        <h2>وصف المنتج</h2>
        <h3>{{ product.description }}</h3>
      </div>
      <div class="btn-group">
        <button class="btn" @click="createOrder">اطلب الآن</button>
        <button class="btn" @click="addToCart">اضف إلى السلة</button>
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
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #000; /* Matches your black button theme */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.product-page {
  display: flex;
  width: 100%;
  margin: 40px auto;
  margin: 7%;
  gap: 30px;
}

.btn-group{
  gap: 20px;
  display: flex;
  justify-content: center;
}
.image-section {
  display: flex;
  width: 60%;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
}

.slider-wrapper {
  position: relative;
  width: 100%;
  border: 1px solid #eee; /* Light stroke */
  border-radius: 4px;
}

.main-display-image {
  width: 100%;
  height: 400px;
  object-fit: contain;
}

.arrow-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.7);
  border: 1px solid #ddd;
  cursor: pointer;
  padding: 10px;
}

.left { left: 10px; }
.right { right: 10px; }

/* Dots and Thumbnails */
.dots-container { margin: 15px 0; display: flex; gap: 8px; }
.dot { width: 8px; height: 8px; background: #ddd; border-radius: 50%; }
.dot.active { background: #888; }

.thumbnails-grid { display: flex; gap: 10px; }
.thumb-item { width: 60px; height: 60px; border: 1px solid #eee; cursor: pointer; }
.thumb-item.selected { border-color: #000; }

/* The Divider */
.vertical-divider {
  width: 6px;
  background: #f0f0f0; /* Soft gray bar */
}

/* Details Section */
.details-section {
  flex: 1;
  text-align: right;
  right: 0;
  direction: rtl;
}

.name-box, .price-box {
  padding: 5px;
  margin-bottom: 5px;
}

.description-box {
  padding: 0px 25px 25px 15px;
  border: 1px solid  #383838;
  margin-bottom: 25px;
}

.soft-line { border: 0; border-top: 1px solid #eee; margin: 20px 0; }

/* Animation */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>