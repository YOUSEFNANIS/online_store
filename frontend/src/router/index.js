import CreateOrder from '@/components/orders/create-order.vue'
import NotFound from '@/components/helperComponents/not-found.vue'
import ProductPage from '@/components/product/product-page.vue'
import ProductsList from '@/components/product/products-list.vue'
import ThankYou from '@/components/helperComponents/thank-you.vue'
import TermsOfUse from '@/components/helperComponents/terms-of-use.vue'
import { createRouter, createWebHistory } from 'vue-router'
import signupMainpage from '@/signup/signup-mainpage.vue'
import LogIn from '@/signup/log-in.vue'
import CreateProduct from '@/components/product/create-product.vue'
import { useRoleStore } from '@/stores/role'
import editOrder from '@/components/orders/edit-order.vue'
import CustomerSettings from '@/components/users/customer-settings.vue'
import EditProduct from '@/components/product/edit-product.vue'
import OrderWrapper from '@/components/orders/order-wrapper.vue'
import SellerDashboard from '@/components/users/seller-dashboard.vue'
import LandingPage from '@/components/landing-page.vue'
import SellersList from '@/components/product/sellers-list.vue'
import SellerStorefront from '@/components/product/seller-storefront.vue'
import ForgotPassword from '@/components/users/forgot-password.vue'
import ResetPassword from '@/components/users/reset-password.vue'
import VerifyEmail from '@/components/users/verify-email.vue'
import WishlistPage from '@/components/product/wishlist-page.vue'
import SellerEarnings from '@/components/users/seller-earnings.vue'
import SellerInventory from '@/components/users/seller-inventory.vue'
import MessagesPage from '@/components/messages/messages-page.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{path: '/', component: LandingPage},
    {path: '/dashboard', component: SellerDashboard, meta: {
      requiresSeller: true,
    }},
    {path: '/inventory', component: SellerInventory, meta: {
      requiresSeller: true,
    }},
    {path: '/earnings', component: SellerEarnings, meta: {
      requiresSeller: true,
    }},
    {path: '/landingpage', component: LandingPage},
    {path: '/products', component: ProductsList},
    {path: '/search', redirect: to => ({ path: '/products', query: to.query.q ? { searchQuery: to.query.q } : {} })},
    {path: '/sellers', component: SellersList, meta: {
      requiresCustomer: true,
    }},
    {path: '/sellers/:sellerId', component: SellerStorefront, meta: {
      requiresCustomer: true,
    }},
    {path: '/wishlist', component: WishlistPage, meta: {
      requiresCustomer: true,
    }},
    {path: '/forgot-password', component: ForgotPassword},
    {path: '/reset-password', component: ResetPassword},
    {path: '/verify-email', component: VerifyEmail},
    {path: '/signup', component: signupMainpage},
    {path: '/login', component: LogIn},
    {path: '/order', component: CreateOrder},
    {path: '/thankyou', component: ThankYou},
    {path: '/terms', component: TermsOfUse},
    {path: '/orderslist', component: OrderWrapper},
    {path: '/settings', component: CustomerSettings},
    {path: '/messages', component: MessagesPage},
    {path: '/products/create', component: CreateProduct, meta: { 
      requiresSeller: true,
    }},
    {path: '/:orderId/edit', component: editOrder, meta: { 
      requiresSeller: true,
    }},
    {path: '/products/:productId', component: ProductPage},
    {path: "/:pathMatch(.*)*", component: NotFound, name: 'NotFound'}
  ],
})

router.beforeEach((to, from, next) => {
  const userStore = useRoleStore()
  if (to.path === '/') {
    if (userStore.role === 'customer') {
      return next('/products')}
    else if (userStore.role === null){
      next()
    }
     else {
      return next('/dashboard')
    }
  }
  if (to.meta.requiresCustomer && userStore.role !== 'customer') {
    return next(userStore.role === null ? '/login' : '/')
  }
  if (to.meta.requiresSeller) {
    
    if (userStore.role==='seller') {
      next() // Permission granted
    } else {
      next('/:pathMatch(.*)*') // Redirect if parameter is false
    }
  } else {
    next() // Always allow non-restricted routes
  }
})

export default router
