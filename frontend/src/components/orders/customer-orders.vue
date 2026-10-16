<template>
  <div>
    <load-component v-if="loading===true"/>
  <div v-else>
    <!-- <div class="header">
      <h1>Orders</h1>
      <button class="btn-black" @click="createNewOrder">Create order</button>
    </div> -->

    <div class="card table-card">
      <table class="order-table">
        <thead>
          <tr>
            <th>{{ $t('customerOrders.store') }}</th>
            <th>{{ $t('customerOrders.value') }}</th>
            <th>{{ $t('customerOrders.date') }}</th>
            <th>{{ $t('customerOrders.items') }}</th>
            <th>{{ $t('customerOrders.location') }}</th>
            <th>{{ $t('customerOrders.status') }}</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td class="bold">{{ order.store_name }}</td>
            <td>{{ order.total_value }} {{ $t('customerOrders.currency') }}</td>
            <td>{{ order.creation_date }}</td>
            <td>{{ order.total_quantity }}</td>
            <td>{{ order.location }}</td>
            <td>
              <span :class="['status-pill', order.order_status]">
                {{ statusLabel(order.order_status) }}
              </span>
            </td>
            <td class="actions">
              <span class="icon-btn" role="button" tabindex="0" @click.stop="updateOrderPane(order)" @keydown.enter="updateOrderPane(order)" :title="$t('customerOrders.editStatus')" :aria-label="$t('customerOrders.editStatus')">
                <Pencil :title="$t('customerOrders.edit')"/>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
      <transition name="pop">
      <div v-if="showOrderPane" class="order-card" ref="orderPane">
        <div class="card-header">
          <span class="order-id">{{ $t('customerOrders.orderNumber', { id: orderTemp.id }) }}</span>
          
          <div class="select-wrapper">
            <select v-model="orderTemp.order_status" :class="['status-pill', orderTemp.order_status]">
              <option class="pending" value="pending">{{ $t('customerOrders.statuses.pending') }}</option>
              <option class="cancelled" value="cancelled">{{ $t('customerOrders.statuses.cancelled') }}</option>
              <option class="completed" value="completed">{{ $t('customerOrders.statuses.completed') }}</option>
            </select>
          </div>
        </div>

        <hr class="divider" />

        <div class="card-actions">
          <button @click="updateOrderStatus" class="btn btn-primary">{{ $t('customerOrders.save') }}</button>
          <button @click="showOrderPane = false" class="btn btn-outline">{{ $t('customerOrders.cancel') }}</button>
        </div>
      </div>
    </transition>
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
import { Pencil } from '@lucide/vue';
import LoadComponent from '../helperComponents/load-component.vue';

export default {
  components: {Pencil, LoadComponent },
  beforeUnmount() {
    document.removeEventListener('click', this.handleOrderPaneOutsideClick);
  },
    mounted(){
        
        document.addEventListener('click', this.handleOrderPaneOutsideClick);
        this.fetchOrders()
    },

    data(){
        return {
            orders: {},
            showOrderPane: false,
            loading: false,
            orderTemp: {},
            params: {
                params: {
                page: 1
            }},
            totalPages: 1
        }
    },
    methods: {
        statusLabel(status) {
          const key = 'customerOrders.statuses.' + status
          return this.$te(key) ? this.$t(key) : status
        },
        handleOrderPaneOutsideClick(event) {
          if (this.showOrderPane && this.$refs.orderPane && !this.$refs.orderPane.contains(event.target)) {
              this.showOrderPane = false;
          }},
          setPageParam(navPage){
            this.params.params.page = navPage
            this.fetchOrders()
            },
        updateOrderPane(order){
          this.showOrderPane=!this.showOrderPane
          this.orderTemp = {...order}
        },

        async updateOrderStatus (){
          try{const url = 'http://127.0.0.1:8000/core/orders/' + this.orderTemp.id + '/'
          const response = await api.patch(url, {'order_status': this.orderTemp.order_status})
          this.showOrderPane = false}
          catch(error){
            console.log(error.response)
          }
        },

        async fetchOrders () {
            this.loading = true
            try{
                const response = await api.get('http://127.0.0.1:8000/core/orders/', this.params)
            this.orders = {
                ...this.orders,
                ...response.data['results']
            }
            this.totalPages = response.data['total_pages']
          
        this.loading = false
      }
            catch(error){
                console.log(error)
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
  text-align: start;
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

.order-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  position: fixed;
  top: 30%;
  inset-inline-start: 50%;
  transform: translateX(-50%);
  padding: 1.5rem;
  width: min(420px, calc(100vw - 2rem));
  z-index: 50;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.order-id {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text);
}
select {
  min-height: 40px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
}
select.status-pill { border-radius: var(--radius-sm); }
.divider {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: 1rem 0;
}
.card-actions { display: flex; gap: 0.75rem; }
.card-actions .btn { flex: 1; }
.pop-enter-active, .pop-leave-active { transition: opacity 0.2s ease; }
.pop-enter-from, .pop-leave-to { opacity: 0; }
</style>
