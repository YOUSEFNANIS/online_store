<template>
  <transition name="slide-fade">
    <div v-if="visible" class="verify-banner" role="status">
      <span>{{ sent ? $t('accountEmail.bannerSent') : $t('accountEmail.bannerText') }}</span>
      <button v-if="!sent" type="button" class="act" :disabled="sending" @click="resend">{{ $t('accountEmail.resend') }}</button>
      <button type="button" class="close" :aria-label="$t('accountEmail.dismiss')" @click="dismissed = true">&times;</button>
    </div>
  </transition>
</template>

<script>
import api from '@/services/api';
import { useRoleStore } from '@/stores/role';

export default {
  name: 'VerifyBanner',
  data() { return { unverified: false, dismissed: false, sent: false, sending: false } },
  computed: {
    role() { return useRoleStore().role },
    visible() { return !!this.role && this.unverified && !this.dismissed },
  },
  watch: { role: { immediate: true, handler() { this.check() } } },
  mounted() { window.addEventListener('email-verified', this.check) },
  beforeUnmount() { window.removeEventListener('email-verified', this.check) },
  methods: {
    async check() {
      this.unverified = false
      if (!this.role) return
      try {
        const { data } = await api.get('/signup/get_id/me/')
        this.unverified = data.email_verified === false
      } catch (e) { /* stay hidden */ }
    },
    async resend() {
      this.sending = true
      try {
        await api.post('/signup/resend-verification/')
        this.sent = true
      } catch (e) { /* the global error banner shows it */ }
      this.sending = false
    },
  },
}
</script>

<style scoped>
.verify-banner { position: fixed; inset-inline: 16px; bottom: 16px; z-index: 900; max-width: 520px; margin-inline: auto; display: flex; align-items: center; gap: 12px; padding: 10px 14px; background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; border-radius: var(--radius-md); box-shadow: var(--shadow-md); font-size: 0.9rem; }
.act { margin-inline-start: auto; padding: 4px 12px; border: 1px solid #92400e; border-radius: var(--radius-sm); background: transparent; color: inherit; cursor: pointer; }
.close { padding: 0 4px; background: none; border: none; color: inherit; font-size: 1.2rem; line-height: 1; cursor: pointer; }
</style>
