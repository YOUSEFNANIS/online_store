<template>
<div>
  <!-- Floating Button -->
  <div class="chat-toggle" role="button" tabindex="0" :aria-label="$t('chatbot.toggle')" @click="toggleChat" @keyup.enter="toggleChat">
    <MessageCircle/>
  </div>

  <!-- Chat Popup -->
  <div v-if="isOpen" class="chat-container">
    <!-- Header -->
    <div class="chat-header">
      <span>{{ $t('chatbot.title') }}</span>
      <button @click="startchat">{{ $t('chatbot.newChat') }}</button>
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
        :placeholder="$t('chatbot.placeholder')"
      />
      <button @click="sendMessage">{{ $t('chatbot.send') }}</button>
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
            messages: [{ text: this.$t('chatbot.greeting'), sender: 'bot' }],
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
              
              const response = await api.post(url, {message: this.newMessage, language: this.$i18n.locale}, {withCredentials: true})
              const getResponse = await api.get(url + response.data.chat_id + '/')         
              console.log(response)
            this.messages.push({
                text: getResponse.data.response,
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
  bottom: 24px;
  inset-inline-start: 24px;
  width: 56px;
  height: 56px;
  background: var(--color-primary);
  border-radius: 50%;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--shadow-md);
  transition: background var(--transition);
}
.chat-toggle:hover { background: var(--color-primary-hover); }

.chat-container {
  position: fixed;
  bottom: 92px;
  inset-inline-start: 24px;
  width: 500px;
  max-width: calc(100vw - 48px);
  height: 600px;
  max-height: calc(100vh - 120px);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1200;
}

.chat-header {
  font-size: 1.1rem;
  font-weight: 600;
  padding: 10px 14px;
  background: var(--color-nav);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.chat-header button {
  min-height: 40px;
  padding: 0 12px;
  background: transparent;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  transition: background var(--transition);
}
.chat-header button:hover { background: rgba(255, 255, 255, 0.12); }

.chat-messages {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  background: var(--color-bg);
}

.message {
  max-width: 85%;
  width: fit-content;
  font-size: 1rem;
  padding: 8px 14px;
  margin-bottom: 8px;
  border-radius: var(--radius-md);
  word-wrap: break-word;
}
.user {
  background: var(--color-primary);
  color: #fff;
  margin-inline-start: auto;
}
.bot {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 10px;
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
}
.chat-input input {
  flex: 1;
  min-height: 40px;
  min-width: 0;
}
.chat-input button {
  min-height: 40px;
  padding: 0 16px;
  background: var(--color-primary);
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-sm);
  color: #fff;
  transition: background var(--transition);
}
.chat-input button:hover { background: var(--color-primary-hover); }
@media (max-width: 600px) {
  .chat-container { inset-inline-start: 12px; bottom: 84px; max-width: calc(100vw - 24px); }
  .chat-toggle { inset-inline-start: 12px; bottom: 16px; }
}
</style>
