<template>
  <div class="profile-card">
    <div class="image-container">
      <div class="profile-circle" role="button" tabindex="0" :aria-label="$t('customerSettings.uploadAria')" @click="triggerImageUpload" @keydown.enter="triggerImageUpload">
        <img v-if="userData.profile_image" :src="userData.profile_image" :alt="$t('customerSettings.profileAlt')" class="profile-img"/>
        <span v-else class="upload-placeholder">+</span>
      </div>
      <input type="file" accept="image/*" ref="fileInput" @change="handleImageChange" hidden />
    </div>

    <form @submit.prevent="saveProfile" class="profile-form">
      <fieldset v-if="isSeller" class="store-section">
        <legend>{{ $t('customerSettings.store') }}</legend>
        <div class="store-row">
          <div class="store-logo" role="button" tabindex="0" :aria-label="$t('customerSettings.uploadStoreAria')" @click="$refs.storeInput.click()" @keydown.enter="$refs.storeInput.click()">
            <img v-if="userData.store_image" :src="userData.store_image" :alt="$t('customerSettings.storeAlt')" class="profile-img"/>
            <span v-else class="upload-placeholder">+</span>
          </div>
          <input type="file" accept="image/*" ref="storeInput" @change="handleStoreImageChange" hidden />
          <div class="input-group">
            <input type="text" v-model="userData.store_name" maxlength="20" required />
            <label>{{ $t('customerSettings.storeName') }}</label>
            <span class="bar"></span>
          </div>
        </div>
      </fieldset>

      <div class="row">
        <div class="input-group">
          <input type="text" v-model="userData.first_name" required />
          <label>{{ $t('customerSettings.firstName') }}</label>
          <span class="bar"></span>
        </div>
        <div class="input-group">
          <input type="text" v-model="userData.last_name" required />
          <label>{{ $t('customerSettings.lastName') }}</label>
          <span class="bar"></span>
        </div>
      </div>

      <div class="input-group full-width">
        <input type="tel" v-model="userData.phone_number" />
        <label>{{ $t('customerSettings.phone') }}</label>
        <span class="bar"></span>
      </div>

      <div class="button-group">
        <button type="submit" class="btn btn-primary">{{ $t('customerSettings.save') }}</button>
        <router-link  type="button" :to="'/'" class="btn btn-outline">{{ $t('customerSettings.cancel') }}</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import api, { API_URL } from '@/services/api';
import { useRoleStore } from '@/stores/role';

export default {
  mounted(){
    this.retreivedata()
  },
  data() {
    return {
      user_id: null,
      userData: {
        first_name: '',
        last_name: '',
        phone_number: '',
        profile_image: null,
        store_name: '',
        store_image: null
    },
      original: {},
      selectedFile: null,
      selectedStoreFile: null
    };
  },
  computed: {
    isSeller() {
      return useRoleStore().role === 'seller'
    }
  },
  methods: {
    triggerImageUpload() {
      const response = this.$refs.fileInput.click();
    },
    handleImageChange(event) {
      const file = event.target.files[0];
      
      if (file && file.type.startsWith('image/')) {
        this.selectedFile = file;

        // Create a temporary URL for the preview
        this.userData.profile_image = URL.createObjectURL(file);
      } else {
        alert(this.$t('customerSettings.invalidImage'));
      }
    },
    handleStoreImageChange(event) {
      const file = event.target.files[0];
      if (file && file.type.startsWith('image/')) {
        this.selectedStoreFile = file;
        this.userData.store_image = URL.createObjectURL(file);
      } else {
        alert(this.$t('customerSettings.invalidImage'));
      }
    },
    async retreivedata(){
      const url = '/signup/get_id/me'
      const response = await api.get(url)
      const data = response.data
      this.userData = {
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        phone_number: data.phone_number || '',
        profile_image: data.profile_image ? API_URL + data.profile_image : null,
        store_name: data.store_name || '',
        store_image: data.store_image ? API_URL + data.store_image : null,
      }
      this.original = { ...this.userData }
      this.user_id = data.id
    },
    async saveProfile() {
      const formData = new FormData();
      const keys = ['first_name', 'last_name', 'phone_number']
      if (this.isSeller) keys.push('store_name')
      for (const key of keys) {
        if (this.userData[key] !== this.original[key]) {
          formData.append(key, this.userData[key]);
        }
      }
      if (this.selectedFile) {
        formData.append('profile_image', this.selectedFile);
      }
      if (this.isSeller && this.selectedStoreFile) {
        formData.append('store_image', this.selectedStoreFile);
      }

      try{
        const role = this.isSeller ? 'seller' : 'customer'
        const url = '/signup/' + role + '/' + this.user_id + '/'

        const response = await api.patch(url, formData)
        this.$router.push('/')
    }
      catch(error){
        console.log(error.response)
      }
    },
    debouncedSearch() {

      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.fetchResults();
      }, 300);
    },

    async fetchResults() {
      if (!this.searchQuery) {
        this.products = [];
        return;
      }

      this.loading = true;
      try {
        const response = await api.get('/core/products/', {
          params: {
            search: this.searchQuery
          }
        });

        this.$emit('search', {'results': response.data})
      } catch (error) {
        console.error("Error fetching search results:", error);
      } finally {
        this.loading = false;
      }
    },
  }
};
</script>

<style scoped>
.profile-card {
  display: grid;
  position: relative;
  margin: 8% auto 2rem;
  width: min(560px, calc(100% - 2rem));
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: 2rem;
}
.image-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}
.profile-circle {
  width: 120px;
  height: 120px;
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  transition: border-color var(--transition);
}
.profile-circle:hover { border-color: var(--color-primary); }
.profile-img {
  position: relative;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.upload-placeholder {
  font-size: 2rem;
  color: var(--color-text-muted);
}
.row {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}
.input-group {
  position: relative;
  flex: 1;
  padding-top: 1.5rem;
}
.input-group input {
  display: block;
  width: 100%;
  min-height: 44px;
}
.input-group label {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  font-weight: 600;
  position: absolute;
  pointer-events: none;
  inset-inline-start: 0;
  top: 0;
  transition: color var(--transition);
}
.input-group input:focus ~ label { color: var(--color-primary); }
.input-group .bar { display: none; }
.full-width { margin-bottom: 2rem; }
.store-section {
  margin: 0 0 1.5rem;
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}
.store-section legend {
  padding: 0 0.4rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-muted);
}
.store-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.store-logo {
  flex: none;
  width: 72px;
  height: 72px;
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  transition: border-color var(--transition);
}
.store-logo:hover { border-color: var(--color-primary); }
.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}
.button-group .btn { flex: 1; }
@media (max-width: 520px) {
  .row { flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; }
  .profile-card { margin-top: 5rem; padding: 1.25rem; }
}
</style>
