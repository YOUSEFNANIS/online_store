import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(() => ({
  plugins: [
    vue(),
    // The overlay is useful when explicitly requested, but adds more than 2 MB
    // of development-only modules to every measured page load.
    process.env.VITE_ENABLE_DEVTOOLS === 'true' && vueDevTools(),
  ].filter(Boolean),
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: '127.0.0.1',
    port: 5173,
  watch: {
    usePolling: true,
  },
},
}))
