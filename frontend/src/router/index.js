import { createRouter, createWebHistory } from 'vue-router'
import { useRoleStore } from '@/stores/role'

// Route-level dynamic imports keep unrelated pages and their dependencies out of
// the initial request chain. Vite turns each page into an on-demand chunk.
const LandingPage = () => import('@/components/landing-page.vue')
const SellerDashboard = () => import('@/components/users/seller-dashboard.vue')
const SellerInventory = () => import('@/components/users/seller-inventory.vue')
const SellerEarnings = () => import('@/components/users/seller-earnings.vue')
const ProductsList = () => import('@/components/product/products-list.vue')
const SellersList = () => import('@/components/product/sellers-list.vue')
const SellerStorefront = () => import('@/components/product/seller-storefront.vue')
const WishlistPage = () => import('@/components/product/wishlist-page.vue')
const ForgotPassword = () => import('@/components/users/forgot-password.vue')
const ResetPassword = () => import('@/components/users/reset-password.vue')
const VerifyEmail = () => import('@/components/users/verify-email.vue')
const SignupMainPage = () => import('@/signup/signup-mainpage.vue')
const LogIn = () => import('@/signup/log-in.vue')
const CreateOrder = () => import('@/components/orders/create-order.vue')
const ThankYou = () => import('@/components/helperComponents/thank-you.vue')
const TermsOfUse = () => import('@/components/helperComponents/terms-of-use.vue')
const OrderWrapper = () => import('@/components/orders/order-wrapper.vue')
const CustomerSettings = () => import('@/components/users/customer-settings.vue')
const MessagesPage = () => import('@/components/messages/messages-page.vue')
const CreateProduct = () => import('@/components/product/create-product.vue')
const EditOrder = () => import('@/components/orders/edit-order.vue')
const ProductPage = () => import('@/components/product/product-page.vue')
const NotFound = () => import('@/components/helperComponents/not-found.vue')

const defaultDescription = 'Shop products from independent sellers on YSF Store, discover new arrivals, and manage orders in one secure marketplace.'

const pageMeta = (title, description = defaultDescription, robots = 'index, follow') => ({
  title,
  description,
  robots,
})

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{path: '/', component: LandingPage, meta: pageMeta('YSF Store | Shop Independent Sellers')},
    {path: '/dashboard', component: SellerDashboard, meta: {
      requiresSeller: true,
      ...pageMeta('Seller Dashboard | YSF Store', 'Manage your YSF Store business, inventory, orders, and earnings.', 'noindex, nofollow'),
    }},
    {path: '/inventory', component: SellerInventory, meta: {
      requiresSeller: true,
      ...pageMeta('Inventory | YSF Store', 'Manage product inventory for your YSF Store business.', 'noindex, nofollow'),
    }},
    {path: '/earnings', component: SellerEarnings, meta: {
      requiresSeller: true,
      ...pageMeta('Earnings | YSF Store', 'Review earnings and sales activity for your YSF Store business.', 'noindex, nofollow'),
    }},
    {path: '/landingpage', component: LandingPage, meta: pageMeta('YSF Store | Shop Independent Sellers')},
    {path: '/products', component: ProductsList, meta: pageMeta('Browse Products | YSF Store', 'Browse products, explore categories, and discover new arrivals from independent sellers on YSF Store.')},
    {path: '/search', redirect: to => ({ path: '/products', query: to.query.q ? { searchQuery: to.query.q } : {} })},
    {path: '/sellers', component: SellersList, meta: {
      requiresCustomer: true,
      ...pageMeta('Explore Sellers | YSF Store', 'Discover independent sellers and browse their storefronts on YSF Store.'),
    }},
    {path: '/sellers/:sellerId', component: SellerStorefront, meta: {
      requiresCustomer: true,
      ...pageMeta('Seller Storefront | YSF Store', 'Browse products available from this independent seller on YSF Store.'),
    }},
    {path: '/wishlist', component: WishlistPage, meta: {
      requiresCustomer: true,
      ...pageMeta('Your Wishlist | YSF Store', 'View the products saved to your YSF Store wishlist.', 'noindex, nofollow'),
    }},
    {path: '/forgot-password', component: ForgotPassword, meta: pageMeta('Forgot Password | YSF Store', 'Request a secure password reset for your YSF Store account.', 'noindex, nofollow')},
    {path: '/reset-password', component: ResetPassword, meta: pageMeta('Reset Password | YSF Store', 'Create a new password for your YSF Store account.', 'noindex, nofollow')},
    {path: '/verify-email', component: VerifyEmail, meta: pageMeta('Verify Email | YSF Store', 'Verify the email address connected to your YSF Store account.', 'noindex, nofollow')},
    {path: '/signup', component: SignupMainPage, meta: pageMeta('Create an Account | YSF Store', 'Join YSF Store to shop from independent sellers or start selling your products.')},
    {path: '/login', component: LogIn, meta: pageMeta('Sign In | YSF Store', 'Sign in securely to your YSF Store account.', 'noindex, nofollow')},
    {path: '/order', component: CreateOrder, meta: pageMeta('Checkout | YSF Store', 'Review and place your order securely on YSF Store.', 'noindex, nofollow')},
    {path: '/thankyou', component: ThankYou, meta: pageMeta('Order Confirmed | YSF Store', 'Your YSF Store order has been received.', 'noindex, nofollow')},
    {path: '/terms', component: TermsOfUse, meta: pageMeta('Terms of Use | YSF Store', 'Read the terms that govern use of the YSF Store marketplace.')},
    {path: '/orderslist', component: OrderWrapper, meta: pageMeta('Your Orders | YSF Store', 'Track and manage your YSF Store orders.', 'noindex, nofollow')},
    {path: '/settings', component: CustomerSettings, meta: pageMeta('Account Settings | YSF Store', 'Manage your YSF Store account settings.', 'noindex, nofollow')},
    {path: '/messages', component: MessagesPage, meta: pageMeta('Messages | YSF Store', 'View your YSF Store conversations.', 'noindex, nofollow')},
    {path: '/products/create', component: CreateProduct, meta: { 
      requiresSeller: true,
      ...pageMeta('Add Product | YSF Store', 'Create a new product listing for your YSF Store business.', 'noindex, nofollow'),
    }},
    {path: '/:orderId/edit', component: EditOrder, meta: { 
      requiresSeller: true,
      ...pageMeta('Edit Order | YSF Store', 'Update an order in your YSF Store seller account.', 'noindex, nofollow'),
    }},
    {path: '/products/:productId', component: ProductPage, meta: pageMeta('Product Details | YSF Store', 'View product details, seller information, and customer reviews on YSF Store.')},
    {path: "/:pathMatch(.*)*", component: NotFound, name: 'NotFound', meta: pageMeta('Page Not Found | YSF Store', 'The requested YSF Store page could not be found.', 'noindex, nofollow')}
  ],
})

router.beforeEach((to, from, next) => {
  const userStore = useRoleStore()
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

router.afterEach((to) => {
  document.title = to.meta.title || 'YSF Store'

  const tags = {
    description: to.meta.description || defaultDescription,
    robots: to.meta.robots || 'index, follow',
  }

  Object.entries(tags).forEach(([name, content]) => {
    let element = document.head.querySelector(`meta[name="${name}"]`)
    if (!element) {
      element = document.createElement('meta')
      element.setAttribute('name', name)
      document.head.appendChild(element)
    }
    element.setAttribute('content', content)
  })
})

export default router
