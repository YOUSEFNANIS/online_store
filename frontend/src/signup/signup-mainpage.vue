<template>
    <div class="signup-container">
    <lang-switcher class="floating-lang" />
    <div class="signup-card">
        <router-link to="/" class="brand"><img src="@/assets/logo.svg" :alt="$t('nav.logoAlt')" class="brand-logo" /></router-link>
        <h1 class="title">{{ $t('signup.title') }}</h1>

        <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" :aria-valuenow="progress"
            :aria-label="$t('signup.progressAria')">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <p class="step-label">{{ $t('signup.stepOf', { current: step, total: totalSteps }) }} · {{ stepTitle }}</p>

        <form @submit.prevent="onSubmit" novalidate>

        <div v-if="formError" class="form-error" role="alert">{{ formError }}</div>

        <div v-if="step === 1" class="field">
            <div class="role-options" role="radiogroup" :aria-label="$t('signup.role')">
                <button v-for="r in ['customer', 'seller']" :key="r" type="button" role="radio" :aria-checked="role === r"
                    :class="['role-card', { selected: role === r }]" @click="selectRole(r)">
                    <span class="role-name">{{ $t('signup.' + r) }}</span>
                    <span class="role-desc">{{ $t('signup.' + r + 'Desc') }}</span>
                </button>
            </div>
            <p v-if="errors.role" class="field-error" role="alert">{{ errors.role }}</p>
        </div>

        <template v-if="step === 2">
        <div class="name-row">
            <div class="field">
                <div class="row" :class="{ invalid: errors.first_name }">
                    <input type="text" :placeholder="$t('signup.firstName')" :aria-label="$t('signup.firstNameAria')" autocomplete="given-name"
                        v-model.trim="form.first_name" class="input" @input="clearError('first_name')"/>
                </div>
                <p v-if="errors.first_name" class="field-error" role="alert">{{ errors.first_name }}</p>
            </div>
            <div class="field">
                <div class="row" :class="{ invalid: errors.last_name }">
                    <input type="text" :placeholder="$t('signup.lastName')" :aria-label="$t('signup.lastNameAria')" autocomplete="family-name"
                        v-model.trim="form.last_name" class="input" @input="clearError('last_name')"/>
                </div>
                <p v-if="errors.last_name" class="field-error" role="alert">{{ errors.last_name }}</p>
            </div>
        </div>

        <div class="field">
            <div class="row" :class="{ invalid: errors.email }">
                <input type="email" :placeholder="$t('signup.email')" :aria-label="$t('signup.email')" autocomplete="email"
                    v-model.trim="form.email" class="input" @input="clearError('email')"/>
            </div>
            <p v-if="errors.email" class="field-error" role="alert">{{ errors.email }}</p>
        </div>

        <div v-if="role === 'seller'" class="field">
            <div class="row" :class="{ invalid: errors.store_name }">
                <input type="text" :placeholder="$t('signup.storeNamePlaceholder')" :aria-label="$t('signup.storeNameAria')"
                    v-model.trim="storeName" class="input" @input="clearError('store_name')"/>
            </div>
            <p v-if="errors.store_name" class="field-error" role="alert">{{ errors.store_name }}</p>
        </div>

        <div class="field">
            <div class="row" :class="{ invalid: errors.phone_number }">
                <input type="tel" :placeholder="$t('signup.phonePlaceholder')" :aria-label="$t('signup.phoneAria')" autocomplete="tel"
                    v-model.trim="form.phone_number" class="input" @input="clearError('phone_number')"/>
            </div>
            <p v-if="errors.phone_number" class="field-error" role="alert">{{ errors.phone_number }}</p>
        </div>

        <div class="field">
            <div class="row password" :class="{ invalid: errors.password }">
                <input :type="passwordVisible ? 'text' : 'password'" :placeholder="$t('signup.password')" :aria-label="$t('signup.password')"
                    autocomplete="new-password" v-model="form.password" class="input"
                    style="border: none; outline: none; box-shadow: none;" @input="clearError('password')"/>
                <button type="button" class="toggle-icon" :aria-label="passwordVisible ? $t('signup.hidePassword') : $t('signup.showPassword')"
                    @click="passwordVisible = !passwordVisible">
                    <Eye v-if="passwordVisible"/>
                    <EyeOff v-else/>
                </button>
            </div>
            <ul class="pw-rules" :aria-label="$t('signup.passwordRequirements')">
                <li v-for="rule in passwordRules" :key="rule.label" :class="['pw-rule', { met: rule.met }]">
                    <span class="pw-rule-icon" aria-hidden="true">{{ rule.met ? '✓' : '○' }}</span>
                    {{ rule.label }}
                    <span class="sr-only">{{ rule.met ? $t('signup.ruleMet') : $t('signup.ruleNotMet') }}</span>
                </li>
            </ul>
            <p v-if="errors.password" class="field-error" role="alert">{{ errors.password }}</p>
        </div>

        <div class="field">
            <div class="row password" :class="{ invalid: errors.confirm }">
                <input :type="ConfirmVisible ? 'text' : 'password'" :placeholder="$t('signup.confirmPassword')" :aria-label="$t('signup.confirmPasswordAria')"
                    autocomplete="new-password" v-model="confirmPassword" class="input"
                    style="border: none; outline: none; box-shadow: none;" @input="clearError('confirm')"/>
                <button type="button" class="toggle-icon" :aria-label="ConfirmVisible ? $t('signup.hidePassword') : $t('signup.showPassword')"
                    @click="ConfirmVisible = !ConfirmVisible">
                    <Eye v-if="ConfirmVisible"/>
                    <EyeOff v-else/>
                </button>
            </div>
            <p v-if="errors.confirm" class="field-error" role="alert">{{ errors.confirm }}</p>
        </div>

        </template>

        <div v-if="step === 3" class="image-container">
        <div class="avatar-picker" role="button" tabindex="0" :aria-label="$t('signup.uploadImage')"
            @click="triggerImageUpload" @keyup.enter="triggerImageUpload">
            <div class="profile-circle">
                <img v-if="form.profile_image" :src="form.profile_image" :alt="$t('signup.profileAlt')" class="profile-img"/>
                <svg v-else class="avatar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                    <circle cx="12" cy="8" r="3.5"/>
                    <path d="M5 20c0-3.6 3.1-6 7-6s7 2.4 7 6" stroke-linecap="round"/>
                </svg>
            </div>
            <span class="camera-badge" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 4 7.5 6H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-2.5L15 4H9zm3 4.5a4 4 0 1 1 0 8 4 4 0 0 1 0-8zm0 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/></svg>
            </span>
        </div>
        <input type="file" accept="image/*" ref="fileInput" @change="handleImageChange" hidden />
        <p class="field-hint">{{ $t('signup.imageHint') }}</p>
        <template v-if="role === 'seller'">
            <div class="avatar-picker store-logo" role="button" tabindex="0" :aria-label="$t('signup.uploadStoreImage')"
                @click="$refs.storeInput.click()" @keyup.enter="$refs.storeInput.click()">
                <div class="profile-circle">
                    <img v-if="form.store_image" :src="form.store_image" :alt="$t('signup.storeAlt')" class="profile-img"/>
                    <svg v-else class="avatar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                        <path d="M4 9.5 5.5 4h13L20 9.5M4 9.5h16M4 9.5V20h16V9.5M9 20v-5h6v5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <span class="camera-badge" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 4 7.5 6H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-2.5L15 4H9zm3 4.5a4 4 0 1 1 0 8 4 4 0 0 1 0-8zm0 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/></svg>
                </span>
            </div>
            <input type="file" accept="image/*" ref="storeInput" @change="handleStoreImageChange" hidden />
            <p class="field-hint">{{ $t('signup.storeImageHint') }}</p>
        </template>
        </div>

        <div class="actions">
            <button v-if="step > 1" type="button" class="btn back-btn" :disabled="loading" @click="back">
                {{ $t('signup.back') }}
            </button>
            <button v-if="step < totalSteps" type="button" class="btn btn-primary submit-btn" @click="next">
                {{ $t('signup.next') }}
            </button>
            <button v-else type="submit" class="btn btn-primary submit-btn" :disabled="loading">
                <span v-if="loading" class="spinner" aria-hidden="true"></span>
                {{ loading ? $t('signup.creating') : $t('signup.submit') }}
            </button>
        </div>
        <footer class="footer">{{ $t('signup.haveAccount') }}
            <router-link to="/login" class="link">{{ $t('signup.logIn') }}</router-link>
        </footer>

        </form>
    </div>
    </div>
