<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/home" v-if="isAuthenticated">Home</router-link>
      <div class="navbar-nav">
        <router-link class="nav-link" to="/admin/dashboard" v-if="isAuthenticated && isAdmin">Dashboard</router-link>
        <router-link class="nav-link" to="/customer/dashboard" v-if="isAuthenticated && isCustomer">Dashboard</router-link>
        <router-link class="nav-link" to="/professional/dashboard" v-if="isAuthenticated && isProfessional">Dashboard</router-link>
        <router-link class="nav-link" to="/service/search" v-if="isAuthenticated && isCustomer">Search</router-link>
        <router-link class="nav-link" to="/admin/search-professionals" v-if="isAuthenticated && isAdmin">Search</router-link>
        <router-link class="nav-link" to="/admin/summary" v-if="isAuthenticated && isAdmin">Summary</router-link>
        <router-link class="nav-link" to="/professional/summary" v-if="isAuthenticated && isProfessional">Summary</router-link>
        <router-link class="nav-link" to="/customer/summary" v-if="isAuthenticated && isCustomer">Summary</router-link>
        <router-link class="nav-link" to="/admin/users" v-if="isAuthenticated && isAdmin">Manage Users</router-link>
        <button class="btn btn-danger ms-2" @click="confirmLogout" v-if="isAuthenticated">Logout</button>
      </div>
    </div>
  </nav>

  <router-view></router-view>
</template>

<script>
import { ref, watchEffect } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();

    // ✅ Make authentication state reactive
    const isAuthenticated = ref(localStorage.getItem("token") !== null);
    const userRole = ref(localStorage.getItem("role"));

    // ✅ Derived states for different user roles
    const isAdmin = ref(userRole.value === "Admin");
    const isCustomer = ref(userRole.value === "Customer");
    const isProfessional = ref(userRole.value === "Professional");

    // ✅ Watch for changes in localStorage and update the state
    watchEffect(() => {
      isAuthenticated.value = localStorage.getItem("token") !== null;
      userRole.value = localStorage.getItem("role");
      isAdmin.value = userRole.value === "Admin";
      isCustomer.value = userRole.value === "Customer";
      isProfessional.value = userRole.value === "Professional";
    });

    // ✅ Logout function
    const confirmLogout = () => {
      if (confirm("Are you sure you want to logout?")) {
        logout();
      }
    };

    const logout = () => {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      isAuthenticated.value = false;
      userRole.value = null;
      isAdmin.value = false;
      isCustomer.value = false;
      isProfessional.value = false;
      router.push("/login"); // Redirect to login
    };

    return {
      isAuthenticated,
      isAdmin,
      isCustomer,
      isProfessional,
      confirmLogout,
    };
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
