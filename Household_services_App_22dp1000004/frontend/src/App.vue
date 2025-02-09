<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/">Home</router-link>
      <div class="navbar-nav">
        <router-link class="nav-link" to="/admin" v-if="isAuthenticated">Admin</router-link>
        <router-link class="nav-link" to="/professional" v-if="isAuthenticated">Professional</router-link>
        <router-link class="nav-link" to="/customer" v-if="isAuthenticated">Customer</router-link>
        <button class="btn btn-danger ms-2" @click="logout" v-if="isAuthenticated">Logout</button>
      </div>
    </div>
  </nav>
  <router-view></router-view>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return localStorage.getItem('token') !== null;
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    },
  },
};
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
