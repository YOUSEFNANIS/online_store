<template>
<div>
  <!-- Floating Button -->
  <div class="chat-toggle" @click="toggleChat">
    <MessageCircle/>
  </div>

  <!-- Chat Popup -->
  <div v-if="isOpen" class="chat-container">
    <!-- Header -->
    <div class="chat-header">
      <span>Chat</span>
      <button @click="startchat">+ new chat</button>
    </div>
    
    <!-- Messages -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.sender]"
      >
        {{ msg.text }}
      </div>
    </div>
    <!-- Input -->
    <div class="chat-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="Type a message..."
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
  </div>
</template>


<script>
import api from '@/services/api';
import {MessageCircle} from '@lucide/vue';
export default {
  components: {MessageCircle},
    data(){
        return  {
            chat_id: 1,
            isOpen: false,
            newMessage: '',
            messages: [],
    }
    },
    computed: {
      exceed_threshold(){
        if (this.messages.length >= 1000){
            startchat();
        }
      }
    },
    methods: {
        async sendMessage(){
            this.messages.push({
                text: this.newMessage,
                sender: 'user',
            })
            
            try{
              const url = 'http://127.0.0.1:8000/chat/chat/' + this.chat_id + '/message/'
              
              const response = await api.post(url, {message: this.newMessage}, {withCredentials: true})            
              
            this.messages.push({
                text: response.data.response,
                sender: 'bot',
            })}
            catch(error){
              if (error.response.status === 401){

                try{
                  // update_cookies()
                  this.sendMessage()
              }
                catch(error){
                  console.log(error.response.data)
                }               
              }
            }
        },
        toggleChat() {
                this.isOpen = !this.isOpen;
            },
            async startchat(){
                    try{
                    const response = await api.post('/chat/chat/', {user: 1});
                    this.chat_id = response.data['chat_id']
                    }
                    catch(error){
                    console.log(error.response.data)
                    }
                }, 
            scrollToBottom() {
      // Accessing the template ref via this.$refs
      const el = this.$refs.messagesContainer;
      if (el) {
        el.scrollTop = el.scrollHeight;
      }
    },
}}
</script>

<style scoped>
.chat-toggle {
  position: fixed;
  bottom: 30px;
  left: 30px;
  width: 60px;
  height: 60px;
  background: #000000;
  border-radius: 50%;
  color: white;
  font-size: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.chat-container {
  position: fixed;
  bottom: 100px;
  left: 60px;
  width: 500px;
  height: 600px;
  background: white;
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
}

.chat-header {
    font-size: 20px;
  padding: 10px;
  background: #575757;
  color: white;
  display: flex;
  justify-content: space-between;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.chat-messages {
    font-size: 25px;
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background: #f5f5f5;
}

.message {
  max-width: fit-content;
  padding: 17px 25px;
  margin-bottom: 8px;
  border-radius: 12px;
  word-wrap: break-word;
}

.user {
  background: #000000;
  color: white;
  align-self: flex-end;
  margin-left: auto;
}

.bot {
  background: #e0e0e0;
  align-self: flex-start;
}

.chat-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  padding: 6px;
  border: 1px solid #ccc;
}

.chat-input button {
  margin-left: 8px;
  padding: 6px 12px;
  background: #575757;
  font-size: 25px;
  border: none;
  color: white;
  cursor: pointer;
}
</style>