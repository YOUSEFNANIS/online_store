<template>
  <!-- root receives .page-content (flex row) from App.vue, so keep a block-level child -->
  <div class="orders-root">
    <div class="orders-page">
      <header class="orders-header">
        <h1>{{ $t('ordersPage.title') }}</h1>
        <p>{{ $t(user_type === 'seller' ? 'ordersPage.subtitleSeller' : 'ordersPage.subtitleCustomer') }}</p>
      </header>
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
.orders-root { margin-inline: auto; }
.orders-page {
  width: 100%;
  max-width: 1100px;
  /* sits under .page-content's navbar offset; this clears the 50px side menu plus a gap */
  margin: max(24px, calc(134px - 5vw)) auto 64px;
  padding: 0 16px;
  color: var(--color-text);
}
.orders-header { margin-bottom: 20px; text-align: start; }
.orders-header h1 { margin: 0 0 4px; font-size: 1.75rem; font-weight: 700; }
.orders-header p { margin: 0; color: var(--color-text-muted); font-size: 0.95rem; }
</style>

<!-- shared by customer-orders.vue and seller-orders.vue -->
<style>
.orders-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}
.orders-table { width: 100%; border-collapse: collapse; text-align: start; }
.orders-table th {
  padding: 14px 20px;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
  font-size: 0.75rem; font-weight: 600;
  letter-spacing: 0.04em; text-transform: uppercase;
  color: var(--color-text-muted);
  text-align: start; white-space: nowrap;
}
.orders-table td {
  padding: 16px 20px;
  border-top: 1px solid var(--color-border);
  font-size: 0.92rem;
  text-align: start; vertical-align: middle;
}
.orders-table tbody tr:first-child td { border-top: none; }
.orders-table tbody tr { transition: background var(--transition); }
.orders-table tbody tr:hover { background: var(--color-bg); }
.orders-table .col-name { font-weight: 600; }
.orders-table .col-value { font-weight: 600; font-variant-numeric: tabular-nums; white-space: nowrap; }
.orders-table .col-muted { color: var(--color-text-muted); white-space: nowrap; }
.orders-table .col-action { width: 1%; text-align: end; }

.status-badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 12px; border-radius: 999px;
  font-size: 0.8125rem; font-weight: 600; white-space: nowrap;
}
.status-badge::before {
  content: ''; width: 7px; height: 7px; border-radius: 50%; background: currentColor;
}
.status-badge.pending { background: #FEF3C7; color: #92400E; }
.pay-line { margin: 0 0 16px; font-size: 0.9rem; color: var(--color-text-muted); }
.status-badge.confirmed { background: #DBEAFE; color: #1E40AF; }
.status-badge.shipped { background: #E0E7FF; color: #3730A3; }
.status-badge.delivered,
.status-badge.completed { background: var(--color-success-soft); color: #166534; }
.status-badge.cancelled { background: var(--color-error-soft); color: #991B1B; }

.orders-icon-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 40px; height: 40px; border: none; padding: 0;
  background: transparent; color: var(--color-primary);
  border-radius: var(--radius-sm); cursor: pointer;
  transition: background var(--transition);
}
.orders-icon-btn:hover { background: var(--color-primary-soft); }
.orders-icon-btn:focus-visible { outline: none; box-shadow: var(--focus-ring); }

.orders-empty {
  padding: 56px 20px; text-align: center; color: var(--color-text-muted);
}
.orders-empty-icon { font-size: 2.5rem; opacity: 0.5; margin-bottom: 8px; }

.orders-pagination {
  display: flex; justify-content: center; gap: 8px; margin-top: 20px; flex-wrap: wrap;
}
.orders-pagination button {
  min-width: 40px; height: 40px; padding: 0 12px;
  background: var(--color-surface); color: var(--color-text);
  border: 1px solid var(--color-border); border-radius: var(--radius-sm);
  font-weight: 600; cursor: pointer;
  transition: background var(--transition), border-color var(--transition);
}
.orders-pagination button:hover { border-color: var(--color-primary); }
.orders-pagination button.active {
  background: var(--color-primary); border-color: var(--color-primary); color: #fff;
}

.orders-backdrop {
  position: fixed; inset: 0; z-index: 50;
  display: flex; align-items: center; justify-content: center; padding: 16px;
  background: rgba(17, 24, 39, 0.45);
}
.orders-modal {
  width: min(460px, 100%);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: 24px;
}
.orders-modal h2 { margin: 0 0 20px; font-size: 1.15rem; font-weight: 700; }
.orders-modal-actions { display: flex; gap: 12px; margin-top: 24px; }
.orders-modal-actions .btn { flex: 1; }
.orders-fade-enter-active, .orders-fade-leave-active { transition: opacity 0.2s ease; }
.orders-fade-enter-from, .orders-fade-leave-to { opacity: 0; }

/* mobile: each row becomes a card */
@media (max-width: 720px) {
  .orders-table thead { display: none; }
  .orders-table, .orders-table tbody, .orders-table tr, .orders-table td { display: block; width: 100%; }
  .orders-table tr { padding: 14px 16px; border-top: 1px solid var(--color-border); }
  .orders-table tbody tr:first-child { border-top: none; }
  .orders-table td {
    display: flex; justify-content: space-between; align-items: center; gap: 12px;
    padding: 6px 0; border: none;
  }
  .orders-table td::before {
    content: attr(data-label);
    color: var(--color-text-muted); font-size: 0.8rem; font-weight: 600;
  }
  .orders-table td.col-action { width: 100%; justify-content: flex-end; }
  .orders-table td.col-action::before { content: none; }
}
</style>
