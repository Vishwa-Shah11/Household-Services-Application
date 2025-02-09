<template>
    <div class="container mt-5">
      <h2>Admin Dashboard</h2>
      <p>Welcome, {{ userRole }}</p>
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return { userRole: localStorage.getItem('role') || 'Unknown' };
    },
    methods: {
      logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        this.$router.push('/login');
      },
    },
  };
  </script>
  