<template>
  <auth-card :title="$t('accountEmail.verifyTitle')">
    <p v-if="state === 'loading'" class="msg" role="status">{{ $t('accountEmail.verifying') }}</p>
    <p v-else-if="state === 'ok'" class="msg ok" role="status">{{ $t('accountEmail.verified') }}</p>
    <p v-else class="msg error" role="alert">{{ $t('accountEmail.verifyFailed') }}</p>
    <p class="links"><router-link to="/products">{{ $t('accountEmail.continue') }}</router-link></p>
  </auth-card>
</template>

<script>
import api from '@/services/api';
import AuthCard from './auth-card.vue';

export default {
  components: { AuthCard },
  data() { return { state: 'loading' } },
  async mounted() {
    try {
      await api.post('/signup/verify-email/', { uid: this.$route.query.uid, token: this.$route.query.token })
      this.state = 'ok'
      window.dispatchEvent(new CustomEvent('email-verified'))
    } catch (e) {
      this.state = 'error'
    }
  },
}
</script>
