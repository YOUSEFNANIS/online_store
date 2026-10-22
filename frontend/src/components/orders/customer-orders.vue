<template>
  <div>
    <load-component v-if="loading===true"/>
    <div v-else>
      <div class="orders-card">
        <div v-if="!orderList.length" class="orders-empty">
          <div class="orders-empty-icon" aria-hidden="true">📦</div>
          {{ $t('customerOrders.empty') }}
        </div>
        <table v-else class="orders-table">
          <thead>
            <tr>
              <th>{{ $t('customerOrders.store') }}</th>
              <th>{{ $t('customerOrders.value') }}</th>
              <th>{{ $t('customerOrders.date') }}</th>
              <th>{{ $t('customerOrders.items') }}</th>
              <th>{{ $t('customerOrders.location') }}</th>
              <th>{{ $t('customerOrders.status') }}</th>
              <th><span class="sr-only">{{ $t('customerOrders.edit') }}</span></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orderList" :key="order.id">
              <td class="col-name" :data-label="$t('customerOrders.store')">{{ order.store_name }}</td>
              <td class="col-value" :data-label="$t('customerOrders.value')">{{ order.total_value }} {{ $t('customerOrders.currency') }}</td>
              <td class="col-muted" :data-label="$t('customerOrders.date')">{{ order.creation_date }}</td>
              <td :data-label="$t('customerOrders.items')">{{ order.total_quantity }}</td>
              <td :data-label="$t('customerOrders.location')">{{ order.location }}</td>
              <td :data-label="$t('customerOrders.status')">
                <span :class="['status-badge', order.order_status]">{{ statusLabel(order.order_status) }}</span>
              </td>
              <td class="col-action">
                <button
                  v-if="order.order_status === 'shipped'"
                  type="button"
                  class="btn btn-primary deliver-btn"
                  :disabled="busy"
                  @click.stop="confirmDelivery(order)"
                >{{ $t('orderFlow.actions.delivered') }}</button>
                <button type="button" class="orders-icon-btn" @click.stop="updateOrderPane(order)" :title="$t('orderFlow.details')" :aria-label="$t('orderFlow.details')">
                  <Eye :size="18" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <transition name="orders-fade">
        <div v-if="showOrderPane" class="orders-backdrop" @click.self="showOrderPane = false">
          <div class="orders-modal" role="dialog" aria-modal="true">
            <h2>{{ $t('customerOrders.orderNumber', { id: orderTemp.id }) }}</h2>
            <order-timeline :history="orderTemp.status_history" />
            <p class="pay-line">{{ $t('orderFlow.payment.' + orderTemp.payment_method) }} · {{ $t('orderFlow.payment.' + orderTemp.payment_status) }}</p>
            <div class="orders-modal-actions">
              <button
                v-for="s in orderTemp.allowed_transitions"
                :key="s"
                type="button"
                :class="['btn', s === 'cancelled' ? 'btn-outline' : 'btn-primary']"
                :disabled="busy"
                @click="changeStatus(s)"
              >{{ $t('orderFlow.actions.' + s) }}</button>
              <button type="button" class="btn btn-outline" @click="showOrderPane = false">{{ $t('orderFlow.close') }}</button>
            </div>
          </div>
        </div>
      </transition>

      <div v-if="totalPages > 1" class="orders-pagination">
        <button
          v-for="i in totalPages"
          :key="i"
          :class="{ active: i === params.params.page }"
          @click="setPageParam(i)"
        >{{ i }}</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import { Eye } from '@lucide/vue';
import OrderTimeline from './order-timeline.vue';
import LoadComponent from '../helperComponents/load-component.vue';

export default {
  components: { Eye, LoadComponent, OrderTimeline },
    mounted(){
        this.fetchOrders()
    },

    data(){
        return {
            orders: [],
            showOrderPane: false,
            loading: false,
            busy: false,
            orderTemp: {},
            params: {
                params: {
                page: 1
            }},
            totalPages: 1
        }
    },
    computed: {
        orderList() {
          return Object.values(this.orders)
        }
    },
    methods: {
        statusLabel(status) {
          const key = 'orderFlow.statuses.' + status
          return this.$te(key) ? this.$t(key) : status
        },
        setPageParam(navPage){
            this.params.params.page = navPage
            this.fetchOrders()
        },
        async updateOrderPane(order){
          // The list holds summary rows only; history, payment and transitions come from the detail call.
          try {
            const response = await api.get('/core/orders/' + order.id + '/')
            this.orderTemp = response.data
            this.showOrderPane = true
          } catch (error) {
            console.log(error.response)
          }
        },

        async changeStatus(next) {
          const updated = await this.patchStatus(this.orderTemp.id, next)
          if (updated) this.orderTemp = updated
        },

        // Shipped orders get a button in the list row, so the customer does not have to open the details first.
        async confirmDelivery(order) {
          await this.patchStatus(order.id, 'delivered')
        },

        async patchStatus(orderId, next) {
          const prompt = { cancelled: 'orderFlow.confirmCancel', delivered: 'orderFlow.confirmDelivery' }[next]
          if (prompt && !window.confirm(this.$t(prompt))) return null
          this.busy = true
          try {
            const response = await api.patch('/core/orders/' + orderId + '/', { order_status: next })
            const i = this.orders.findIndex(o => o.id === response.data.id)
            if (i >= 0) this.orders[i] = { ...this.orders[i], order_status: response.data.order_status }
            return response.data
          } catch (error) {
            console.log(error.response)
            return null
          } finally {
            this.busy = false
          }
        },

        async fetchOrders () {
            this.loading = true
            try{
                const response = await api.get('/core/orders/', this.params)
                this.orders = response.data['results']
                this.totalPages = response.data['total_pages']
            }
            catch(error){
                console.log(error)
            }
            finally {
                this.loading = false
            }
        },
    }
}
</script>

<style scoped>
.field-label { display: block; margin-bottom: 6px; font-size: 0.85rem; font-weight: 600; color: var(--color-text-muted); }
.deliver-btn { margin-inline-end: 8px; white-space: nowrap; }
.status-select { width: 100%; min-height: 44px; padding: 0 12px; cursor: pointer; }
.sr-only {
  position: absolute; width: 1px; height: 1px; overflow: hidden;
  clip: rect(0 0 0 0); white-space: nowrap;
}
</style>
