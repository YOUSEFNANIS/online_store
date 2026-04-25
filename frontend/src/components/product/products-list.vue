<template>
  <div>
  <load-component v-if="loading"/>
  <div v-else class="catalog-container">

      <h1 style="font-weight: bold;">TREND PRODUCTS</h1>
    <div class="products-grid">
      <div 
        v-for="(product, index) in products" 
        :key="index" 
      >
          
          <div class="shopping-router-group">
            <router-link :to="`/products/${product.id}`" class="product-card">
              <img :src="product.images?.[0]?.image" class="product-thumbnail">
          <div class="product-info">
            <h2 class="product-name">{{ product.name }}</h2>
            <h2 class="product-price">{{ product.price }}LYD</h2>
          </div>
            </router-link>
          </div>

      </div>
    </div>
    </div>
    <div class="pagination">
    <button
      v-for="i in totalPages"
      :key="i"
      :class="['pagination-btn', { active: page === currentPage }]"
      @click="setPageParam(i)"
    >
    {{ i }}
    </button>
  </div>
  </div>
</template>

<script>
import api from '@/services/api';
import loadComponent from '../helperComponents/load-component.vue';
import { ShoppingCart } from '@lucide/vue';
export default {
  components: { loadComponent, ShoppingCart },
  
    data() {
        return {
          products: {},
            loading: false,
            totalPages: 0,
            params: {params: {
              search: null,
              page: null
            }}
        }
    },
    watch: {
  '$route.query.searchQuery': {
    immediate: true,
    handler(searchQuery) {
      if (!searchQuery) {
        this.products = this.getdata()
      } else {
        this.debouncedSearch(searchQuery)
      }
    }
  }
},
    methods: {
        debouncedSearch(searchQuery) {

      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.params.params.search = searchQuery;
        this.getdata()

      }, 300);
    },

    setPageParam(navPage){
      this.params.params.page = navPage
      this.getdata()
    },
        async getdata() {
          this.loading= true
            try {
                console.log(this.params)
                const response = await api.get('http://127.0.0.1:8000/core/products/', this.params);
                this.totalPages = response.data['total_pages']
                this.loading= false
                this.products = response.data['results'];
                this.params.params.search = null
                this.params.params.page = null
            } catch (error) {
              console.log(error)
            }
        },
        async addToCart(product){
          try{

            const cart = await api.get('http://127.0.0.1:8000/core/cart/')
            const url = 'http://127.0.0.1:8000/core/cart/' + cart.data[0].id + '/cartitem/'

            const response = await api.post(url, {'product': product.id, 'quantity': 1, 'cart': cart.data[0].id})
          }
          catch(error){
            console.log(error)
          }

        },
        goToPage(id) {
            // Navigates to the product detail page using the name
            const pagePath = id + '/';

            this.$router.push({ path: pagePath,
                query: {path: pagePath}
              });
        }
    },
}
</script>
<style scoped>
.catalog-container {
  width: 100%;
  align-items: center;
  margin: 3% 0;
  direction: rtl; /* Sets Arabic alignment */
}
.product-info {
  margin-bottom: 10px;
  align-items: left ;
  text-align: left;
}
/* HERO SECTION */
.hero-section {
  width: 100%;
  height: 300px;
  background: #fdffe1;
  border: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
  color: #888;
}

.product-thumbnail {
  width: 250px;
  height: 250px;
  object-fit: cover; /* This crops the image to fill the 200x200 area perfectly */
  border: 1px solid #ffffff;
}
/* GRID LAYOUT */
.products-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 25px;
  justify-content: center;
}

/* PRODUCT CARD */
.product-card {
  background: white;
  width: 250px;
  padding: 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Hover Animation */
.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}


.product-name {
  font-weight: bold;
  margin: 0;
  font-size: 1.8rem;
}

.product-price {
  margin: 5px 0 0;
  font-size: 1.3rem;
}
.order-btn {
  font-weight: bold;
  background-color: #000;
  font-size: 1.5rem;
  text-decoration: none;
  color: #fff;
  border: none;
  padding: 10px 10px;
  margin: 10px 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}
.shopping-router-group{
  display: inline-flex;
  padding: 10px;
  align-items: center;
  justify-content: center;
}
.order-btn:hover {
  opacity: 0.8;
}
</style>