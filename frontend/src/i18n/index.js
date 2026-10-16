import { createI18n } from 'vue-i18n'

const STORAGE_KEY = 'locale'
const SUPPORTED = ['en', 'ar']

// Each file under locales/<lang>/<namespace>.json becomes messages[lang][namespace]
function loadMessages() {
  const messages = { en: {}, ar: {} }
  const modules = import.meta.glob('./locales/*/*.json', { eager: true })
  for (const path in modules) {
    const [, lang, file] = path.match(/\.\/locales\/(\w+)\/(.+)\.json$/)
    messages[lang][file] = modules[path].default
  }
  return messages
}

function initialLocale() {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (SUPPORTED.includes(saved)) return saved
  return navigator.language?.startsWith('ar') ? 'ar' : 'en'
}

export function applyDocumentLocale(locale) {
  document.documentElement.lang = locale
  document.documentElement.dir = locale === 'ar' ? 'rtl' : 'ltr'
}

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: initialLocale(),
  fallbackLocale: 'en',
  messages: loadMessages(),
})

export function setLocale(locale) {
  if (!SUPPORTED.includes(locale)) return
  i18n.global.locale.value = locale
  localStorage.setItem(STORAGE_KEY, locale)
  applyDocumentLocale(locale)
}

applyDocumentLocale(i18n.global.locale.value)

export default i18n
