<template>
  <div>
    <div class="card">
      <table class="order-table">
        <thead>
          <tr>
            <th>Customer</th>
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
            <td class="bold">{{ order.customer_name }}</td>
            <td>{{ order.total_value }} LYD</td>
            <td>{{ order.creation_date }}</td>
            <td>{{ order.total_quantity }}</td>
            <td>{{ order.location }}</td>
            <td>
              <span :class="['status-pill', order.order_status]">
                {{ order.order_status }}
              </span>
            </td>
            <td>
              <span @click="updateOrderPane(order)" title="Edit this item">
                <Pencil title="edit"/>
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
            placeholder="location"
        >

        <div class="price-row">
        <input 
            type="text" 
            placeholder="total price"
            v-model="orderTemp.price" 
            class="price-input"
        >
        
        <span>LYD</span>
    </div>
    </div>

    

    <div class="actions">
        <button @click="save" class="btn">save</button>
        <button @click="handleCancel" class="btn">cancel</button>
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
  text-align: center;
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

/* Status Pills */
.status-pill {
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}
.container {
          position: fixed;
          top: 30%;
          left: 30%;
          background: white;
          border: 1px solid #ebebeb;
          box-shadow: 0 1px 3px rgba(0,0,0,0.05);
          padding: 2.5rem;
          max-width: 700px
        }
.order-id-header {
    width: 100%;
    display: flex;
    background-color: #fcfcfc;
    justify-content: space-between;
    border-bottom: 2px solid #000000; /* That specific blue line from your image */
    margin-bottom: 2rem;
}

.order-id-header h2 {
    margin: 0;
    padding: 0px 0px 20px 0px;
    font-size: 1.2rem;
    font-weight: 500;
    color: #111;
    /* This makes it look like the "typewriter" or clean font in your pic */
}
.form-row {
    display: flex;
    width: 100%; /* Changed from fit-content */
    align-items: flex-end;
    justify-content: space-between; 
    border: 20px 0px;
    gap: 2rem;
    margin-bottom: 2.5rem;
}

.laction-field {
    flex: 2;
}

.price-row {
    display: flex;
    width: fit-content;
    align-items: flex-end;
    gap: 1rem;
    flex: 1; /* Takes up less space */
}

.actions {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 1rem;
    margin-top: 1rem;
}

input {
    flex: 1;
    border: none;
    border-bottom: 1.5px solid #999;
    background: transparent;
    font-size: 1.2rem;
    outline: none;
    transition: border-color 0.2s;
}

input:focus {
    border-bottom-color: #3b82f6;
}
.completed { background: #e3f1df; color: #008060; } /* Subtle Green */
.pending { background: #fff4d4; color: #8a6116; }   /* Subtle Yellow */
.cancelled { background: #f9e1e1; color: #a92d2d; } /* Subtle Red */

</style>