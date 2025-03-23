<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/home" v-if="isAuthenticated">Home</router-link>
      <!-- <router-link class="navbar-brand" to="/home">Home</router-link> -->
      <div class="navbar-nav">
        <router-link class="nav-link" to="/admin/dashboard" v-if="isAuthenticated && isAdmin">Dashboard</router-link>
        <router-link class="nav-link" to="/customer/dashboard" v-if="isAuthenticated && isCustomer">Dashboard</router-link>
        <router-link class="nav-link" to="/professional/dashboard" v-if="isAuthenticated && isProfessional">Dashboard</router-link>
        <!-- <router-link class="nav-link" to="/service/search" v-if="isAuthenticated">Search</router-link> -->
        <router-link class="nav-link" to="/service/search" v-if="isAuthenticated && isCustomer">Search</router-link>
        <router-link class="nav-link" to="/admin/search-professionals" v-if="isAuthenticated && isAdmin">Search</router-link>
        <router-link class="nav-link" to="/admin/summary" v-if="isAuthenticated && isAdmin">Summary</router-link>
        <router-link class="nav-link" to="/professional/summary" v-if="isAuthenticated && isProfessional">Summary</router-link>
        <router-link class="nav-link" to="/customer/summary" v-if="isAuthenticated && isCustomer">Summary</router-link>
        <router-link class="nav-link" to="/admin/users" v-if="isAuthenticated && isAdmin">Manage Users</router-link>
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
    isProfessional() {
      return this.userRole === "Professional"; // ✅ Check if the user is a Professional
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
