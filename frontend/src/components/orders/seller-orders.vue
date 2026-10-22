<template>
  <div>
    <div class="export-bar">
      <button type="button" class="btn btn-outline" :disabled="exporting" @click="exportCsv">{{ $t('sellerTools.exportOrders') }}</button>
    </div>
    <div class="orders-card">
      <div v-if="!orderList.length" class="orders-empty">
        <div class="orders-empty-icon" aria-hidden="true">📦</div>
        {{ $t('sellerOrders.empty') }}
      </div>
      <table v-else class="orders-table">
        <thead>
          <tr>
            <th>{{ $t('sellerOrders.customer') }}</th>
            <th>{{ $t('sellerOrders.value') }}</th>
            <th>{{ $t('sellerOrders.date') }}</th>
            <th>{{ $t('sellerOrders.items') }}</th>
            <th>{{ $t('sellerOrders.location') }}</th>
            <th>{{ $t('sellerOrders.status') }}</th>
            <th><span class="sr-only">{{ $t('sellerOrders.edit') }}</span></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orderList" :key="order.id">
            <td class="col-name" :data-label="$t('sellerOrders.customer')">{{ order.customer_name }}</td>
            <td class="col-value" :data-label="$t('sellerOrders.value')">{{ order.total_value }} {{ $t('sellerOrders.currency') }}</td>
            <td class="col-muted" :data-label="$t('sellerOrders.date')">{{ order.creation_date }}</td>
            <td :data-label="$t('sellerOrders.items')">{{ order.total_quantity }}</td>
            <td :data-label="$t('sellerOrders.location')">{{ order.location }}</td>
            <td :data-label="$t('sellerOrders.status')">
              <span :class="['status-badge', order.order_status]">{{ statusLabel(order.order_status) }}</span>
            </td>
            <td class="col-action">
              <button type="button" class="orders-icon-btn" @click="updateOrderPane(order)" :title="$t('sellerOrders.editItem')" :aria-label="$t('sellerOrders.editItem')">
                <Pencil :size="18" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <transition name="orders-fade">
      <div v-if="showOrderPane" class="orders-backdrop" @click.self="handleCancel">
        <div class="orders-modal" role="dialog" aria-modal="true">
          <h2>{{ orderTemp.customer_name }}</h2>

          <order-timeline :history="orderTemp.status_history" />
          <p class="pay-line">{{ $t('orderFlow.payment.' + orderTemp.payment_method) }} · {{ $t('orderFlow.payment.' + orderTemp.payment_status) }}</p>
          <div v-if="orderTemp.allowed_transitions?.length" class="orders-modal-actions status-actions">
            <button
              v-for="s in orderTemp.allowed_transitions"
              :key="s"
              type="button"
              :class="['btn', s === 'cancelled' ? 'btn-outline' : 'btn-primary']"
              :disabled="busy"
              @click="changeStatus(s)"
            >{{ $t('orderFlow.actions.' + s) }}</button>
          </div>

          <label class="field-label" for="order-location">{{ $t('sellerOrders.location') }}</label>
          <input id="order-location" type="text" v-model="orderTemp.location" class="field-input">

          <label class="field-label" for="order-price">{{ $t('sellerOrders.totalPrice') }} ({{ $t('sellerOrders.currency') }})</label>
          <input id="order-price" type="text" inputmode="decimal" v-model="orderTemp.price" class="field-input">

          <div class="orders-modal-actions">
            <button @click="save" class="btn btn-primary">{{ $t('sellerOrders.save') }}</button>
            <button @click="handleCancel" class="btn btn-outline">{{ $t('sellerOrders.cancel') }}</button>
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
</template>

<script>
import api from '@/services/api';
import { Pencil } from '@lucide/vue';
import OrderTimeline from './order-timeline.vue';
import { downloadFile } from '@/services/download';

export default {
  components: { Pencil, OrderTimeline },
    mounted(){
        this.fetchOrders()
        this.$emit('loaded')
    },
    data(){
        return {
            orders: [],
            orderTemp: {},
            showOrderPane: false,
            busy: false,
            exporting: false,
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
        async updateOrderPane(order){
          // The list holds summary rows only; history, payment and transitions come from the detail call.
          try {
            const response = await api.get(`/core/orders/${order.id}/`)
            this.orderTemp = { ...response.data, price: response.data.total_value }
            this.showOrderPane = true
          } catch (error) {
            console.error(error.response)
          }
        },
        handleCancel(){
          this.showOrderPane = false
        },
        setPageParam(navPage){
            this.params.params.page = navPage
            this.fetchOrders()
        },
        async exportCsv() {
          this.exporting = true
          try { await downloadFile('/core/seller/export/orders/', 'orders.csv') } catch (error) { console.error(error) }
          this.exporting = false
        },
        async changeStatus(next) {
          if (next === 'cancelled' && !window.confirm(this.$t('orderFlow.confirmCancel'))) return
          this.busy = true
          try {
            const response = await api.patch(`/core/orders/${this.orderTemp.id}/`, { order_status: next })
            const i = this.orders.findIndex(o => o.id === response.data.id)
            if (i >= 0) this.orders[i] = { ...this.orders[i], order_status: response.data.order_status }
            this.orderTemp = { ...response.data, price: response.data.total_value }
            this.$emit('saved', true)
          } catch (error) {
            console.error(error.response)
          } finally {
            this.busy = false
          }
        },
        async save() {
            try {
                await api.patch(`/core/orders/${this.orderTemp.id}/`,
                {'location': this.orderTemp.location, 'total_value': this.orderTemp.price});
                this.showOrderPane = false
                this.$emit('saved', true)
                this.fetchOrders()
            } catch (error) {
                console.error(error.response);
            }
        },
        async fetchOrders () {
            try{
                const response = await api.get('/core/orders/', this.params)
                this.orders = response.data['results']
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
.field-label { display: block; margin-bottom: 6px; font-size: 0.85rem; font-weight: 600; color: var(--color-text-muted); }
.field-input { display: block; width: 100%; min-height: 44px; margin-bottom: 16px; box-sizing: border-box; }
.export-bar { display: flex; justify-content: flex-end; margin-bottom: 12px; }
.status-actions { margin-bottom: 16px; flex-wrap: wrap; }
.sr-only {
  position: absolute; width: 1px; height: 1px; overflow: hidden;
  clip: rect(0 0 0 0); white-space: nowrap;
}
</style>
