<template>
  <button type="button" class="lang-switcher" :aria-label="$t('common.switchLanguage')"
    :title="$t('common.switchLanguage')" @click="toggle">
    <span>{{ $i18n.locale === 'ar' ? 'EN' : 'عربي' }}</span>
  </button>
</template>

<script>
import { setLocale } from '@/i18n'

export default {
  name: 'LangSwitcher',
  methods: {
    toggle() {
      setLocale(this.$i18n.locale === 'ar' ? 'en' : 'ar')
    },
  },
}
</script>

<style scoped>
.lang-switcher {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 36px;
  padding: 0 0.75rem;
  color: inherit;
  font-weight: 600;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: var(--radius-sm);
  cursor: pointer;
}
.lang-switcher:hover { background: rgba(255, 255, 255, 0.22); }
</style>
