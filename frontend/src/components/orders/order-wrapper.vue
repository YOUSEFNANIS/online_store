<template>
    <div>
        <div class="shopify-container">
            <SellerOrders v-if="user_type === 'seller'"/>
            <CustomerOrders v-else/>
            
        </div>
        
  </div>
</template>
<script>
import SellerOrders from './seller-orders.vue';
import CustomerOrders from './customer-orders.vue';
import { useRoleStore } from '@/stores/role'

export default {
    
    components: { SellerOrders, CustomerOrders},
    computed: {
        user_type(){
            const store = useRoleStore();
            return store.role;
        }
    },
}
</script>
<style scoped>
.shopify-container {
  max-width: 100%;
  margin: 7% auto;
  padding: 0 20px;
  color: #1a1a1a;
  justify-content: center;
  font-size: 1rem;
}
</style>