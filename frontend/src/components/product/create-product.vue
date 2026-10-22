<template>
  <div class="main">
    <header class="page-head">
      <h1 class="page-title">{{ $t('createProduct.title') }}</h1>
      <p class="page-sub">{{ $t('createProduct.subtitle') }}</p>
    </header>

    <form class="layout" @submit.prevent="saveProduct">
      <div class="col-main">
        <section class="card">
          <h2 class="card-title">{{ $t('createProduct.details') }}</h2>

          <div class="field">
            <div class="label-row">
              <label class="label" for="p-name">{{ $t('createProduct.name') }}</label>
              <span class="hint">{{ product.name.length }}/20</span>
            </div>
            <input id="p-name" v-model="product.name" class="input" maxlength="20" :placeholder="$t('createProduct.namePlaceholder')" required/>
          </div>

          <div class="field">
            <label class="label" for="p-desc">{{ $t('createProduct.description') }}</label>
            <textarea id="p-desc" v-model="product.description" class="textarea" :placeholder="$t('createProduct.descriptionPlaceholder')"></textarea>
          </div>

          <div v-if="catalog.categories.length" class="field">
            <label class="label" for="p-cat">{{ $t('createProduct.category') }}</label>
            <select id="p-cat" v-model="product.category" class="input">
              <option value="">{{ $t('createProduct.noCategory') }}</option>
              <option v-for="c in catalog.categories" :key="c.id" :value="c.id">{{ catalog.nameOf(c, $i18n.locale) }}</option>
            </select>
          </div>
        </section>

        <section class="card">
          <h2 class="card-title">{{ $t('createProduct.media') }}</h2>

          <label class="dropzone" :class="{ active: dragging }"
                 @dragover.prevent="dragging = true" @dragleave="dragging = false" @drop.prevent="onDrop">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <span class="drop-title"><b>{{ $t('createProduct.clickToUpload') }}</b> {{ $t('createProduct.orDrag') }}</span>
            <span class="hint">{{ $t('createProduct.formats') }}</span>
            <input type="file" accept="image/png,image/jpeg,image/webp" multiple @change="uploadImage">
          </label>

          <ul v-if="imagePreviews.length" class="images">
            <li v-for="(img, index) in imagePreviews" :key="img" class="image-item">
              <img :src="img" alt=""/>
              <span v-if="index === 0" class="badge">{{ $t('createProduct.cover') }}</span>
              <button type="button" class="remove-btn" :aria-label="$t('createProduct.removeImage')" @click="removeElement(index)">&times;</button>
            </li>
          </ul>
        </section>
      </div>

      <aside class="col-side">
        <section class="card">
          <h2 class="card-title">{{ $t('createProduct.pricingStock') }}</h2>

          <div class="field">
            <label class="label" for="p-price">{{ $t('createProduct.price') }}</label>
            <div class="input-affix">
              <span class="affix">{{ $t('createProduct.currencySymbol') }}</span>
              <input id="p-price" type="number" min="0" step="0.01" v-model="product.price" class="input" placeholder="0.00" required/>
            </div>
          </div>

          <div class="field">
            <label class="label" for="p-qty">{{ $t('createProduct.quantity') }}</label>
            <input id="p-qty" type="number" min="0" v-model="product.inventory" class="input"/>
          </div>

          <button type="submit" class="btn btn-primary save-btn">{{ $t('createProduct.save') }}</button>
        </section>
      </aside>
    </form>
  </div>
</template>

<script>

import api from '@/services/api';
import { useCatalogStore } from '@/stores/catalog';


