<template>
  <auth-card :title="$t('accountEmail.resetTitle')">
    <p v-if="done" class="msg ok" role="status">{{ $t('accountEmail.resetDone') }}</p>
    <form v-else novalidate @submit.prevent="submit">
      <label for="rp-password">{{ $t('accountEmail.newPassword') }}</label>
      <input id="rp-password" v-model="password" type="password" autocomplete="new-password" autofocus />
      <p class="msg hint">{{ $t('accountEmail.passwordRules') }}</p>
      <p v-if="error" class="msg error" role="alert">{{ error }}</p>
      <button type="submit" class="btn btn-primary" :disabled="loading || !password">{{ $t('accountEmail.changePassword') }}</button>
    </form>
    <p class="links"><router-link to="/login">{{ $t('accountEmail.backToLogin') }}</router-link></p>
  </auth-card>
</template>

<script>
import api from '@/services/api';
import AuthCard from './auth-card.vue';

export default {
  components: { AuthCard },
  data() { return { password: '', done: false, loading: false, error: '' } },
  methods: {
    async submit() {
      this.loading = true
      this.error = ''
      try {
        await api.post('/signup/password-reset/confirm/', {
          uid: this.$route.query.uid, token: this.$route.query.token, password: this.password,
        })
        this.done = true
      } catch (e) {
        const data = e.response?.data
        this.error = (Array.isArray(data) && data[0]) || data?.detail || this.$t('accountEmail.failed')
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
