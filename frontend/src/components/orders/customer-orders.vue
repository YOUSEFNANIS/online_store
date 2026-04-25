<template>
  <div>
    <load-component v-if="loading===true"/>
  <div v-else>
    <!-- <div class="header">
      <h1>Orders</h1>
      <button class="btn-black" @click="createNewOrder">Create order</button>
    </div> -->

    <div class="card">
      <table class="order-table">
        <thead>
          <tr>
            <th>Store</th>
            <th>Value</th>
            <th>Date</th>
            <th>Items</th>
            <th>Location</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td class="bold">{{ order.store_name }}</td>
            <td>{{ order.total_value }} LYD</td>
            <td>{{ order.creation_date }}</td>
            <td>{{ order.total_quantity }}</td>
            <td>{{ order.location }}</td>
            <td>
              <span :class="['status-pill', order.order_status]">
                {{ order.order_status }}
              </span>
            </td>
            <td class="actions">
              <span @click.stop="updateOrderPane(order)" title="Edit order status">
                <Pencil title="edit"/>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
      <transition name="pop">
      <div v-if="showOrderPane" class="order-card" ref="orderPane">
        <div class="card-header">
          <span class="order-id">#order: {{ orderTemp.id }}</span>
          
          <div class="select-wrapper">
            <select v-model="orderTemp.order_status" :class="['status-pill', orderTemp.order_status]">
              <option class="pending" value="pending">Pending</option>
              <option class="cancelled" value="cancelled">cancelled</option>
              <option class="completed" value="completed">completed</option>
            </select>
          </div>
        </div>

        <hr class="divider" />

        <div class="card-actions">
          <button @click="updateOrderStatus" class="btn btn-save">save</button>
          <button @click="showOrderPane = false" class="btn btn-cancel">cancel</button>
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 { font-size: 24px; font-weight: 600; }

/* Table Design */
.card {
  width: fit-content;
  background: white;
  border: 1px solid #ebebeb;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  overflow: hidden;
}

.order-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.order-table th {
  background: #f7f7f7;
  padding: 12px 16px;
  font-size: 15px;
  font-weight: bold;
  text-transform: uppercase;
  color: #616161;
}

.order-table td {
  padding: 16px;
  border-top: 1px solid #ebebeb;
  font-size: 14px;
}

.bold { font-weight: 500; }

/* Buttons */
.btn-black {
  background: #1a1a1a;
  color: white;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
  font-weight: 500;
}

.actions button {
  background: none;
  border: none;
  color: #005bd3;
  cursor: pointer;
  text-decoration: underline;
}

/* Status Pills */
.status-pill {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: 500;

  text-transform: capitalize;
}


/* The Card Structure */
.order-card {
  background-color: #ffffff; /* Light gray background */
  position: fixed;
  top: 30%;
  left: 30%;
  padding: 24px;
  width: 30%;
  box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.order-id {
  font-size: 1.5rem;
  font-weight: 500;
}

/* Pill Select Styling */
select {
  padding: 8px 16px;
  border: 1px solid #ccc;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
}

.divider {
  border: none;
  border-top: 1px solid #333;
  margin: 15px 0;
}

/* Button Layout */
.card-actions {
  display: flex;
  gap: 15px;
}

.btn {
  flex: 1;
  padding: 12px;
  border: none;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  color: white;
  background-color: black;
  transition: transform 0.1s;
}

.btn:active {
  transform: scale(0.96);
}

/* --- ANIMATION --- */
.pop-enter-active, .pop-leave-active {
  transition: all 0.3s ease-out;
}

.pop-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.pop-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
.completed { background: #e3f1df; color: #008060; } /* Subtle Green */
.pending { background: #fff4d4; color: #8a6116; }   /* Subtle Yellow */
.cancelled { background: #f9e1e1; color: #a92d2d; } /* Subtle Red */

</style>