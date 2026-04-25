<template>
  <div class="cart-container">
    
    <!-- Scrollable products list -->
    <div class="cart-items">

      <div class="cart-item" v-for="(item,index) in cartData" :key="index">

        <!-- Product Image -->
        <div class="product-img">
          <img :src="item.first_image">
        </div>
        <div class="product-info">
          <div class="product-name">{{ item.product_name }}</div>
          <div class="product-price">{{ item.price }}</div>
        </div>
        <!-- Quantity Controls -->
        <div class="qty-controls">
          <button @click="decreaseQty(index)">-</button>
          <span class="qty">{{ item.quantity }}</span>
          <button @click="increaseQty(index)">+</button>
        </div>
        <!-- Remove Item -->
        <button class="remove-btn" @click="removeItem(index)">✕</button>

      </div>

    </div>

    <div>
    <button class="btn" @click="orderNow">
      order now
    </button>
    <button class="btn" @click="save">
      save
    </button>
    </div>
  </div>
</template>

<script>
import api from './services/api';

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
      this.cartData[index].quantity -=1
    },
    async removeItem(index) {
      try {const url = 'http://127.0.0.1:8000/core/cart/' + this.cart_id + '/cartitem/' + this.cartData[index].id + '/' 
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
        const url = 'http://127.0.0.1:8000/core/cart/' + this.cart_id + '/cartitem/' + this.cartData[i].id + '/' 
        const response = await api.patch(url, {'quantity': this.cartData[i].quantity})
        
      }
      this.$emit('close')
    },
    async retreiveItems(){
      try{const response = await api.get('http://127.0.0.1:8000/core/cart/')

      const data = response.data[0].cart_item_set
      this.cart_id = response.data[0].id
      this.cartData = {
  ...this.cartData, // Keep the original structure
  ...response.data[0].cart_item_set     // Add and overwrite with everything from result
}   
    const baseUrl = 'http://127.0.0.1:8000'
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

.cart-container{
  position: fixed;

  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  z-index: 9999;

  width: 500px;
  max-height: 95vh;

  background:#e9e9e9;
  padding:25px;
  box-shadow:0 10px 25px rgba(0,0,0,0.2);

  display:flex;
  flex-direction:column;
  align-items:center;
}

/* Scrollable area */
.cart-items{
  width:100%;
  max-height:620px;
  overflow-y:auto;
}

/* Cart item */
.cart-item{
  display:grid;
  grid-template-columns:80px 1fr auto auto;
  align-items:center;
  gap:12px;
  margin-bottom:18px;
}

/* Image placeholder */
.product-img{
  width:90px;
  background:#cfcfcf;
  display:flex;
  align-items:center;
  justify-content:center;
}
.product-img img{
  max-width:100%;
  max-height:100%;
  object-fit:contain;
}
/* Product info */
.product-info {
  margin-left: 20px;
  flex-direction:column; /* pushes text to the right */
}

.product-name{
  font-size:18px;
}

.product-price{
  font-size:14px;
  color:#555;
}

/* Quantity buttons */
.qty-controls{
  display:flex;
  border:1px solid #333;
}

.qty-controls button{
  background:white;
  border:none;
  width:28px;
  height:28px;
  cursor:pointer;
}

.qty{
  width:30px;
  display:flex;
  align-items:center;
  justify-content:center;
}

/* Remove button */


</style>