export default {

  data() {
    return {
      product: {
        name: "",
        description: "",
        price: null,
        inventory: 0,
        category: '',
        },
        imagesfile: [],
        imagePreviews: [],
        product_id: null,
        dragging: false,
    }
  },

  computed: {
    catalog() { return useCatalogStore() },
  },

  created() { this.catalog.load() },

  methods: {

    uploadImage(e) {
      this.addFiles(e.target.files)
      e.target.value = ""
    },

    onDrop(e) {
      this.dragging = false
      this.addFiles(e.dataTransfer.files)
    },

    addFiles(files) {
      for (const file of files) {
        if (!file.type.startsWith("image/")) continue
        this.imagesfile.push(file)
        this.imagePreviews.push(URL.createObjectURL(file))
      }
    },

    removeElement(i){
      URL.revokeObjectURL(this.imagePreviews[i])
      this.imagePreviews.splice(i, 1)
      this.imagesfile.splice(i, 1)
    },

    async saveProduct() {

              try{
                const response = await api.post('/core/products/', { ...this.product, category: this.product.category || null })
                      this.product_id = response.data.id
                  }
              catch(error){
                    console.log(error.response)
                  }
              try {
                const url = '/core/products/' + this.product_id + '/images/';
                // The images endpoint takes one file per request, so send them one by one in order.
                for (const file of this.imagesfile) {
                  const formData = new FormData()
                  formData.append("image", file)
                  await api.post(url, formData, { headers: { "Content-Type": "multipart/form-data" } })
                }
                this.$emit('saved', true);
                    }
              catch(error){
                      console.log(error.response)
              }


    }

  }
}
</script>

<style scoped>
.main { width: 100%; max-width: 1040px; margin: 0 auto; padding: 32px 16px 48px; box-sizing: border-box; font-size: 1rem; }
.page-head { margin-bottom: 24px; }
.page-title { color: var(--color-text); margin: 0 0 4px; font-size: 1.75rem; font-weight: 700; letter-spacing: -0.01em; }
.page-sub { margin: 0; color: var(--color-text-muted); }

.layout { display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 24px; align-items: start; }
.col-main { display: flex; flex-direction: column; gap: 24px; }
.col-side { position: sticky; top: 16px; }

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: 24px;
}
.card-title { margin: 0 0 20px; font-size: 1.05rem; font-weight: 600; color: var(--color-text); }

.field { margin-bottom: 18px; }
.label-row { display: flex; justify-content: space-between; align-items: baseline; }
.label { display: block; font-weight: 600; font-size: 0.9rem; margin-bottom: 6px; color: var(--color-text); }
.hint { font-size: 0.8rem; color: var(--color-text-muted); }

.input, .textarea {
  width: 100%; box-sizing: border-box; min-height: 44px;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font: inherit;
  transition: border-color var(--transition), box-shadow var(--transition);
}
.textarea { min-height: 140px; resize: vertical; }
.input:focus, .textarea:focus { outline: none; border-color: var(--color-primary); box-shadow: var(--focus-ring); }

.input-affix { position: relative; }
.input-affix .input { padding-inline-start: 30px; }
.affix { position: absolute; inset-inline-start: 12px; top: 50%; transform: translateY(-50%); color: var(--color-text-muted); pointer-events: none; }

.dropzone {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  padding: 32px 16px; text-align: center; cursor: pointer;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg);
  color: var(--color-text-muted);
  transition: border-color var(--transition), background var(--transition);
}
.dropzone:hover, .dropzone.active { border-color: var(--color-primary); background: var(--color-primary-soft); color: var(--color-primary); }
.dropzone input { display: none; }
.drop-title { color: var(--color-text); }
.drop-title b { color: var(--color-primary); }

.images { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 12px; margin: 16px 0 0; padding: 0; list-style: none; }
.image-item { position: relative; aspect-ratio: 1; }
.image-item img { width: 100%; height: 100%; object-fit: cover; border-radius: var(--radius-md); border: 1px solid var(--color-border); box-sizing: border-box; }
.badge { position: absolute; inset-inline-start: 6px; bottom: 6px; padding: 2px 8px; font-size: 0.72rem; font-weight: 600; border-radius: 999px; background: rgba(17, 24, 39, 0.75); color: #fff; }

.remove-btn {
  position: absolute; top: 6px; inset-inline-end: 6px;
  width: 28px; height: 28px; padding: 0;
  border: none; border-radius: 50%;
  background: rgba(17, 24, 39, 0.75); color: #fff;
  font-size: 1.1rem; line-height: 1; cursor: pointer;
  transition: background var(--transition);
}
.remove-btn:hover { background: var(--color-error); }

.save-btn { width: 100%; min-height: 46px; margin-top: 4px; }

@media (max-width: 800px) {
  .layout { grid-template-columns: 1fr; }
  .col-side { position: static; }
  .card { padding: 18px; }
}
</style>
