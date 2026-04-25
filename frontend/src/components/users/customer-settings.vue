<template>
  <div class="profile-card">
    <div class="image-container">
      <div class="profile-circle" @click="triggerImageUpload">
        <img v-if="userData.profile_image" :src="userData.profile_image" alt="Profile" class="profile-img"/>
        <span v-else class="upload-placeholder">+</span>
      </div>
      <input type="file" ref="fileInput" @change="handleImageChange" hidden />
    </div>

    <form @submit.prevent="saveProfile" class="profile-form">
      <div class="row">
        <div class="input-group">
          <input type="text" v-model="userData.first_name" required />
          <label>first name</label>
          <span class="bar"></span>
        </div>
        <div class="input-group">
          <input type="text" v-model="userData.last_name" required />
          <label>last name</label>
          <span class="bar"></span>
        </div>
      </div>

      <div class="input-group full-width">
        <input type="tel" v-model="userData.phone_number" required />
        <label>phone number</label>
        <span class="bar"></span>
      </div>

      <div class="button-group">
        <button type="submit" class="btn">save</button>
        <router-link  type="button" :to="'/'" class="btn">cancel</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import api from '@/services/api';

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
        profile_image: null
    },
      selectedFile: null
    };
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
        alert("Please select a valid image file.");
      }
    },
    async retreivedata(){
      const url = 'http://127.0.0.1:8000/signup/get_id/me'
      const response = await api.get(url)
      this.userData = response.data
      this.userData.profile_image = 'http://127.0.0.1:8000'+ this.userData.profile_image
      this.user_id = response.data.id
    },
    async saveProfile() {
      const formData = new FormData();
      formData.append('first_name', this.userData.first_name);
      formData.append('last_name', this.userData.last_name);
      formData.append('phone_number', this.userData.phone_number);
      formData.append('profile_image', this.selectedFile);

      try{
        const url = 'http://127.0.0.1:8000/signup/seller/' + this.user_id + '/'

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
        const response = await api.get('http://127.0.0.1:8000/core/products/', {
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
/* Container styling */
.profile-card {
  display: grid;
  position: relative;
  margin-top: 10%; 
  margin-left: 30%;
  max-width: 100%;
  width: fit-content;
  background: #eeeeee; /* Matching the blue border from your image */
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
}

/* Profile Image */
.image-container {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.profile-circle {
  width: 120px;
  height: 120px;
  background-color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.2s ease;
}

.profile-circle:hover {
  transform: scale(1.05);
}
.profile-img{
  position: relative;
  width: 100%;
  object-fit: contain;
  justify-content: center;
}
.upload-placeholder {
  font-size: 2rem;
  color: #ccc;
}

/* Input Fields (Underline style) */
.row {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.input-group {
  position: relative;
  flex: 1;
}

.input-group input {
  font-size: 16px;
  padding: 10px 0;
  display: block;
  width: 100%;
  border: none;
  border-bottom: 1.5px solid #000;
  background: transparent;
  outline: none;
}

.input-group label {
  color: #000;
  font-size: 18px;
  font-weight: 400;
  position: absolute;
  pointer-events: none;
  left: 0;
  top: 10px;
  transition: 0.2s ease all;
}

/* Floating label effect when typing */
.input-group input:focus ~ label,
.input-group input:valid ~ label {
  top: -15px;
  font-size: 12px;
  color: #3b82f6;
}

.input-group .bar {
  position: relative;
  display: block;
  size: 1rem;
}

.input-group .bar:before {
  content: '';
  height: 2px;
  width: 0;
  bottom: 0px;
  position: absolute;
  background: #3b82f6;
  transition: 0.3s ease all;
  left: 0;
}

.input-group input:focus ~ .bar:before {
  width: 100%;
}

.full-width {
  margin-bottom: 40px;
}

/* Buttons */
.button-group {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.btn {
  flex: 1;
  padding: 12px;
  margin: 1rem;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  transition: opacity 0.2s ease, transform 0.1s active;
}

.btn-save, .btn-cancel {
  background-color: #000;
  color: #fff;
}

</style>