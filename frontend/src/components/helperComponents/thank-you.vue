<template>
  <div class="success-container">

    <div class="success-card">

      <div class="success-icon">
        ✓
      </div>

      <h1 class="title">
        شكراً لطلبك المنتج
      </h1>

      <p class="message">
        سيتم التواصل معك من قبل فريقنا في أقرب وقت ممكن
      </p>

      <!-- Optional Order Number -->
      <p v-if="orderId" class="order-id">
        رقم الطلب: <strong>#{{ orderId }}</strong>
      </p>
      <router-link :to="'/'"  class="btn">
        العودة للصفحة الرئيسية
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
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  direction: rtl;
  padding: 20px;
}

.success-card {
  background: white;
  padding: 50px 40px;
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  animation: fadeIn 0.5s ease;
}

.success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 25px;
  background: #22c55e;
  color: white;
  font-size: 40px;
  font-weight: bold;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 10px;
}

.message {
  font-size: 18px;
  color: #555;
  margin-bottom: 25px;
}

.order-id {
  font-size: 16px;
  margin-bottom: 30px;
  color: #333;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
