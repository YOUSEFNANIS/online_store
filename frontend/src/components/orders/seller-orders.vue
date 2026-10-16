<template>
  <div>
    <div class="card table-card">
      <table class="order-table">
        <thead>
          <tr>
            <th>{{ $t('sellerOrders.customer') }}</th>
            <th>{{ $t('sellerOrders.value') }}</th>
            <th>{{ $t('sellerOrders.date') }}</th>
            <th>{{ $t('sellerOrders.items') }}</th>
            <th>{{ $t('sellerOrders.location') }}</th>
            <th>{{ $t('sellerOrders.status') }}</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td class="bold">{{ order.customer_name }}</td>
            <td>{{ order.total_value }} {{ $t('sellerOrders.currency') }}</td>
            <td>{{ order.creation_date }}</td>
            <td>{{ order.total_quantity }}</td>
            <td>{{ order.location }}</td>
            <td>
              <span :class="['status-pill', order.order_status]">
                {{ statusLabel(order.order_status) }}
              </span>
            </td>
            <td>
              <span class="icon-btn" role="button" tabindex="0" @click="updateOrderPane(order)" @keydown.enter="updateOrderPane(order)" :title="$t('sellerOrders.editItem')" :aria-label="$t('sellerOrders.editItem')">
                <Pencil :title="$t('sellerOrders.edit')"/>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="showOrderPane" class="container">

    <div class="order-id-header">
      <!-- <h2>#order Id: {{ $route.params.orderId }}</h2> -->
      <h2>{{ orderTemp.customer_name }}</h2>
    </div>
    <div class="form-row">
        <input 
            type="text" 
            v-model="orderTemp.location" 
            class="laction-field"
            :aria-label="$t('sellerOrders.location')"
            :placeholder="$t('sellerOrders.location')"
        >

        <div class="price-row">
        <input 
            type="text" 
            :placeholder="$t('sellerOrders.totalPrice')"
            v-model="orderTemp.price"
            class="price-input"
            :aria-label="$t('sellerOrders.totalPrice')"
        >

        <span>{{ $t('sellerOrders.currency') }}</span>
    </div>
    </div>

    

    <div class="actions">
        <button @click="save" class="btn btn-primary">{{ $t('sellerOrders.save') }}</button>
        <button @click="handleCancel" class="btn btn-outline">{{ $t('sellerOrders.cancel') }}</button>
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
import { Pause, Pencil } from '@lucide/vue';

export default {
  components: {Pencil},
    mounted(){
      setTimeout(() => {
}, 3000)
        this.fetchOrders()
        this.$emit('loaded')
    },
    data(){
        return {
            orders: {},
            orderTemp: {},
            showOrderPane: false,
            params: {
                params: {
                page: 1
            }},
            totalPages: 1
        }
    },
    methods: {
        statusLabel(status) {
          const key = 'sellerOrders.statuses.' + status
          return this.$te(key) ? this.$t(key) : status
        },
        updateOrderPane(order){
          this.showOrderPane = !this.showOrderPane
          this.orderTemp = {...order}
        },
        setPageParam(navPage){
            this.params.params.page = navPage
            this.fetchOrders()
            },
        async save() {
                try {
                const response = await api.patch(`http://127.0.0.1:8000/core/orders/${this.orderTemp.id}/`, 
                {'location': this.orderTemp.location, 'total_value': this.orderTemp.price});
                this.showOrderPane = false
                this.$emit('saved', true)

        } catch (error) {
            console.error(error.response);
        }
            },
        async fetchOrders () {
            try{
                const response = await api.get('http://127.0.0.1:8000/core/orders/', this.params)
            
            this.orders = {
                ...this.orders,
                ...response.data['results']
            }
            this.totalPages = response.data['total_pages']
          }
            catch(error){
                console.log(error.response)
            }
        },
    }
}
</script>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
h1 { font-size: 1.5rem; font-weight: 600; color: var(--color-text); }
.card { width: fit-content; max-width: 100%; overflow: hidden; }

.table-card {
  width: 100%;
  overflow-x: auto;
}
.order-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  color: var(--color-text);
}
.order-table th {
  background: var(--color-bg);
  padding: 0.75rem 1rem;
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}
.order-table td {
  padding: 0.875rem 1rem;
  border-top: 1px solid var(--color-border);
  font-size: 0.9rem;
}
.order-table tbody tr:first-child td { border-top: none; }
.order-table tbody tr:hover { background: var(--color-bg); }
.bold { font-weight: 600; }
.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  min-height: 40px;
  border-radius: var(--radius-sm);
  color: var(--color-primary);
  cursor: pointer;
  transition: background var(--transition);
}
.icon-btn:hover { background: var(--color-primary-soft); }
.status-pill {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: capitalize;
}
.completed { background: var(--color-success-soft); color: var(--color-text); }
.pending { background: var(--color-bg); color: var(--color-text-muted); border: 1px solid var(--color-border); }
.cancelled { background: var(--color-error-soft); color: var(--color-text); }

.container {
  position: fixed;
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
