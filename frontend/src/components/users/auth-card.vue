<template>
  <div class="auth-wrap">
    <div class="auth-card">
      <h1>{{ title }}</h1>
      <slot />
    </div>
  </div>
</template>

<script>
export default { name: 'AuthCard', props: { title: { type: String, required: true } } }
</script>

<style scoped>
.auth-wrap { display: block; width: 100%; height: auto; padding: 130px 16px 48px; box-sizing: border-box; }
.auth-card { width: 100%; max-width: 420px; margin: 0 auto; padding: 32px; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); color: var(--color-text); }
h1 { margin: 0 0 20px; font-size: 1.5rem; text-align: center; }
.auth-card :slotted(label) { display: block; margin: 0 0 6px; font-size: 0.875rem; font-weight: 600; }
.auth-card :slotted(input) { width: 100%; box-sizing: border-box; margin-bottom: 16px; }
.auth-card :slotted(.msg) { margin: 0 0 16px; }
.auth-card :slotted(.msg.error) { color: var(--color-error); }
.auth-card :slotted(.msg.ok) { color: #166534; }
.auth-card :slotted(.btn) { width: 100%; }
.auth-card :slotted(.links) { margin-top: 16px; text-align: center; font-size: 0.9rem; }
</style>