</template>
<script>

import api from '@/services/api';
import { Eye, EyeOff } from '@lucide/vue';

export default {
    components: {EyeOff, Eye},
    data() {
    return {
        form: {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        phone_number: "",
        profile_image: null,
        store_image: null
        },
        storeName: "",
        role: "",
        step: 1,
        totalSteps: 3,
        confirmPassword: "",
        selectedFile: null,
        selectedStoreFile: null,
        passwordVisible: false,
        ConfirmVisible: false,
        errors: {},
        formError: '',
        loading: false
    };
    },
    computed: {
        progress() {
            return Math.round(((this.step - 1) / this.totalSteps) * 100)
        },
        stepTitle() {
            return this.$t('signup.steps.' + this.step)
        },
        passwordRules() {
            const p = this.form.password
            return [
                { label: this.$t('signup.rules.length'), met: p.length >= 8 },
                { label: this.$t('signup.rules.upper'), met: /[A-Z]/.test(p) },
                { label: this.$t('signup.rules.lower'), met: /[a-z]/.test(p) },
                { label: this.$t('signup.rules.number'), met: /[0-9]/.test(p) },
                { label: this.$t('signup.rules.special'), met: /[!@#$%^&*(),.?":{}|<>]/.test(p) },
            ]
        },
    },
    methods: {
        triggerImageUpload() {
            this.$refs.fileInput.click();
        },
        selectRole(r) {
            this.role = r
            this.clearError('role')
        },
        next() {
            if (this.validateStep(this.step)) {
                this.formError = ''
                this.step++
            }
        },
        back() {
            if (this.step > 1) {
                this.formError = ''
                this.step--
            }
        },
        onSubmit() {
            if (this.step < this.totalSteps) this.next()
            else this.submitForm()
        },
        clearError(field) {
            if (this.errors[field]) this.errors = { ...this.errors, [field]: '' }
            this.formError = ''
        },
        handleImageChange(event) {
        const file = event.target.files[0];
        if (!file) return;
        if (file.type.startsWith('image/')) {
            this.selectedFile = file;
            this.form.profile_image = URL.createObjectURL(file);
            this.formError = ''
        } else {
            this.formError = this.$t('signup.errors.invalidImage')
        }
    },
    handleStoreImageChange(event) {
        const file = event.target.files[0];
        if (!file) return;
        if (file.type.startsWith('image/')) {
            this.selectedStoreFile = file;
            this.form.store_image = URL.createObjectURL(file);
            this.formError = ''
        } else {
            this.formError = this.$t('signup.errors.invalidImage')
        }
    },

    validateStep(step) {
        const e = {}
        const f = this.form
        if (step === 1) {
            if (!this.role) e.role = this.$t('signup.errors.role')
        } else if (step === 2) {
            if (!f.first_name) e.first_name = this.$t('signup.errors.firstName')
            if (!f.last_name) e.last_name = this.$t('signup.errors.lastName')
            if (!f.email) e.email = this.$t('signup.errors.emailRequired')
            else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) e.email = this.$t('signup.errors.emailInvalid')
            if (this.role === 'seller' && !this.storeName) e.store_name = this.$t('signup.errors.storeName')
            if (!f.phone_number) e.phone_number = this.$t('signup.errors.phone')
            if (!f.password) e.password = this.$t('signup.errors.passwordRequired')
            else if (this.passwordRules.some(r => !r.met)) e.password = this.$t('signup.errors.passwordRules')
            if (!this.confirmPassword) e.confirm = this.$t('signup.errors.confirmRequired')
            else if (f.password !== this.confirmPassword) e.confirm = this.$t('signup.errors.mismatch')
        }
        this.errors = e
        if (Object.keys(e).length) this.formError = this.$t('signup.errors.fixFields')
        return Object.keys(e).length === 0
    },

    applyServerErrors(error) {
        if (!error.response) {
            this.formError = this.$t('signup.errors.network')
            return
        }
        const { status, data } = error.response
        if (status === 400 && data && typeof data === 'object') {
            const errs = {}
            for (const [key, val] of Object.entries(data)) {
                const msg = Array.isArray(val) ? val.join(' ') : String(val)
                if (key === 'detail' || key === 'non_field_errors') this.formError = msg
                else errs[key] = msg
            }
            this.errors = errs
            if (Object.keys(errs).some(k => k !== 'profile_image' && k !== 'store_image')) this.step = 2
            if (!this.formError) this.formError = this.$t('signup.errors.fixFields')
        } else if (status >= 500) {
            this.formError = this.$t('signup.errors.server')
        } else {
            this.formError = (data && data.detail) || this.$t('signup.errors.failed')
        }
    },

    async submitForm(){
        if (this.loading || !this.validateStep(1) || !this.validateStep(2)) return
        this.loading = true
        this.formError = ''
        try{
            const formData = new FormData();
            if (this.role === 'seller'){
                formData.append('store_name', this.storeName);
            }
            const url = '/signup/' + this.role + '/';
            formData.append('first_name', this.form.first_name);
            formData.append('last_name', this.form.last_name);
            formData.append('phone_number', this.form.phone_number);
            formData.append('email', this.form.email);
            formData.append('password', this.form.password);
            if (this.selectedFile) formData.append('profile_image', this.selectedFile);
            if (this.role === 'seller' && this.selectedStoreFile) formData.append('store_image', this.selectedStoreFile);
            await api.post(url, formData)
            this.$emit('saved', true);
            this.$router.push('/')
        }
        catch(error){
            this.applyServerErrors(error)
        }
        finally{
            this.loading = false
        }
    },
    }
};

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
  max-width: 480px;
  padding: 32px 32px 24px;
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
}
.brand { display: flex; justify-content: center; margin-bottom: 12px; }
.brand-logo { height: 56px; width: auto; }
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
.field { margin-bottom: 16px; flex: 1; min-width: 0; }
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
.pw-rules {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 8px 0 0;
  padding: 0;
}
.pw-rule {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-size: 0.8rem;
  transition: background var(--transition), color var(--transition), border-color var(--transition);
}
.pw-rule.met {
  background: var(--color-success-soft);
  border-color: var(--color-success);
  color: #14532D;
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}
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
.submit-btn {
  width: 100%;
  min-height: 44px;
  margin-top: 8px;
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
.image-container { display: flex; flex-direction: column; align-items: center; margin-bottom: 20px; }
.profile-circle {
  width: 120px;
  height: 120px;
  background: #e8f0fe;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: #1a73e8;
  border: 2px solid #d2e3fc;
  transition: border-color var(--transition);
}
.avatar-picker {
  position: relative;
  width: 120px;
  height: 120px;
  cursor: pointer;
  border-radius: 50%;
}
.avatar-picker:hover .profile-circle,
.avatar-picker:focus-visible .profile-circle { border-color: #1a73e8; }
.avatar-picker.store-logo { margin-top: 16px; border-radius: var(--radius-md); }
.avatar-picker.store-logo .profile-circle { border-radius: var(--radius-md); }
.avatar-icon { width: 60%; height: 60%; }
.camera-badge {
  position: absolute;
  right: 2px;
  bottom: 2px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #1a73e8;
  color: #fff;
  border: 2px solid #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.camera-badge svg { width: 16px; height: 16px; }
.profile-img { width: 100%; height: 100%; object-fit: cover; }
.name-row { display: flex; gap: 14px; }
.progress {
  height: 6px;
  border-radius: 999px;
  background: var(--color-border);
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 999px;
  transition: width 0.3s ease;
}
.step-label {
  margin: 8px 0 20px;
  font-size: 0.85rem;
  color: var(--color-text-muted);
}
.role-options { display: flex; gap: 14px; }
.role-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px;
  text-align: start;
  cursor: pointer;
  color: var(--color-text);
  background: var(--color-surface);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  transition: border-color var(--transition);
}
.role-card:hover { border-color: var(--color-text-muted); }
.role-card.selected { border-color: var(--color-primary); }
.role-name { font-weight: 700; font-size: 1.05rem; }
.role-desc { font-size: 0.85rem; color: var(--color-text-muted); }
.actions { display: flex; gap: 12px; margin-top: 8px; }
.actions .submit-btn { margin-top: 0; flex: 1; }
.back-btn { min-height: 44px; cursor: pointer; }
.image-container { flex-direction: column; align-items: center; }
@media (max-width: 480px) {
  .signup-card { padding: 24px 18px 20px; }
  .title { font-size: 1.5rem; }
  .name-row { flex-direction: column; gap: 0; }
  .role-options { flex-direction: column; }
}
</style>
