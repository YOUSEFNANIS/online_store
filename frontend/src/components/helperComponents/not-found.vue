<template>
  <div class="container">
    <div class="error-code">404</div>
    <div class="title">{{ $t('notFound.title') }}</div>
    <div class="description">
    {{ $t('notFound.description') }}
    </div>
    <a href="/" class="btn btn-primary">{{ $t('notFound.home') }}</a>
  </div>

</template>

<style scoped>
.container {
  text-align: center;
  margin: auto;
  justify-content: center;
  align-items: center;
  display: flex;
  max-width: 500px;
  padding: 10%;
  flex-direction: column;
}
.error-code {
  font-size: 120px;
  font-weight: 700;
  line-height: 1.1;
  color: var(--color-text);
}
.title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--color-text);
}
.description {
  color: var(--color-text-muted);
  margin-bottom: 28px;
  line-height: 1.6;
}
@media (max-width: 600px) {
  .error-code { font-size: 80px; }
}
</style>
