<template>
    <div class="order-container">
      <div class="order-form">
    <h2>قم بإدخال عنوانك</h2>

    <form @submit.prevent="confirm_order">
        
      <input type="text" placeholder="الموقع"  v-model="location" style="background-color: white;"/>

      <button type="submit" class="submit-btn">
        تأكيد الطلب
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
          <button @click="decreaseQty(index)">-</button>
          <span class="qty">{{ item.quantity }}</span>
          <button @click="increaseQty(index)">+</button>
        </div>
        <!-- Remove Item -->
        <button class="remove-btn" @click="removeItem(index)">✕</button>
      </div>
      </div>
      <div class="price-container">
      <div class="top-line"></div>

      <div class="price-row">
        <span class="label">total price:</span>
        <span class="value">{{ total_value }} LYD</span>
      </div>
    </div>
  </div>
  
  
</div>

</template>
<script>
import api from '@/services/api';

export default {
    mounted(){
      this.retreive_items()
    },
    
    data(){
        return {
            location: '',
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
          const response = await api.get('http://127.0.0.1:8000/core/cart/')
        this.data = {
        ...this.data, // Keep the original structure
        ...response.data[0].cart_item_set     // Add and overwrite with everything from result
        };
      
      // this.cart_id = response.data[0].id
      const baseUrl = "http://127.0.0.1:8000"
      for (const i in this.data){

      this.data[i].first_image = baseUrl + this.data[i].first_image
    }
    }
      catch(error){
        console.log(error)
      }
      },

      async confirm_order(){
            try{const response = await api.post('http://127.0.0.1:8000/core/orders/', {'location': this.location, 'total_value': this.total_value})
            this.$router.push({path:'/thankyou'})}
            catch(error){
              console.log(error.response)
            }
      }
    },
}
</script>
.body{
  color: #aeaeae;
}
<style scoped>

.order-container {
  display: flex;
  font-weight: bold;
  align-items: center;
  max-width: 70%;
  flex-direction: row;
  margin: 8% auto 8% 5%; 
  padding: 100px 20px;
  animation: pageFade 0.6s ease;
}

@keyframes pageFade {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.full-name {
  width: 370px;
  gap: 10px;
  display: flex; 
  flex-direction: row; 
}
/* Main container for the form */
.order-form { 
  width: 30%;
  max-width: 300px;
  height: 30%;
  display: flex;
  flex-direction: column; 
  padding: 30px 20px 20px 20px; 
  
  background: #003cff;
  margin: auto;
  direction: rtl; 
  align-items: center; 
  
  /* REINSTATED: Original animation transition */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
/* Internal form wrapper */
form { 
  display: flex; 
  flex-direction: column; 
  gap: 15px; 
  width: 100%; 
  align-items: center; 
  
}

/* Title Styling */
.order-form h2 {
  font-size: 24px;
  color: white;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  padding: 12px;
  font-size: 15px;
  width: 85%;
  transition: 0.3s;
}

input:focus {
  outline: none;
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.submit-btn {
  width: 65%; /* Adjusted for the look in your image */
  padding: 14px;
  border: none;
  background: black;
  color: white;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  
  /* REINSTATED: Original button animations */
  transition: 0.2s ease;
}

.submit-btn:hover {
  background: #333;
  transform: translateY(-2px);
}

.submit-btn:active {
  transform: translateY(0px) scale(0.97);
}
/* RIGHT - SUMMARY */
.cart-items{
  width:20%;
  max-width: 400px;
  margin: auto;
  display: flex;
  gap: 20px;
  flex-direction: column; /* Aligns the products horizontally */
  flex-wrap: wrap;
}

/* Cart item */
.cart-item{
  display: flex;
  align-items: center;
  justify-content: space-between; /* important */
  gap: 16px;
}
.left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.item-details {
  display: flex;
  justify-content: center;
  gap: 10px;
}
.product-img{
  width:90px;
  background:#cfcfcf;
  display:flex;
  margin-right: 10%;
  justify-content:center;
}
.product-img img{
  max-width:100%;
  max-height:100%;
  object-fit:contain;
}
/* Product info */
.product-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
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
.price-container {
  width: 400px;
  background: #ffffff;
  padding: 20px;
}

.top-line {
  width: 100%;
  height: 3px;
  background: black;
  margin-bottom: 15px;
}

.price-row {
  display: flex;
  justify-content: center; /* Pushes items to opposite ends */   /* Recreates the line in your image */
  padding-top: 10px;
  font-size: 20px;
}

.label {
  text-transform: lowercase;
  margin: auto 10%;
  font-weight: bold;
}

.value {
  font-weight: 500;
  font-weight: bold;
  margin: auto 10%;
}

</style>