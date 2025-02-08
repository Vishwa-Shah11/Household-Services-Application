<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/">Home</router-link>
      <div class="navbar-nav">
        <router-link class="nav-link" to="/admin">Admin</router-link>
        <router-link class="nav-link" to="/professional">Professional</router-link>
        <router-link class="nav-link" to="/customer">Customer</router-link>
      </div>
    </div>
  </nav>
  <router-view></router-view>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.navbar {
  margin-bottom: 20px;
}
</style>
