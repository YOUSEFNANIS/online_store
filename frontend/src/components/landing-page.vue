<template>
  <div class="page">

    <!-- NAVBAR -->
    <nav class="navbar">
      <div class="container navbar-container">

        <div class="navbar-left">
          <span class="logo">The Editorial Marketplace</span>

          <div class="nav-links">
            <a
              v-for="item in navItems"
              :key="item.title"
              :href="item.page"
              class="nav-link"
            >
              {{ item.title }}
            </a>
          </div>
        </div>

        <div class="navbar-right">
          <router-link class="btn-text" :to="'/login'">Log In</router-link>
          <router-link class="btn-primary" :to="'/signup'">Sign Up</router-link>
        </div>

      </div>
    </nav>

    <!-- HERO -->
    <header class="hero">
      <div class="container hero-container">

        <div class="hero-content">

          <h1 class="hero-title">
            MAKE A <br />
            <span class="hero-title italic">DEAL</span>
          </h1>

          <p class="hero-description">
            Discover products from local sellers in your area.
            A marketplace reimagined with editorial precision and high-trust standards.
          </p>

          <div class="hero-actions">
            <router-link :to="'/signup'" class="btn-primary large">Signup For Free </router-link>
            <router-link :to="'/products'" class="btn-secondary large">Browse Marketplace</router-link>
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
          <h2>Why shop local?</h2>
          <p>
            Our platform bridges the gap between digital convenience
            and local community heritage.
          </p>
        </div>

        <div class="features">
          <div
            v-for="feature in features"
            :key="feature.title"
            :class="feature"
          >
            <component :is="feature.comp" class="icons"></component>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>

      </div>
    </section>
    
    <section class="cta" id="take-actions">
      <div class="container cta-container">

        <div class="cta-text">
          <h2>Want To Start Your Business?</h2>
          <p>
            Join over 2,000 local artisans who have turned their passion
            into a thriving commercial presence.
          </p>
          <router-link :to="'/signup'" class="btn-primary large" style="width: fit-content; ">Become A Seller</router-link>
        </div>

        <div class="cta-image">
          <img src="https://picsum.photos/seed/partnership/800/600" />
        </div>

      </div>
    </section>
    <section class="section" id="who-we-are">
      <div class="container">

        <div class="cta-text">
          <h1 style="text-align: center; font-size: 3rem;">Who We Are</h1>
          <p>
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quas hic, cupiditate vel ipsa, reiciendis delectus aliquid repellendus quaerat au
          </p>
        </div>
      </div>
    </section>
    <!-- FOOTER -->
    <footer class="footer">
      <div class="container footer-grid">

        <div>
          <h4>Marketplace</h4>
          <ul>
            <li><a href="#">Sustainability</a></li>
            <li><a href="#">Merchant Terms</a></li>
            <li><a href="#">Privacy Policy</a></li>
          </ul>
        </div>

        <div>
          <h4>Company</h4>
          <ul>
            <li><a href="#">Careers</a></li>
            <li><a href="#">Support</a></li>
          </ul>
        </div>
        <div>
          <h3>Contact Us</h3>

          <div class="social-links" style="gap: 5px;">
              <a href="#" class="social facebook" target="_blank">
                  <img src="@/assets/facebook.svg" alt="Facebook" class="contact-icons"/> Facebook
              </a>

              <a href="#" class="social instagram" target="_blank">
                  <img src="@/assets/instagram.svg" alt="instagram" class="contact-icons"/> Instagram
              </a>

              <a href="#" class="social whatsapp" target="_blank">
                  <img src="@/assets/whats-app.svg" alt="whats app" class="contact-icons"/> WhatsApp
              </a>
          </div>
      </div>
        <div style="margin-right: 0;">
          <h4>Message Us</h4>
          <div style="display:inline-flex">
            <input placeholder="Email Address" class="email-placeholder"/>
            <button class="email-submit"> → </button>
          </div>
        </div>

      </div>
      <div class="footer-content">
        <div class="divider"></div>
        <p>© 2026 10FastFingers, Inc. All rights reserved.</p>
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
        
        {title: "Services",
        page: '#our-services'
      },
        {title: "Who We Are",
        page: '#who-we-are'
      },
      {title: "Join Us",
        page: '#take-actions'
      }
      ],
      features: [
        {
          title: "Trusted Sellers",
          description: "Every seller is verified for quality and reliability.",
          comp: Compass
        },
        {
          title: "Local Discovery",
          description: "Find unique products near your location.",
          comp: ArrowLeftRight
        },
        {
          title: "Fast Delivery",
          description: "No more long international shipping delays.",
          comp: ShoppingBasket
        }
      ]
    };
  }
};
</script>

