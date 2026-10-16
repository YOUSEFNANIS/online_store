<template>
  <div class="terms">
    <h1>{{ $t('terms.title') }}</h1>
    <p class="updated">{{ $t('terms.updated') }}</p>

    <section>
      <h2>{{ $t('terms.s1.title') }}</h2>
      <p>{{ $t('terms.s1.body') }}</p>
    </section>

    <section>
      <h2>{{ $t('terms.s2.title') }}</h2>
      <p>{{ $t('terms.s2.body') }}</p>
    </section>

    <section>
      <h2>{{ $t('terms.s3.title') }}</h2>
      <p>{{ $t('terms.s3.body') }}</p>
    </section>

    <section>
      <h2>{{ $t('terms.s4.title') }}</h2>
      <p>{{ $t('terms.s4.body') }}</p>
    </section>

    <section>
      <h2>{{ $t('terms.s5.title') }}</h2>
      <p>{{ $t('terms.s5.body') }}</p>
    </section>

    <section>
      <h2>{{ $t('terms.s6.title') }}</h2>
      <p>{{ $t('terms.s6.body') }}</p>
    </section>

    <section>
      <h2>{{ $t('terms.s7.title') }}</h2>
      <p>{{ $t('terms.s7.body') }}</p>
    </section>

    <router-link to="/" class="btn btn-primary">{{ $t('terms.backHome') }}</router-link>
  </div>
</template>

<style scoped>
.terms {
  max-width: 760px;
  margin: 0 auto;
  padding: 40px 16px;
  color: var(--color-text);
}
h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 4px;
}
.updated {
  color: var(--color-text-muted);
  margin-bottom: 28px;
}
section {
  margin-bottom: 22px;
}
h2 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 6px;
}
p {
  line-height: 1.6;
  color: var(--color-text-muted);
}
</style>
