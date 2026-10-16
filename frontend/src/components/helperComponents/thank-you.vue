<template>
  <div class="success-container">

    <div class="success-card">

      <div class="success-icon">
        ✓
      </div>

      <h1 class="title">
        {{ $t('thankYou.title') }}
      </h1>

      <p class="message">
        {{ $t('thankYou.message') }}
      </p>

      <!-- Optional Order Number -->
      <p v-if="orderId" class="order-id">
        {{ $t('thankYou.orderNumber') }} <strong>#{{ orderId }}</strong>
      </p>
      <router-link :to="'/'"  class="btn btn-primary">
        {{ $t('thankYou.home') }}
      </router-link>

    </div>

  </div>
</template>

<script>
import router from '@/router';

export default {
  props: {
    orderId: {
      type: [String, Number],
      default: null
    }
  }
}
</script>

<style scoped>
.success-container {
  min-height: 100vh;
  background: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.success-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 48px 32px;
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: var(--shadow-md);
}
.success-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 24px;
  background: var(--color-success-soft);
  color: var(--color-success);
  border: 2px solid var(--color-success);
  font-size: 36px;
  font-weight: 700;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.title {
  font-size: 1.6rem;
  font-weight: 700;
  margin: 0 0 10px;
  color: var(--color-text);
}
.message {
  font-size: 1.1rem;
  color: var(--color-text-muted);
  margin: 0 0 24px;
}
.order-id {
  font-size: 1rem;
  margin: 0 0 28px;
  color: var(--color-text);
}
</style>
