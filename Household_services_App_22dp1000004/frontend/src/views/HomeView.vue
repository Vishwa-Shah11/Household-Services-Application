<template>
  <div class="home-container">
    <header class="hero">
      <h1>Welcome to Household Services</h1>
      <p>Your one-stop solution for all home service needs – Reliable, Affordable, and Fast!</p>
    </header>
    
    <section class="about">
      <h2>About Us</h2>
      <p>
        We are a trusted platform connecting customers with top-rated professionals for household services.
        From plumbing to cleaning, we bring convenience to your doorstep with just a few clicks.
      </p>
    </section>
    
    <section class="why-choose-us">
      <h2>Why Choose Us?</h2>
      <ul>
        <li><strong>Verified Professionals:</strong> Handpicked experts for reliable service.</li>
        <li><strong>Affordable Pricing:</strong> Transparent rates with no hidden charges.</li>
        <li><strong>Quick Service:</strong> Book and get services at your convenience.</li>
        <li><strong>24/7 Support:</strong> We’re here whenever you need us.</li>
      </ul>
    </section>
    
    <section class="cta">
      <h2>Get Started Today!</h2>
      <p>Sign up now and book your first service hassle-free.</p>
      <router-link to="/register" class="btn">Register Now</router-link>
      <router-link to="/login" class="btn login">Login</router-link>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home-container {
  text-align: center;
  padding: 20px;
}
.hero {
  background: #1d7388;
  color: white;
  padding: 40px 20px;
  border-radius: 8px;
}
.about, .why-choose-us, .cta {
  margin-top: 30px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 10px 0;
}
.btn {
  display: inline-block;
  margin: 10px;
  padding: 10px 20px;
  color: white;
  background: #28a745;
  border-radius: 5px;
  text-decoration: none;
}
.btn.login {
  background: #007bff;
}
</style>
