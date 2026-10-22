<template>
  <div class="inv">
    <header class="head">
      <div>
        <h1>{{ $t('sellerTools.inventoryTitle') }}</h1>
        <p>{{ $t('sellerTools.inventorySub', { low: LOW }) }}</p>
      </div>
      <router-link to="/products/create" class="btn btn-primary">{{ $t('nav.newProduct') }}</router-link>
    </header>

    <section class="card import">
      <h2>{{ $t('sellerTools.importTitle') }}</h2>
      <p class="muted">{{ $t('sellerTools.importHelp') }}</p>
      <div class="import-row">
        <input ref="file" type="file" accept=".csv,text/csv" @change="importResult = null" />
        <button type="button" class="btn btn-primary" :disabled="importing" @click="runImport">{{ $t('sellerTools.upload') }}</button>
        <button type="button" class="btn btn-outline" @click="downloadTemplate">{{ $t('sellerTools.template') }}</button>
      </div>
      <p v-if="importResult?.ok" class="ok" role="status">{{ $t('sellerTools.imported', { count: importResult.created }) }}</p>
      <div v-else-if="importResult" class="err" role="alert">
        <p>{{ importResult.detail }}</p>
        <ul v-if="importResult.errors?.length">
          <li v-for="e in importResult.errors" :key="e.line">{{ $t('sellerTools.line', { line: e.line }) }}: {{ flatten(e.errors) }}</li>
        </ul>
      </div>
    </section>

    <section class="card">
      <div class="toolbar">
        <input v-model.trim="search" type="search" :placeholder="$t('sellerTools.searchProducts')" @input="debouncedLoad" />
      </div>
      <p v-if="failed" class="err" role="alert">{{ $t('sellerTools.loadFailed') }}</p>
      <p v-else-if="loaded && !products.length" class="muted">{{ $t('sellerTools.noProducts') }}</p>
      <table v-else class="table">
        <thead>
          <tr>
            <th>{{ $t('sellerTools.product') }}</th>
            <th>{{ $t('sellerTools.category') }}</th>
            <th>{{ $t('sellerTools.price') }}</th>
            <th>{{ $t('sellerTools.stock') }}</th>
            <th><span class="sr-only">{{ $t('sellerTools.save') }}</span></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id" :class="{ low: Number(p.inventory) <= LOW }">
            <td :data-label="$t('sellerTools.product')"><router-link :to="'/products/' + p.id">{{ p.name }}</router-link></td>
            <td :data-label="$t('sellerTools.category')">
              <select v-model="p.category" @change="dirty(p)">
                <option :value="null">—</option>
                <option v-for="c in catalog.categories" :key="c.id" :value="c.id">{{ catalog.nameOf(c, $i18n.locale) }}</option>
              </select>
            </td>
            <td :data-label="$t('sellerTools.price')"><input v-model="p.price" type="number" min="0" step="0.01" @input="dirty(p)" /></td>
            <td :data-label="$t('sellerTools.stock')">
              <input v-model.number="p.inventory" type="number" min="0" step="1" @input="dirty(p)" />
              <span v-if="Number(p.inventory) <= LOW" class="badge">{{ Number(p.inventory) === 0 ? $t('sellerTools.out') : $t('sellerTools.lowBadge') }}</span>
            </td>
            <td class="act">
              <button type="button" class="btn btn-primary small" :disabled="!changed[p.id] || saving[p.id]" @click="save(p)">
                {{ saved[p.id] ? '✓' : $t('sellerTools.save') }}
              </button>
              <p v-if="rowError[p.id]" class="err small-text">{{ rowError[p.id] }}</p>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="pages > 1" class="pager">
        <button type="button" :disabled="page <= 1" @click="load(page - 1)">{{ $t('storefront.prev') }}</button>
        <span>{{ $t('storefront.pageOf', { page, total: pages }) }}</span>
        <button type="button" :disabled="page >= pages" @click="load(page + 1)">{{ $t('storefront.next') }}</button>
      </div>
    </section>
  </div>
</template>

<script>
import api from '@/services/api';
import { useCatalogStore } from '@/stores/catalog';

const LOW = 5 // keep in step with LOW_STOCK_THRESHOLD in core/seller_tools.py

