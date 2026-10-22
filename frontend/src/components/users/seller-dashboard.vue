<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>{{ $t('sellerDashboard.title') }}</h1>
      <p>{{ rangeLabel }}</p>
    </header>

    <section class="stats" :aria-label="$t('sellerDashboard.summaryAria')">
      <div class="stat">
        <span class="stat-label">{{ rangeShort }}</span>
        <span class="stat-value">{{ loaded ? fmt(total) : '—' }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">{{ $t('sellerDashboard.today') }}</span>
        <span class="stat-value">{{ loaded ? fmt(today) : '—' }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">{{ $t('sellerDashboard.dailyAverage') }}</span>
        <span class="stat-value">{{ loaded ? fmt(average, 1) : '—' }}</span>
      </div>
    </section>

    <section class="card">
      <div class="card-header">
        <h2>{{ $t('sellerDashboard.ordersPerDay') }}</h2>
      </div>

      <div class="chart-container">
        <p v-if="!loaded && !failed" class="chart-state" role="status">{{ $t('sellerDashboard.loadingOrders') }}</p>
        <p v-else-if="failed" class="chart-state chart-state-error" role="alert">
          {{ $t('sellerDashboard.loadFailed') }}
        </p>
        <template v-else>
          <Line :data="chartData" :options="chartOptions" />
          <p v-if="total === 0" class="chart-state chart-empty">
            {{ $t(windowDays < 7 ? 'sellerDashboard.noOrdersSinceJoin' : 'sellerDashboard.noOrdersWeek') }}
          </p>
        </template>
      </div>
    </section>

    <section class="insights">
      <div class="stat">
        <span class="stat-label">{{ $t('sellerTools.revenue7') }}</span>
        <span class="stat-value">{{ stats ? fmt(stats.revenue_7, 2) : '—' }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">{{ $t('sellerTools.revenue30') }}</span>
        <span class="stat-value">{{ stats ? fmt(stats.revenue_30, 2) : '—' }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">{{ $t('sellerTools.toProcess') }}</span>
        <span class="stat-value">{{ stats ? fmt((stats.orders_by_status.pending || 0) + (stats.orders_by_status.confirmed || 0)) : '—' }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">{{ $t('sellerTools.toDeliver') }}</span>
        <span class="stat-value">{{ stats ? fmt(stats.orders_by_status.shipped || 0) : '—' }}</span>
      </div>
    </section>

    <div v-if="stats" class="two-col">
      <section class="card">
        <div class="card-header"><h2>{{ $t('sellerTools.topProducts') }}</h2></div>
        <p v-if="!stats.top_products.length" class="list-empty">{{ $t('sellerTools.noSalesYet') }}</p>
        <ol v-else class="rank">
          <li v-for="t in stats.top_products" :key="t.id">
            <router-link :to="'/products/' + t.id">{{ t.name }}</router-link>
            <span>{{ $t('sellerTools.units', { count: fmt(t.units) }) }}</span>
          </li>
        </ol>
      </section>
      <section class="card">
        <div class="card-header">
          <h2>{{ $t('sellerTools.lowStock') }}</h2>
          <router-link to="/inventory" class="card-link">{{ $t('sellerTools.manage') }}</router-link>
        </div>
        <p v-if="!stats.low_stock.length" class="list-empty">{{ $t('sellerTools.stockOk') }}</p>
        <ul v-else class="rank">
          <li v-for="p in stats.low_stock" :key="p.id">
            <router-link :to="'/products/' + p.id">{{ p.name }}</router-link>
            <span :class="{ out: p.inventory === 0 }">{{ p.inventory === 0 ? $t('sellerTools.out') : $t('sellerTools.left', { count: p.inventory }) }}</span>
          </li>
        </ul>
      </section>
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
    this.loadStats()

    try {
      await this.loadWindow()
      const labels = await this.fetchOrders()
      const entries = Object.entries(labels)
      entries.sort((a, b) => new Date(a[0]) - new Date(b[0]))
      const sortedData = Object.fromEntries(entries)
      this.labels = Object.keys(sortedData)
      this.orders = Object.values(sortedData)
      this.loaded = true
    } catch (error) {
      this.failed = true
    }
  },
  data() {
    return {
      orders: null,
      labels:  null,
      windowDays: 7,
      loaded: false,
      failed: false,
      stats: null
    }
  },

  computed: {
    total() {
      return (this.orders || []).reduce((sum, n) => sum + n, 0)
    },
    today() {
      return this.orders?.length ? this.orders[this.orders.length - 1] : 0
    },
    average() {
      return (this.total / this.windowDays).toFixed(1)
    },
    rangeLabel() {
      return this.$t(this.windowDays < 7 ? 'sellerDashboard.rangeSinceJoin' : 'sellerDashboard.rangeWeek')
    },
    rangeShort() {
      return this.$t(this.windowDays < 7 ? 'sellerDashboard.shortSinceJoin' : 'sellerDashboard.shortWeek')
    },

    chartData() {
      return {
        labels: (this.labels || []).map(this.formatLabel),
        datasets: [
          {
            label: this.$t('sellerDashboard.orders'),
            data: this.orders,

            borderColor: '#1A56DB',
            backgroundColor: 'rgba(26, 86, 219, 0.1)',

            tension: 0.4,
            fill: true,

            pointRadius: 0,
            pointHoverRadius: 5,
            pointBackgroundColor: '#1A56DB',

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
              label: (context) => this.$t('sellerDashboard.tooltipOrders', { count: this.fmt(context.raw) })
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
              precision: 0
            }
          }
        }
      }
    }
  },

  methods: {
    async loadStats() {
      try {
        this.stats = (await api.get('/core/seller/stats/')).data
      } catch (error) {
        this.stats = null
      }
    },
    fmt(n, digits = 0) {
      return new Intl.NumberFormat(this.$i18n.locale, { maximumFractionDigits: digits, minimumFractionDigits: digits }).format(Number(n))
    },
    formatLabel(key) {
      const [y, m, d] = String(key).split(' ')
      const idx = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].indexOf(m)
      if (idx < 0) return key
      return new Date(Number(y), idx, Number(d)).toLocaleDateString(this.$i18n.locale, { month: 'short', day: 'numeric' })
    },

    // Days shown = min(7, calendar days since the account was created, inclusive of today).
    // Accounts 7 days old or newer only show days that exist; older accounts show the last 7.
    async loadWindow() {
      const response = await api.get('/signup/get_id/me/')
      const joined = response.data.date_joined ? new Date(response.data.date_joined) : null
      if (!joined || Number.isNaN(joined.getTime())) return
      const startOfDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate())
      const ageDays = Math.round((startOfDay(new Date()) - startOfDay(joined)) / 86400000)
      this.windowDays = Math.min(7, Math.max(1, ageDays + 1))
    },

    async fetchOrders() {
      const url = '/core/orders/'
      const date = new Date()
      date.setDate(date.getDate() - (this.windowDays - 1))
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

    for (let i = this.windowDays - 1; i >= 0; i--) {
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
.dashboard {
  display: block;
  width: min(1100px, 92%);
  height: auto;
  margin: 130px auto 2rem;
}
.dashboard-header { margin-bottom: 1.25rem; }
.dashboard-header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
}
.dashboard-header p {
  margin: 0.25rem 0 0;
  color: var(--color-text-muted);
  font-size: 0.95rem;
}
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}
.stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1rem 1.25rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.stat-label {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}
.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
}
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: 1.25rem;
}
.card-header { margin-bottom: 0.75rem; }
.card-header h2 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
}
.chart-container {
  position: relative;
  width: 100%;
  height: 320px;
}
.chart-state {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  color: var(--color-text-muted);
  text-align: center;
  pointer-events: none;
}
.chart-state-error { color: var(--color-error); }
.insights { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin: 1rem 0; }
.two-col { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 1rem; }
.card-header { display: flex; align-items: baseline; justify-content: space-between; }
.card-link { font-size: 0.85rem; }
.list-empty { margin: 0; color: var(--color-text-muted); }
.rank { list-style: none; margin: 0; padding: 0; }
.rank li { display: flex; justify-content: space-between; gap: 12px; padding: 8px 0; border-top: 1px solid var(--color-border); }
.rank li:first-child { border-top: none; }
.rank span { color: var(--color-text-muted); font-variant-numeric: tabular-nums; white-space: nowrap; }
.rank .out { color: var(--color-error); }
.chart-empty { align-items: center; padding-bottom: 2rem; }
</style>
