<template>
    <div class="signup-container">
    <div class="signup-card">
        <h1 class="title">Create Account</h1>

        <form @submit.prevent="handleSignup">

        <div class="image-container">
        <div class="profile-circle" @click="triggerImageUpload">
            <img v-if="form.profile_image" :src="form.profile_image" alt="Profile" class="profile-img"/>
            <span v-else class="upload-placeholder">+</span>
        </div>
        <input type="file" ref="fileInput" @change="handleImageChange" hidden />
        </div>
        <div class="row">
            <select v-model="role" class="input select">
            <option disabled value="">Select Role</option>
            <option value="seller">Seller</option>
            <option value="customer">Customer</option>
            </select>
        </div>

        <!-- First + Last Name -->
        <div class="row">
            <input
            type="text"
            placeholder="First Name"
            v-model="form.first_name"
            class="input"
            />
            <input
            type="text"
            placeholder="Last Name"
            v-model="form.last_name"
            class="input"
            />
        </div>

        <!-- Email -->
        <div class="row">
            <input
            type="email"
            placeholder="Email"
            v-model="form.email"
            class="input"
            />
        </div>

        <div v-if="role === 'seller'" class="row">
            <input
            type="text"
            placeholder="store name"
            v-model="storeName"
            class="input"
            />
        </div>

        <div class="row">
            <input
            placeholder="phone number"
            v-model="form.phone_number"
            class="input"
            />
        </div>

        <div class="row">
            <input
            type="password"
            placeholder="Password"
            v-model="form.password"
            class="input"
            />
        </div>

        <!-- Confirm Password -->
        <div class="row">
            <input
            type="password"
            placeholder="Confirm Password"
            v-model="confirmPassword"
            class="input"
            />
        </div>

        <!-- Buttons -->
        <button type="submit" @click="submitForm" class="btn btn-primary">
            Sign Up
        </button>

        </form>
    </div>
    </div>
</template>
<script>

import api from '@/services/api';

export default {
    data() {
    return {
        form: {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        phone_number: "",
        profile_image: null
        },
        storeName: "",
        role: "",
        confirmPassword: "",
        selectedFile: null,

    };
    },
    computed:{
        password_confirmed(){
            return this.form.password === this.confirmPassword;
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
        this.form.profile_image = URL.createObjectURL(file);
        } else {
        alert("Please select a valid image file.");
        }
    },

    async submitForm(){
        if (this.password_confirmed){
            const formData = new FormData();
            try{
            if (this.role === 'seller'){
                formData.append('store_name', this.storeName);
            }
            this.form.profile_image = this.selectedFile
            const url ='http://127.0.0.1:8000/signup/'+ this.role + '/';
            formData.append('first_name', this.form.first_name);
            formData.append('last_name', this.form.last_name);
            formData.append('phone_number', this.form.phone_number);
            formData.append('email', this.form.email);
            formData.append('password', this.form.password);
            formData.append('profile_image', this.selectedFile);
            console.log(this.form.password)
            const response = await api.post(url, formData)
            this.$emit('saved', true);
            this.$router.push('/')
    }
    catch(error){
        console.log(error.response)
    }
        }
        else {alert('password is not confirmed')}
    },
    }
};

</script>
<style scoped>
.signup-container {
    min-height: 100vh;
    margin: 0;
    width: 100vw;
    top: 10%;
    position: relative;
    border-radius: 0px;
    justify-content: center;
    background: radial-gradient(circle, #a4a4a4 0%, #6f829e 100%);
}

.signup-card {
    height: fit-content;
    width: 25%;
    margin: auto;
    margin: 5% 0;
    justify-content: center;
    align-content: center;
    padding: 25px 60px;
    box-shadow: 8px 8px 20px rgba(0, 0, 0, 0.35);
    background: #ffffff;
}

.image-container {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.profile-circle {
  width: 60px;
  height: 60px;
  background-color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  border: 1px solid gray;
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

.title {
    text-align: center;
    font-size: 3rem;
    margin: 0;
    margin-bottom: 10%;
    color: #000000;
}


.row {
    display: flex;
    gap: 15px;
    opacity: 60%;
    margin-bottom: 20px;
}
.row:hover{
    opacity: 100%;
}
.row:active {
    opacity: 100%;
}
.input {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid black;
    color: rgb(0, 0, 0);
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
    font-size: 14px;
}

.select {
    cursor: pointer;
}

.button-row {
    display: flex;
    max-width: 100%;
    margin: auto;
    position: relative;
    justify-content: space-between;
    margin-top: 25px;
}

.secondary {
    background: #000000;  
    color: #ffffff;
    font-weight: bold;
    width: 100%;
    height: 105%;

}
.secondary:hover {
    opacity: 70%;
}
.btn-primary{
    width: 100%;
    height: 3rem;
    font-size: 1.6rem;
    background: black;
    color: white;
}
</style>