export default {
  name: 'SellerInventory',
  data() {
    return {
      LOW, products: [], page: 1, pages: 1, search: '', loaded: false, failed: false, timer: null,
      changed: {}, saving: {}, saved: {}, rowError: {}, importing: false, importResult: null,
    }
  },
  computed: { catalog() { return useCatalogStore() } },
  created() { this.catalog.load() },
  mounted() { this.load(1) },
  beforeUnmount() { clearTimeout(this.timer) },
  methods: {
    async load(page) {
      try {
        const params = { page, ordering: 'inventory' }
        if (this.search) params.search = this.search
        const { data } = await api.get('/core/products/', { params })
        this.products = data.results
        this.page = page
        this.pages = data.total_pages || 1
        this.changed = {}
        this.failed = false
      } catch (e) {
        this.failed = true
      }
      this.loaded = true
    },
    debouncedLoad() {
      clearTimeout(this.timer)
      this.timer = setTimeout(() => this.load(1), 300)
    },
    dirty(p) {
      this.changed[p.id] = true
      this.saved[p.id] = false
      this.rowError[p.id] = ''
    },
    async save(p) {
      this.saving[p.id] = true
      try {
        await api.patch(`/core/products/${p.id}/`, { price: p.price, inventory: Number(p.inventory), category: p.category })
        this.changed[p.id] = false
        this.saved[p.id] = true
      } catch (e) {
        const data = e.response?.data
        this.rowError[p.id] = data ? Object.values(data).flat().join(' ') : this.$t('sellerTools.saveFailed')
      } finally {
        this.saving[p.id] = false
      }
    },
    async runImport() {
      const file = this.$refs.file.files[0]
      if (!file) return
      this.importing = true
      this.importResult = null
      try {
        const body = new FormData()
        body.append('file', file)
        const { data } = await api.post('/core/seller/import/products/', body, { headers: { 'Content-Type': 'multipart/form-data' } })
        this.importResult = { ok: true, created: data.created }
        this.$refs.file.value = ''
        this.load(1)
      } catch (e) {
        this.importResult = { ok: false, detail: e.response?.data?.detail || this.$t('sellerTools.importFailed'), errors: e.response?.data?.errors }
      } finally {
        this.importing = false
      }
    },
    flatten(errors) {
      return Object.entries(errors).map(([field, msgs]) => `${field}: ${[].concat(msgs).join(' ')}`).join('; ')
    },
    downloadTemplate() {
      const csv = '﻿name,description,price,inventory,category\nExample mug,Ceramic mug,12.50,20,home-garden\n'
      const href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }))
      const link = document.createElement('a')
      link.href = href
      link.download = 'products-template.csv'
      link.click()
      URL.revokeObjectURL(href)
    },
  },
}
</script>

<style scoped>
.inv { display: block; width: min(1100px, 92%); height: auto; margin: 130px auto 2rem; }
.head { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 1.25rem; }
.head h1 { margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--color-text); }
.head p, .muted { margin: 0.25rem 0 0; color: var(--color-text-muted); font-size: 0.92rem; }
.card { margin-bottom: 1rem; padding: 1.25rem; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); }
.card h2 { margin: 0; font-size: 1rem; font-weight: 600; }
.import-row { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem; margin-top: 0.75rem; }
.ok { margin: 0.75rem 0 0; color: #166534; }
.err { margin: 0.75rem 0 0; color: var(--color-error); font-size: 0.9rem; }
.err ul { margin: 0.25rem 0 0; padding-inline-start: 1.2rem; }
.toolbar { margin-bottom: 0.75rem; }
.toolbar input { width: min(320px, 100%); }
.table { width: 100%; border-collapse: collapse; text-align: start; }
.table th { padding: 8px 10px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--color-text-muted); text-align: start; border-bottom: 1px solid var(--color-border); }
.table td { padding: 8px 10px; border-top: 1px solid var(--color-border); vertical-align: middle; }
.table tbody tr:first-child td { border-top: none; }
.table td input[type=number] { width: 90px; }
.low { background: #fffbeb; }
.badge { margin-inline-start: 8px; padding: 2px 8px; border-radius: 999px; background: #fef3c7; color: #92400e; font-size: 0.75rem; }
.act { white-space: nowrap; }
.small { padding: 4px 14px; }
.small-text { margin: 4px 0 0; font-size: 0.8rem; white-space: normal; }
.pager { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-top: 1rem; font-size: 0.9rem; color: var(--color-text-muted); }
.pager button { padding: 0.4rem 1rem; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); cursor: pointer; }
.pager button:disabled { opacity: 0.5; cursor: not-allowed; }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
@media (max-width: 700px) {
  .head { flex-direction: column; }
  .table thead { display: none; }
  .table td { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
  .table td::before { content: attr(data-label); color: var(--color-text-muted); }
}
</style>
