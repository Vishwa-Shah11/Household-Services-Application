<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/">Home</router-link>
      <div class="navbar-nav">
        <router-link class="nav-link" to="/service/search" v-if="isAuthenticated">Search</router-link>
        <router-link class="nav-link" to="/summary" v-if="isAuthenticated">Summary</router-link>
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
    userRole() {
      const user = JSON.parse(localStorage.getItem('username')); // Assuming user role is stored
      return user ? user.role : null;
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('username'); // Remove user details
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
