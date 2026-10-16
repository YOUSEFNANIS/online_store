<template>
  <div class="loader-container">
    <div class="spinner"></div>
    <p>{{ $t('loading.text') }}</p>
  </div>
</template>

<style scoped>
.loader-container {
  display: flex;
  margin: auto;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 5%;
  color: var(--color-text-muted);
}
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
