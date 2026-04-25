import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import CreateOrder from './components/orders/create-order.vue'
import ThankYou from './components/helperComponents/thank-you.vue'
import ProductPage from './components/product/product-page.vue'
import LoadComponent from './components/helperComponents/load-component.vue'
import ChatBot from './chat-bot.vue'
import NavBar from './components/helperComponents/nav-bar.vue'
import CreateProduct from './components/product/create-product.vue'
import showCart from './show-cart.vue'
import CustomerSettings from './components/users/customer-settings.vue'
import EditProduct from './components/product/edit-product.vue'
import OrderWrapper from './components/orders/order-wrapper.vue'
import SellerDashboard from './components/users/seller-dashboard.vue'
import LandingPage from './components/landing-page.vue'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.component('LandingPage', LandingPage)
app.component('SellerDashboard', SellerDashboard)
app.component('OrderWrapper', OrderWrapper)
app.component('EditProduct', EditProduct)
app.component('ProductPage', ProductPage)
app.component('CreateOrder', CreateOrder)
app.component('ThankYou', ThankYou)
app.component('LoadComponent', LoadComponent)
app.component('ChatBot', ChatBot)
app.component('NavBar', NavBar)
app.component('CreateProduct', CreateProduct)
app.component('ShowCart', showCart)
app.component('CustomerSettings', CustomerSettings)
app.use(router)



app.mount('#app')
