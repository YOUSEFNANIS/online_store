<template>
  <div class="cart-container">
    
    <!-- Scrollable products list -->
    <div class="cart-items">

      <div class="cart-item" v-for="(item,index) in cartData" :key="index">

        <!-- Product Image -->
        <div class="product-img">
          <img :src="item.first_image" :alt="item.product_name">
        </div>
        <div class="product-info">
          <div class="product-name">{{ item.product_name }}</div>
          <div class="product-price">{{ item.price }}</div>
        </div>
        <!-- Quantity Controls -->
        <div class="qty-controls">
          <button :aria-label="$t('cart.decrease')" @click="decreaseQty(index)">-</button>
          <span class="qty">{{ item.quantity }}</span>
          <button :aria-label="$t('cart.increase')" @click="increaseQty(index)">+</button>
        </div>
        <!-- Remove Item -->
        <button class="remove-btn" :aria-label="$t('cart.remove')" @click="removeItem(index)">✕</button>

      </div>

    </div>

    <div class="cart-actions">
    <button class="btn btn-cta" @click="orderNow">
      {{ $t('cart.orderNow') }}
    </button>
    <button class="btn btn-outline" @click="save">
      {{ $t('cart.save') }}
    </button>
    </div>
  </div>
</template>

<script>
import api, { API_URL } from './services/api';

export default {
  name: "CartComponent",
  mounted(){
    this.retreiveItems()
  },
  data() {
    return {
      cartData: [],
      cart_id: null,
    }
  },

  methods: {
    increaseQty(index) {
      this.cartData[index].quantity +=1
    },
    decreaseQty(index) {
      // Server rejects quantities below 1; use remove to drop an item.
      if (this.cartData[index].quantity > 1) this.cartData[index].quantity -=1
    },
    async removeItem(index) {
      try {const url = '/core/cart/' + this.cart_id + '/cartitem/' + this.cartData[index].id + '/' 
      const response = await api.delete(url)
      delete this.cartData[index]
      }
      catch(error){
        console.log(error)
      }
    },
    orderNow(){
      this.$router.push('/order')
      this.$emit('close')

    },
    async save() {
      for (const i in this.cartData){
        const url = '/core/cart/' + this.cart_id + '/cartitem/' + this.cartData[i].id + '/' 
        const response = await api.patch(url, {'quantity': this.cartData[i].quantity})
        
      }
      this.$emit('close')
    },
    async retreiveItems(){
      try{const response = await api.get('/core/cart/')

      const data = response.data[0].cart_item_set
      this.cart_id = response.data[0].id
      this.cartData = {
  ...this.cartData, // Keep the original structure
  ...response.data[0].cart_item_set     // Add and overwrite with everything from result
}   
    const baseUrl = API_URL
    for (const i in this.cartData){

      this.cartData[i].first_image = baseUrl + this.cartData[i].first_image
    }
    
    }
      catch(error){
        console.log(error)
      }
    }
  }
}
</script>

<style scoped>
.cart-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  width: 500px;
  max-width: calc(100vw - 24px);
  max-height: 95vh;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.cart-items {
  width: 100%;
  max-height: 620px;
  overflow-y: auto;
}
.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto;
  align-items: center;
  gap: 12px;
  padding-bottom: 14px;
  margin-bottom: 14px;
  border-bottom: 1px solid var(--color-border);
}
.product-img {
  width: 80px;
  background: var(--color-bg);
  border-radius: var(--radius-sm);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.product-img img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.product-info { margin-inline-start: 8px; min-width: 0; }
.product-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
}
.product-price {
  font-size: 0.9rem;
  color: var(--color-text-muted);
}
.qty-controls {
  display: flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}
.qty-controls button {
  background: var(--color-surface);
  color: var(--color-text);
  border: none;
  width: 40px;
  height: 40px;
  font-size: 1.1rem;
  transition: background var(--transition);
}
.qty-controls button:hover { background: var(--color-bg); }
.qty {
  min-width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text);
}
.remove-btn {
  min-width: 40px;
  min-height: 40px;
  background: transparent;
  color: var(--color-text-muted);
  border: none;
  border-radius: var(--radius-sm);
  transition: color var(--transition), background var(--transition);
}
.remove-btn:hover { color: var(--color-error); background: var(--color-error-soft); }
.cart-actions { display: flex; gap: 10px; }
@media (max-width: 480px) {
  .cart-container { padding: 16px; }
  .cart-item { grid-template-columns: 64px 1fr auto; }
  .remove-btn { grid-column: 3; grid-row: 1; }
  .qty-controls { grid-column: 2 / 4; }
  .product-img { width: 64px; }
}
</style>
