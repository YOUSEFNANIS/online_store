<template>
  <div class="page">
    <lang-switcher class="floating-lang" />

    <!-- NAVBAR -->
    <nav class="navbar">
      <div class="container navbar-container">

        <div class="navbar-left">
          <span class="logo">{{ $t('landing.brand') }}</span>

          <div class="nav-links">
            <a
              v-for="item in navItems"
              :key="item.title"
              :href="item.page"
              class="nav-link"
            >
              {{ $t(item.title) }}
            </a>
          </div>
        </div>

        <div class="navbar-right">
          <router-link class="btn btn-outline" :to="'/login'">{{ $t('landing.nav.login') }}</router-link>
          <router-link class="btn btn-primary" :to="'/signup'">{{ $t('landing.nav.signup') }}</router-link>
        </div>

      </div>
    </nav>

    <!-- HERO -->
    <header class="hero">
      <div class="container hero-container">

        <div class="hero-content">

          <h1 class="hero-title">
            {{ $t('landing.hero.titleLine1') }} <br />
            <span class="hero-title italic">{{ $t('landing.hero.titleLine2') }}</span>
          </h1>

          <p class="hero-description">
            {{ $t('landing.hero.description') }}
          </p>

          <div class="hero-actions">
            <router-link :to="'/signup'" class="btn btn-primary large">{{ $t('landing.hero.signupFree') }}</router-link>
            <router-link :to="'/products'" class="btn btn-outline large">{{ $t('landing.hero.browse') }}</router-link>
          </div>
        </div>

        <div class="hero-image">
          <img src="https://picsum.photos/seed/retail/800/1000" />
        </div>

      </div>
    </header>

    <!-- FEATURES -->
    <section class="section" id="our-services">
      <div class="container">

        <div class="section-header">
          <h2>{{ $t('landing.why.title') }}</h2>
          <p>
            {{ $t('landing.why.subtitle') }}
          </p>
        </div>

        <div class="features">
          <div
            v-for="feature in features"
            :key="feature.title"
            :class="feature"
          >
            <component :is="feature.comp" class="icons"></component>
            <h3>{{ $t(feature.title) }}</h3>
            <p>{{ $t(feature.description) }}</p>
          </div>
        </div>

      </div>
    </section>
    
    <section class="cta" id="take-actions">
      <div class="container cta-container">

        <div class="cta-text">
          <h2>{{ $t('landing.cta.title') }}</h2>
          <p>
            {{ $t('landing.cta.text', { count: '2,000' }) }}
          </p>
          <router-link :to="'/signup'" class="btn btn-primary large" style="width: fit-content; ">{{ $t('landing.cta.button') }}</router-link>
        </div>

        <div class="cta-image">
          <img src="https://picsum.photos/seed/partnership/800/600" />
        </div>

      </div>
    </section>
    <section class="section" id="who-we-are">
      <div class="container">

        <div class="cta-text">
          <h1 style="text-align: center; font-size: 3rem;">{{ $t('landing.about.title') }}</h1>
          <p>
            {{ $t('landing.about.text') }}
          </p>
        </div>
      </div>
    </section>
    <!-- FOOTER -->
    <footer class="footer">
      <div class="container footer-grid">

        <div>
          <h4>{{ $t('landing.footer.marketplace') }}</h4>
          <ul>
            <li><a href="#">{{ $t('landing.footer.sustainability') }}</a></li>
            <li><a href="#">{{ $t('landing.footer.merchantTerms') }}</a></li>
            <li><a href="#">{{ $t('landing.footer.privacy') }}</a></li>
          </ul>
        </div>

        <div>
          <h4>{{ $t('landing.footer.company') }}</h4>
          <ul>
            <li><a href="#">{{ $t('landing.footer.careers') }}</a></li>
            <li><a href="#">{{ $t('landing.footer.support') }}</a></li>
          </ul>
        </div>
        <div>
          <h3>{{ $t('landing.footer.contactUs') }}</h3>

          <div class="social-links" style="gap: 5px;">
              <a href="#" class="social facebook" target="_blank">
                  <img src="@/assets/facebook.svg" alt="Facebook" class="contact-icons"/> {{ $t('landing.footer.facebook') }}
              </a>

              <a href="#" class="social instagram" target="_blank">
                  <img src="@/assets/instagram.svg" alt="Instagram" class="contact-icons"/> {{ $t('landing.footer.instagram') }}
              </a>

              <a href="#" class="social whatsapp" target="_blank">
                  <img src="@/assets/whats-app.svg" alt="WhatsApp" class="contact-icons"/> {{ $t('landing.footer.whatsapp') }}
              </a>
          </div>
      </div>
        <div>
          <h4>{{ $t('landing.footer.messageUs') }}</h4>
          <div style="display:inline-flex">
            <input :placeholder="$t('landing.footer.emailPlaceholder')" :aria-label="$t('landing.footer.emailPlaceholder')" class="email-placeholder"/>
            <button class="email-submit" :aria-label="$t('landing.footer.send')"><span class="arrow">→</span></button>
          </div>
        </div>

      </div>
      <div class="footer-content">
        <div class="divider"></div>
        <p>{{ $t('landing.footer.copyright') }}</p>
      </div>
    </footer>

  </div>
</template>

