<template>
  <button type="button" class="lang-switcher" :aria-label="$t('common.switchLanguage')"
    :title="$t('common.switchLanguage')" @click="toggle">
    <svg v-if="$i18n.locale === 'ar'" class="flag" viewBox="0 0 20 14" aria-hidden="true">
      <rect width="20" height="14" fill="#fff" />
      <g fill="#b22234">
        <rect y="0" width="20" height="2" /><rect y="4" width="20" height="2" />
        <rect y="8" width="20" height="2" /><rect y="12" width="20" height="2" />
      </g>
      <rect width="9" height="8" fill="#3c3b6e" />
    </svg>
    <svg v-else class="flag" viewBox="0 0 20 14" aria-hidden="true">
      <rect width="20" height="14" fill="#006c35" />
      <rect x="4" y="5.5" width="12" height="1.5" fill="#fff" />
      <rect x="6" y="9" width="8" height="1" fill="#fff" />
    </svg>
    <span>{{ $i18n.locale === 'ar' ? 'EN' : 'AR' }}</span>
    <svg class="chevron" viewBox="0 0 10 6" aria-hidden="true">
      <path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
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
.flag { width: 20px; height: 14px; border-radius: 2px; flex-shrink: 0; }
.chevron { width: 10px; height: 6px; flex-shrink: 0; }
.lang-switcher:hover { background: rgba(255, 255, 255, 0.22); }
</style>
