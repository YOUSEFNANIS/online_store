<!-- OrdersChart.vue -->
<template>
  <div class="card">
    <div class="card-header">
      <h3>Orders (Last 7 Days)</h3>
    </div>

    <div class="chart-container">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'
import api from '@/services/api';
import { useRoleStore } from '@/stores/role';

Chart.register(...registerables)

export default {
  name: 'OrdersChart',
  components: { Line },
  
  async mounted(){

    const labels = await this.fetchOrders()
    const entries = Object.entries(labels)
    entries.sort((a, b) => new Date(a[0]) - new Date(b[0]))
    const sortedData = Object.fromEntries(entries)
    this.labels = Object.keys(sortedData)
    this.orders = Object.values(sortedData)
  },
  data() {
    return {
      orders: null,
      labels:  null
    }
  },

  computed: {
    
    chartData() {
      return {
        labels: this.labels,
        datasets: [
          {
            label: 'Orders',
            data: this.orders,

            borderColor: '#5C6AC4',
            backgroundColor: 'rgba(92, 106, 196, 0.1)',

            tension: 0.4,
            fill: true,

            pointRadius: 0,
            pointHoverRadius: 5,
            pointBackgroundColor: '#5C6AC4',

            borderWidth: 2
          }
        ]
      }
    },

    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: '#111827',
            titleColor: '#fff',
            bodyColor: '#fff',
            padding: 10,
            displayColors: false,
            callbacks: {
              label: (context) => `Orders: ${context.raw}`
            }
          }
        },

        scales: {
          x: {
            grid: {
              display: false
            },
            ticks: {
              color: '#6B7280'
            }
          },
          y: {
            beginAtZero: true,
            grid: {
              color: '#E5E7EB'
            },
            ticks: {
              color: '#6B7280',
              stepSize: 5
            }
          }
        }
      }
    }
  },

  methods: {

    async fetchOrders() {
      const url = 'http://127.0.0.1:8000/core/orders/'
      const date = new Date()
      date.setDate(date.getDate() - 7)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')

      const queryDate = `${year}-${month}-${day}`
      
      const response = await api.get(url, {params: {
        start_date: queryDate
      }})
      const data = response.data
      
      const orders = Object.groupBy(data, (item) => {
                return item.creation_date.split(',')[0]
              })
      for (const date in orders){
        orders[date] = orders[date].length
      }
      const days = this.getLast7Days()
      for (const i of days){
        if (orders[i] === undefined){
          orders[i] = 0
        }
      }
      return orders 
    },

    getLast7Days() {
    const days = []

    for (let i = 6; i >= 0; i--) {
      const date = new Date()
    date.setDate(date.getDate() - i)

    const year = date.getFullYear()
    const month = date.toLocaleString('en-US', { month: 'short' })
    const day = date.getDate()

    days.push(`${year} ${month} ${day}`)
    }

    return days
  },
  }
}
</script>

<style scoped>
.card {
  background: #ffffff;
  widows: 100%;
  height: 100%;
  position: relative;
  margin: 10% 5% 0 5%;
  display: block;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.card-header {
  margin-bottom: 10px;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.chart-container {
  position: relative;
  width: 90%;
  height: 300px;
  max-height: 100%;
  margin: 5% 5% 0 5%;
}
</style>