<script>
import LogIn from '@/signup/log-in.vue';
import { Compass, ArrowLeftRight, ShoppingBasket } from '@lucide/vue';
export default {
  components: {Compass, ArrowLeftRight, ShoppingBasket},
  name: "MarketplaceLanding",
  data() {
    return {
      navItems: [
        
        {title: "landing.nav.services",
        page: '#our-services'
      },
        {title: "landing.nav.whoWeAre",
        page: '#who-we-are'
      },
      {title: "landing.nav.joinUs",
        page: '#take-actions'
      }
      ],
      features: [
        {
          title: "landing.features.trusted.title",
          description: "landing.features.trusted.description",
          comp: Compass
        },
        {
          title: "landing.features.local.title",
          description: "landing.features.local.description",
          comp: ArrowLeftRight
        },
        {
          title: "landing.features.fast.title",
          description: "landing.features.fast.description",
          comp: ShoppingBasket
        }
      ]
    };
  }
};
</script>

<style scoped>
html { scroll-behavior: smooth; }

.page {
  color: var(--color-text);
  width: 100%;
  background: var(--color-bg);
}
.container { max-width: 1200px; margin: auto; padding: 0 16px; }

/* NAVBAR */
.navbar {
  position: fixed; top: 0; width: 100%; z-index: 10;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}
.navbar-container { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; gap: 16px; flex-wrap: wrap; }
.navbar-left { display: flex; gap: 32px; align-items: center; flex-wrap: wrap; }
.logo { font-size: 1.25rem; font-weight: 700; color: var(--color-text); }
.nav-links { display: flex; gap: 8px; }
.nav-link {
  display: inline-flex; align-items: center; min-height: 40px; padding: 0 10px;
  color: var(--color-text); font-weight: 500; text-decoration: none;
  border-radius: var(--radius-sm); transition: color var(--transition), background var(--transition);
}
.nav-link:hover { color: var(--color-primary); background: var(--color-primary-soft); }
.navbar-right { display: flex; align-items: center; gap: 12px; }

/* HERO */
.hero { padding: 96px 24px 64px; }
.hero-container { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center; }
.hero-title { margin: 0; font-size: 3.5rem; line-height: 1.1; font-weight: 800; color: var(--color-text); }
.italic { color: var(--color-primary); font-style: normal; }
.hero-description { margin-top: 16px; color: var(--color-text-muted); font-size: 1.125rem; max-width: 520px; }
.hero-actions { margin-top: 24px; display: flex; gap: 12px; flex-wrap: wrap; }
.large { min-height: 48px; padding: 0.75rem 1.5rem; font-size: 1rem; }
.hero-image img { width: 100%; max-width: 480px; border-radius: var(--radius-lg); display: block; }

/* SECTION */
.section { padding: 48px 0; width: 100%; background: var(--color-surface); color: var(--color-text); }
.section-header h2 { font-size: 2rem; margin: 0 0 8px; }
.section-header p { color: var(--color-text-muted); margin: 0; }
.icons {
  padding: 10px; width: 48px; height: 48px; box-sizing: border-box;
  background: var(--color-primary-soft); color: var(--color-primary);
  border-radius: var(--radius-md);
}
.features { display: flex; gap: 24px; margin-top: 32px; flex-wrap: wrap; }
.feature {
  flex: 1 1 240px; max-width: 320px; padding: 20px;
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius-md); box-shadow: var(--shadow-sm);
}
.feature h3 { margin: 12px 0 4px; }
.feature p { margin: 0; color: var(--color-text-muted); }

.cta { background: var(--color-bg); }
.cta-container { padding: 40px 16px; display: grid; grid-template-columns: 1fr 1fr; align-items: center; gap: 40px; }
.cta-image img { width: 100%; border-radius: var(--radius-lg); display: block; }
.cta-text { margin: 10px; gap: 12px; display: grid; }
.cta-text h2 { margin: 0; }
.cta-text p { margin: 0; color: var(--color-text-muted); }

/* FOOTER */
.footer { width: 100%; color: #fff; background: var(--color-nav); padding: 48px 16px 24px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 32px; }
.footer h3, .footer h4 { margin: 0 0 12px; color: #fff; }
.footer ul { list-style: none; padding: 0; margin: 0; }
.footer a {
  display: inline-flex; align-items: center; gap: 6px; min-height: 32px;
  color: #D1D5DB; text-decoration: none; transition: color var(--transition);
}
.footer a:hover { color: #fff; text-decoration: underline; }
.footer li { padding: 2px 0; }

.email-placeholder {
  width: 70%; min-height: 40px; padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-start-start-radius: var(--radius-sm); border-end-start-radius: var(--radius-sm);
  border-start-end-radius: 0; border-end-end-radius: 0;
  background: var(--color-surface); color: var(--color-text); font-size: 1rem;
}
.email-submit {
  width: 20%; min-width: 44px; min-height: 40px;
  border: 1px solid var(--color-primary);
  border-start-end-radius: var(--radius-sm); border-end-end-radius: var(--radius-sm);
  border-start-start-radius: 0; border-end-start-radius: 0;
  background: var(--color-primary); color: #fff; font-size: 1rem;
  transition: background var(--transition);
}
[dir="rtl"] .arrow { display: inline-block; transform: scaleX(-1); }
.email-submit:hover { background: var(--color-primary-hover); }

.footer-content { width: 100%; max-width: 1200px; margin: 32px auto 0; }
.divider { width: 100%; border-top: 1px solid #374151; margin-bottom: 16px; }
.footer p { color: #D1D5DB; font-size: 0.8rem; margin: 0; }

.social-links { display: flex; flex-direction: column; }
.contact-icons { max-width: 20px; }

@media (max-width: 800px) {
  .hero-container, .cta-container { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: 1fr 1fr; }
  .hero-title { font-size: 2.5rem; }
  .nav-links { display: none; }
}
</style>
