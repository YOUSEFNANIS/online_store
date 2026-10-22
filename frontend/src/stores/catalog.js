import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/api'

export const useCatalogStore = defineStore('catalog', () => {
  const categories = ref([])
  let loading = null

  function load() {
    if (categories.value.length) return Promise.resolve()
    if (!loading) {
      loading = api.get('/core/categories/')
        .then((response) => { categories.value = response.data })
        .catch(() => { /* categories are optional; the UI hides the filter */ })
        .finally(() => { loading = null })
    }
    return loading
  }

  function nameOf(category, locale) {
    return locale === 'ar' ? category.name_ar : category.name_en
  }

  return { categories, load, nameOf }
})
