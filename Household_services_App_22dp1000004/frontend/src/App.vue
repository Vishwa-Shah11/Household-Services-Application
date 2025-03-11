<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/home" v-if="isAuthenticated">Home</router-link>
      <div class="navbar-nav">
        <router-link class="nav-link" to="/admin/dashboard" v-if="isAdmin">Dashboard</router-link>
        <router-link class="nav-link" to="/customer/dashboard" v-if="isCustomer">Dashboard</router-link>
        <router-link class="nav-link" to="/proffesional/dashboard" v-if="isProffesional">Dashboard</router-link>
        <router-link class="nav-link" to="/service/search" v-if="isAuthenticated">Search</router-link>
        <router-link class="nav-link" to="/summary" v-if="isAuthenticated">Summary</router-link>
        <router-link class="nav-link" to="/admin/users" v-if="isAdmin">Manage Users</router-link>
        <button class="btn btn-danger ms-2" @click="logout" v-if="isAuthenticated">Logout</button>
      </div>
    </div>
  </nav>

  <router-view></router-view>
</template>

<script>
// import { is } from "core-js/core/object";

export default {
  
  computed: {
    isAuthenticated() {
      return localStorage.getItem("token") !== null;
    },
    userRole() {
      return localStorage.getItem("role"); // ✅ Directly fetch role
    },
    isAdmin() {
      return this.userRole === "Admin"; // ✅ Check if the user is an Admin
    },
    isCustomer() {
      return this.userRole === "Customer"; // ✅ Check if the user is a Customer
    },
    isProffesional() {
      return this.userRole === "Proffesional"; // ✅ Check if the user is a Proffesional
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("role"); // ✅ Ensure role is cleared on logout
      this.$router.push("/login");
    },
  },
  mounted() {
    console.log("User Role:", this.userRole); // ✅ Debugging
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
