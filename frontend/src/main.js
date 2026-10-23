import './styles/identity.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { resetScrollMomentum } from './services/smooth-scroll'
import i18n from './i18n'
import LangSwitcher from './components/helperComponents/lang-switcher.vue'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.component('LangSwitcher', LangSwitcher)
app.use(router)
router.afterEach(resetScrollMomentum)
app.use(i18n)



app.mount('#app')
