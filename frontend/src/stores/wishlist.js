import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/api'
import { useRoleStore } from '@/stores/role'

export const useWishlistStore = defineStore('wishlist', () => {
  const ids = ref([])
  const loaded = ref(false)
  const count = computed(() => ids.value.length)

  async function load() {
    if (loaded.value || useRoleStore().role !== 'customer') return
    try {
      ids.value = (await api.get('/core/wishlist/ids/')).data
      loaded.value = true
    } catch (e) { /* hearts stay empty */ }
  }

  function has(productId) {
    return ids.value.includes(productId)
  }

  // Optimistic: flip locally, roll back if the request fails.
  async function toggle(productId) {
    const wasSaved = has(productId)
    ids.value = wasSaved ? ids.value.filter((id) => id !== productId) : [...ids.value, productId]
    try {
      if (wasSaved) await api.delete(`/core/wishlist/${productId}/`)
      else await api.post('/core/wishlist/', { product: productId })
    } catch (e) {
      ids.value = wasSaved ? [...ids.value, productId] : ids.value.filter((id) => id !== productId)
    }
  }

  function reset() {
    ids.value = []
    loaded.value = false
  }

  return { ids, count, loaded, load, has, toggle, reset }
})
