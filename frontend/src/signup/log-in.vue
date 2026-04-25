<template>
    <div class="signup-container">
    <div class="signup-card">
        <h1 class="title">Login</h1>

        <form @submit.prevent="handleSignup">

        <!-- First + Last Name -->
        <div class="row">
            <input
            type="text"
            placeholder="User name"
            v-model="form.username"
            class="input"
            />
        </div>

        <!-- Password -->
        <div class="row">
            <input
            type="password"
            placeholder="Password"
            v-model="form.password"
            class="input"
            />
        </div>

        <!-- Buttons -->
        <div class="button-row">
            <button type="submit" @click="submitForm" class="btn secondary">
            Login
            </button>
        </div>
        <footer style="padding: 5px;"> don't have an account? 
            <router-link :to="'/signup'" style="color: blue;">
                register here
            </router-link> 
        </footer>
        </form>
    </div>
    </div>
</template>
<script>
import api from '@/services/api';
import { mapActions, mapState } from 'pinia'
import {useRoleStore} from '@/stores/role.js';

export default {
        computed: {
            ...mapState(useRoleStore, ['role'])
        },

        data(){
            return {
                chat_id: 1,
                form: {
                username:'',
                password: '',
                    }
                }
            },

        methods:{
            ...mapActions(useRoleStore, ['set_role']),
            
            async submitForm(){
                try{
                    const response = await api.post('http://127.0.0.1:8000/api/token/', this.form);
                    this.$router.push('/');
                    this.startchat();
                    this.set_role(response.data['user_type'])
                }
                catch(error){
                    console.log(error)
                }
            },
            async startchat(){
                    try{
                    const response = await api.post('/chat/chat/', {user: 1});
                    this.chat_id = response.data['chat_id']
                    }
                    catch(error){
                    }
                }
        }
}
</script>

<style scoped>

.signup-container {
    height: 100vh;
    width: 100vw;
    position: relative;
    border-radius: 0px;
    margin: 0;
    justify-content: center;
  background-image: radial-gradient(circle, #a4a4a4 0%, #6f829e 100%);
}

.signup-card {
    height: 50%;
    width: 25%;
    margin: auto;
    justify-content: center;
    align-content: center;
    padding: 25px 60px;
    box-shadow: 8px 8px 20px rgba(0, 0, 0, 0.35);
    background: #ffffff;
  background-image: radial-gradient(circle, #ffffff 50%, #f4f4f4 );
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
</style>