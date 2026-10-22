<template>
    <div class="order-container">
      <div class="order-form">
    <h2>{{ $t('createOrder.title') }}</h2>

    <form @submit.prevent="confirm_order">

      <label class="field-label" for="order-location">{{ $t('createOrder.location') }}</label>
      <input id="order-location" type="text" :placeholder="$t('createOrder.location')" v-model="location" :aria-invalid="!!locationError" @input="locationError = false"/>
      <p v-if="locationError" class="field-error" role="alert">{{ $t('createOrder.locationRequired') }}</p>

      <button type="submit" class="btn btn-cta submit-btn">
        {{ $t('createOrder.confirm') }}
      </button>
    </form>
  </div>
  <div class="cart-items">

      <div class="cart-item" v-for="(item,index) in data" :key="index">

        <!-- Product Image -->
        <div class="left">
          <div class="product-img">
            <img :src="item.first_image">
          </div>
          <div class="product-info">
            <div class="product-name">{{ item.product_name }}</div>
            <div class="product-price">{{ item.price }}</div>
          </div>
        </div>
        <div class="item-details">
        <!-- Quantity Controls -->
        <div class="qty-controls">
          <button type="button" :aria-label="$t('createOrder.decrease')" @click="decreaseQty(index)">-</button>
          <span class="qty">{{ item.quantity }}</span>
          <button type="button" :aria-label="$t('createOrder.increase')" @click="increaseQty(index)">+</button>
        </div>
        <!-- Remove Item -->
        <button type="button" class="remove-btn" :aria-label="$t('createOrder.remove')" @click="removeItem(index)">✕</button>
      </div>
      </div>
      <div class="price-container">
      <div class="top-line"></div>

      <div class="price-row">
        <span class="label">{{ $t('createOrder.totalPrice') }}</span>
        <span class="value">{{ total_value }} {{ $t('createOrder.currency') }}</span>
      </div>
    </div>
  </div>
  
  
</div>

</template>
<script>
import api, { API_URL } from '@/services/api';

export default {
    mounted(){
      this.retreive_items()
    },
    
    data(){
        return {
            location: '',
            locationError: false,
            data: {},
        }
    },
    computed:{
  total_value(){
    let total = 0
    
    for (const i in this.data){
      total += this.data[i].price * this.data[i].quantity
    }
    return total
  }
},
    methods:{
      increaseQty(index) {
      this.data[index].quantity +=1
    },
    decreaseQty(index) {
      this.data[index].quantity -=1
    },
      async retreive_items(){
        try{
          const response = await api.get('/core/cart/')
        this.data = {
        ...this.data, // Keep the original structure
        ...response.data[0].cart_item_set     // Add and overwrite with everything from result
        };
      
      // this.cart_id = response.data[0].id
      const baseUrl = API_URL
      for (const i in this.data){

      this.data[i].first_image = baseUrl + this.data[i].first_image
    }
    }
      catch(error){
        console.log(error)
      }
      },

      async confirm_order(){
            if (!this.location.trim()) {
              this.locationError = true
              return
            }
            try{const response = await api.post('/core/orders/', {'location': this.location, 'total_value': this.total_value})
            this.$router.push({path:'/thankyou'})}
            catch(error){
              console.log(error.response)
            }
      }
    },
}
</script>
<style scoped>
.order-container {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  max-width: 1000px;
  margin: 6rem auto 2rem;
  padding: 2rem 1rem;
  flex-direction: row;
  flex-wrap: wrap;
  color: var(--color-text);
}
.order-form {
  flex: 1 1 280px;
  max-width: 360px;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.order-form h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 1rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}
.field-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text);
}
input {
  width: 100%;
  min-height: 40px;
}
.field-error {
  margin: 0;
  font-size: 0.875rem;
  color: var(--color-error);
}
input[aria-invalid="true"] { border-color: var(--color-error); }
.submit-btn {
  width: 100%;
  margin-top: 0.5rem;
}
.cart-items {
  flex: 2 1 340px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.cart-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}
.left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.item-details {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.product-img {
  width: 72px;
  height: 72px;
  background: var(--color-bg);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.product-img img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.product-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.product-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
}
.product-price {
  font-size: 0.875rem;
  color: var(--color-text-muted);
}
.qty-controls {
  display: flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  overflow: hidden;
}
.qty-controls button {
  background: var(--color-surface);
  color: var(--color-text);
  border: none;
  min-width: 40px;
  min-height: 40px;
  font-size: 1.1rem;
  transition: background var(--transition);
}
.qty-controls button:hover { background: var(--color-bg); }
.qty {
  min-width: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}
.remove-btn {
  min-width: 40px;
  min-height: 40px;
  background: var(--color-surface);
  color: var(--color-error);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  transition: background var(--transition), border-color var(--transition);
}
.remove-btn:hover {
  background: var(--color-error-soft);
  border-color: var(--color-error);
}
.price-container {
  width: 100%;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
}
.top-line { display: none; }
.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.125rem;
}
.label {
  text-transform: lowercase;
  color: var(--color-text-muted);
  font-weight: 600;
}
.value {
  font-weight: 700;
  color: var(--color-text);
}
@media (max-width: 700px) {
  .order-container { margin-top: 4rem; }
  .order-form { max-width: none; }
}
</style>