<style scoped>

html {
  scroll-behavior: smooth;
}

.page {
  font-family: Georgia, 'Times New Roman', Times, serif, Arial, sans-serif;
  color: #0f172a;
  z-index: 11111;
  width: 100%;
  border-radius: 10px;
  font-weight: bold;
  background: #fbf8fe;
}

.container {
  max-width: 1200px;
  margin: auto;
  padding: 0 14px;
  
}

/* NAVBAR */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  background: white;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
}

.navbar-left {
  display: flex;
  gap: 40px;
  align-items: center;
}

.logo {
  font-size: 20px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: #2f5385;
  border-radius: 0;
  text-decoration: none;
}

.nav-link.active {
  color: #2563eb;
  border-bottom: 2px solid #2563eb;
}

/* RIGHT */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-box input {
  padding: 8px 12px;
    border: 1px solid #ddd;
}

/* BUTTONS */
.btn-primary {
  background: #003466FF;
  color: white;
  font-weight: bold;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}

.btn-secondary {
  background: #b5b4b4;
  padding: 10px 20px;
  font-weight: bold;
  border: none;
  color: #003466FF;
}

.btn-text {
  background: none;
  border: none;
  color: #2563eb;
  cursor: pointer;
}

.large {
  padding: 14px 28px;
}

/* HERO */
.hero {
  padding: 80px 40px;
  align-items: center;
  background-image: "https://picsum.photos/seed/retail/800/1000";
}

.hero-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: self-start;
}

.hero-title {
  margin-top: 20%;
  font-size: 64px;
  color: #003466FF;
}

.italic{
  color: #335F99;
  font-style: italic;
}
.hero-description {
  margin-top: 16px;
  color: #64748b;
}

.hero-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.hero-image img {
  width: 80%;
}

/* SECTION */
.section {
  padding: 40px 0;
  align-self: center;
  width: 100%;
  color: rgb(0, 47, 90);
  background: #F6F2F8;
}

.section-header h2 {
  font-size: 32px;
}
.icons{
  padding: 12px;
  background: rgb(0, 47, 90);
  color: white;
}
.features {
  display: flex;
  gap: 30px;
  margin-top: 40px;
}

.feature {
  max-width: 300px;
  align-items: center;
}

.cta-container {
  padding: 30px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 40px;
}

.cta-image img {
  width: 100%;
}

.cta-text{
  margin:10px;
  gap: 10px;
  display: grid;
  
}
.footer {
  width: 100%;
  border-radius: 0;
  color: rgb(255, 255, 255);
  background: rgb(0, 47, 90);
  padding: 60px 10px;
  gap:10px;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
}

.footer a {
  color: rgb(170, 170, 163);
  text-decoration: none;
}

.muted {
  color: #9b9ea2;
}

.email-placeholder {
  width: 70%;
  padding: 10px 40px 10px 10px; /* Padding-right creates space for the arrow */
  border: none;
  border-radius: 0px;
  border-bottom: 1px solid #7a8aa3; /* The thin grey line */
  background: white;
  outline: none;
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: #335F99; /* Navy blue color from your previous hex conversion */
}

.email-submit {
  width: 20%;
  border: none;
  border-radius: 3px;
  border: 1px solid #7a8aa3; /* The thin grey line */
  background: rgb(0, 47, 90);
  outline: none;
  cursor: pointer;
  font-size: 1rem;
  color: white; /* Navy blue color from your previous hex conversion */
}
.email-submit:hover {
  transform: translateY(-4px);
}
.email-placeholder:focus {
  border: 1px solid black;
}

.footer-content {
  width: 90%;
  margin: 0 auto;
}
.divider {
  width: 100%;
  border-top: 1px solid rgb(98, 98, 98);
  margin-bottom: 20px; /* space below line */
}
.footer p {
  color: #dfdfdf; 
  font-size: 11px;
  margin: 0;
}

.social-links {
    display: flex;
    flex-direction: column;
}

.footer li {
  padding:3px 0 ;
} 

.contact-icons{
  max-width: 20px; 
  align-self: end;
}
</style>