<template>
  <div class="loader-container">
    <div class="spinner"></div>
    <p>جاري التحميل...</p>
  </div>
</template>

<style scoped>
.loader-container {
  display: flex;
  margin: auto;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 5%;
}
.spinner {
  width: 100px;
  height: 100px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #000; /* Matches your black button theme */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>