<template>
  <auth-card :title="$t('accountEmail.forgotTitle')">
    <p v-if="sent" class="msg ok" role="status">{{ $t('accountEmail.resetSent') }}</p>
    <form v-else novalidate @submit.prevent="submit">
      <p class="msg">{{ $t('accountEmail.forgotHint') }}</p>
      <label for="fp-email">{{ $t('accountEmail.email') }}</label>
      <input id="fp-email" v-model.trim="email" type="email" autocomplete="email" autofocus />
      <p v-if="error" class="msg error" role="alert">{{ error }}</p>
      <button type="submit" class="btn btn-primary" :disabled="loading || !email">{{ $t('accountEmail.sendLink') }}</button>
    </form>
    <p class="links"><router-link to="/login">{{ $t('accountEmail.backToLogin') }}</router-link></p>
  </auth-card>
</template>

<script>
import api from '@/services/api';
import AuthCard from './auth-card.vue';

export default {
  components: { AuthCard },
  data() { return { email: '', sent: false, loading: false, error: '' } },
  methods: {
    async submit() {
      this.loading = true
      this.error = ''
      try {
        await api.post('/signup/password-reset/', { email: this.email })
        this.sent = true
      } catch (e) {
        this.error = e.response?.status === 429 ? this.$t('accountEmail.tooMany') : this.$t('accountEmail.failed')
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
