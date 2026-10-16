<template>
    <div class="signup-container">
    <lang-switcher class="floating-lang" />
    <div class="signup-card">
        <h1 class="title">{{ $t('login.title') }}</h1>

        <form @submit.prevent="submitForm" novalidate>

        <div v-if="formError" class="form-error" role="alert">
            {{ formError }}
        </div>

        <div class="field">
            <label for="username" class="label">{{ $t('login.username') }}</label>
            <div class="row" :class="{ invalid: errors.username }">
                <input
                id="username"
                ref="username"
                type="text"
                :placeholder="$t('login.username')"
                autocomplete="username"
                autofocus
                v-model.trim="form.username"
                class="input"
                :aria-invalid="!!errors.username"
                aria-describedby="username-error"
                @input="clearError('username')"
                />
            </div>
            <p v-if="errors.username" id="username-error" class="field-error" role="alert">
                {{ errors.username }}
            </p>
        </div>

        <div class="field">
            <label for="password" class="label">{{ $t('login.password') }}</label>
            <div class="row password" :class="{ invalid: errors.password }">
                <input
                id="password"
                ref="password"
                :type="passwordVisible ? 'text' : 'password'"
                :placeholder="$t('login.password')"
                autocomplete="current-password"
                v-model="form.password"
                class="input input-bare"
                :aria-invalid="!!errors.password"
                aria-describedby="password-error"
                @input="clearError('password')"
                @keyup="capsLock = $event.getModifierState && $event.getModifierState('CapsLock')"
                @blur="capsLock = false"
                />

                <button
                type="button"
                class="toggle-icon"
                :aria-label="passwordVisible ? $t('login.hidePassword') : $t('login.showPassword')"
                :aria-pressed="passwordVisible"
                @click="passwordVisible = !passwordVisible"
                >
                    <Eye v-if="passwordVisible"/>
                    <EyeOff v-else/>
                </button>
            </div>
            <p v-if="errors.password" id="password-error" class="field-error" role="alert">
                {{ errors.password }}
            </p>
            <p v-else-if="capsLock" class="field-hint">{{ $t('login.capsLock') }}</p>
        </div>

        <div class="button-row">
            <button type="submit" class="btn btn-primary submit-btn" :disabled="loading">
                <span v-if="loading" class="spinner" aria-hidden="true"></span>
                {{ loading ? $t('login.loggingIn') : $t('login.submit') }}
            </button>
        </div>
        <footer class="footer"> {{ $t('login.noAccount') }}
            <router-link :to="'/signup'" class="link">
                {{ $t('login.registerHere') }}
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
import { Eye, EyeOff } from '@lucide/vue';
export default {
    components: {EyeOff, Eye},
        computed: {
            ...mapState(useRoleStore, ['role'])
        },

        data(){
            return {
                chat_id: 1,
                form: {
                username:'',
                password: '',
                    },
                errors: {},
                formError: '',
                loading: false,
                capsLock: false,
                passwordVisible: false
                }
            },

        methods:{
            ...mapActions(useRoleStore, ['set_role']),

            clearError(field){
                if (this.errors[field]) {
                    this.errors = { ...this.errors, [field]: '' }
                }
                this.formError = ''
            },

            validate(){
                const errors = {}
                if (!this.form.username) errors.username = this.$t('login.errors.usernameRequired')
                if (!this.form.password) errors.password = this.$t('login.errors.passwordRequired')
                this.errors = errors
                const firstInvalid = ['username', 'password'].find(f => errors[f])
                if (firstInvalid) this.$refs[firstInvalid].focus()
                return !firstInvalid
            },

            describeError(error){
                if (!error.response) {
                    return this.$t('login.errors.network')
                }
                const { status, data } = error.response
                if (status === 400 || status === 401) {
                    return this.$t('login.errors.wrongCredentials')
                }
                if (status === 429) {
                    return this.$t('login.errors.tooMany')
                }
                if (status >= 500) {
                    return this.$t('login.errors.server')
                }
                return (data && data.detail) || this.$t('login.errors.failed')
            },

            async submitForm(){
                if (this.loading || !this.validate()) return
                this.loading = true
                this.formError = ''
                try{
                    const response = await api.post('/api/token/', this.form);
                    this.set_role(response.data['user_type'])
                    this.startchat();
                    this.$router.push('/');
                }
                catch(error){
                    this.formError = this.describeError(error)
                    this.form.password = ''
                    this.$refs.password.focus()
                }
                finally{
                    this.loading = false
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
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
  background: var(--color-bg);
}
.signup-card {
  width: 100%;
  max-width: 420px;
  padding: 32px 32px 24px;
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
}
.title {
  text-align: center;
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 24px;
  color: var(--color-text);
}
.form-error {
  background: var(--color-error-soft);
  color: var(--color-error);
  border: 1px solid var(--color-error);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  margin-bottom: 16px;
  font-size: 0.9rem;
}
.field { margin-bottom: 16px; }
.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--color-text);
}
.row {
  display: flex;
  align-items: center;
  min-height: 44px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  transition: border-color var(--transition), box-shadow var(--transition);
}
.row:hover { border-color: var(--color-text-muted); }
.row:focus-within {
  border-color: var(--color-primary);
  box-shadow: var(--focus-ring);
}
.row.invalid { border-color: var(--color-error); }
.row.invalid:focus-within { box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.3); }
.input,
.input:focus {
  width: 100%;
  min-height: 42px;
  padding: 0.6rem 0.9rem;
  color: var(--color-text);
  font-size: 1rem;
  border: none;
  border-radius: var(--radius-sm);
  outline: none;
  box-shadow: none;
  background: transparent;
}
.toggle-icon {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  min-height: 40px;
  padding: 0;
  color: var(--color-text-muted);
  border-radius: var(--radius-sm);
}
.toggle-icon:hover { color: var(--color-text); }
.field-error {
  margin: 6px 0 0;
  font-size: 0.85rem;
  color: var(--color-error);
}
.field-hint {
  margin: 6px 0 0;
  font-size: 0.85rem;
  color: var(--color-text-muted);
}
.button-row { display: flex; margin-top: 24px; }
.submit-btn {
  width: 100%;
  min-height: 44px;
  margin-top: 0;
  font-size: 1rem;
  cursor: pointer;
}
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.footer {
  padding: 16px 5px 4px;
  text-align: center;
  font-size: 0.9rem;
  color: var(--color-text-muted);
}
.link {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}
.link:hover { color: var(--color-primary-hover); text-decoration: underline; }
@media (max-width: 480px) {
  .signup-card { padding: 24px 18px 20px; }
  .title { font-size: 1.5rem; }
}
</style>
