<template>
  <div class="container">

    <div class="order-id-header">
      <h2>{{ $t('editOrder.orderId', { id: $route.params.orderId }) }}</h2>
      <h2>{{ customer_name }}</h2>
    </div>
    <div class="form-row">
        <input 
            type="text" 
            v-model="location" 
            class="laction-field"
            :aria-label="$t('editOrder.location')"
            :placeholder="$t('editOrder.location')"
        >

        <div class="price-row">
        <input 
            type="text" 
            :placeholder="$t('editOrder.totalPrice')"
            v-model="price"
            class="price-input"
            :aria-label="$t('editOrder.totalPrice')"
        >

        <span>{{ $t('editOrder.currency') }}</span>
    </div>
    </div>

    

    <div class="actions">
        <button @click="save" class="btn btn-primary">{{ $t('editOrder.save') }}</button>
        <button @click="handleCancel" class="btn btn-outline">{{ $t('editOrder.cancel') }}</button>
    </div>
  </div>
</template>
<script>
import api from '@/services/api';


    export default{
      mounted(){
        this.retreiveItems()
      },
        data() {
            return {
              id: this.$route.params.orderId,
              orderTemp: {},
              location: '',
              price: null,
              customer_name: null,
            }
        },
        methods: {
            async save() {
                try {
                  // 3. Send the PUT request to your backend
                  // Assuming your API expects: /orders/{id}/
                const response = await api.patch(`/core/orders/${this.id}/`, {'location': this.location, 'total_value': this.price});

                  // 4. (Optional) Redirect the user back to the list or details page
                this.$router.push('/orderslist'); 
                this.$emit('saved', true)

        } catch (error) {
            console.error("Error saving data:", error);
            alert(this.$t('editOrder.saveFailed'));
        }
            },
            handleCancel() {
                // Logic for resetting or closing goes here
            },
            
        }
    }

</script>

<style scoped>
.container {
  position: absolute;
  top: 30%;
  inset-inline-start: 50%;
  transform: translateX(-50%);
  width: min(700px, calc(100vw - 2rem));
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 2rem;
  z-index: 50;
}
.order-id-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 1.5rem;
}
.order-id-header h2 {
  margin: 0;
  padding: 0 0 1rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text);
}
.form-row {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
.laction-field { flex: 2; }
.price-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  color: var(--color-text-muted);
}
.price-row input { flex: 1; min-width: 0; }
.actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}
input { flex: 1; min-height: 40px; }
@media (max-width: 600px) {
  .form-row { flex-direction: column; align-items: stretch; gap: 1rem; }
}
</style>
