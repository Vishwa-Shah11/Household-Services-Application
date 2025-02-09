<template>
    <div class="container mt-5">
      <h2>Login</h2>
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label class="form-label">Email:</label>
          <input type="email" v-model="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password:</label>
          <input type="password" v-model="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
      
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: { 
      async loginUser() {
        try {
          const response = await axios.post('http://localhost:5858/auth/login', {
            email: this.email,
            password: this.password
          });
  
          localStorage.setItem('token', response.data.token);
          alert('Login Successful!');

          // Redirect based on role
          if (response.data.role === 'admin') this.$router.push('/admin');
          else if (response.data.role === 'professional') this.$router.push('/professional');
          else this.$router.push('/customer');
          
        } catch (error) {
          console.error("Error:", error.response ? error.response.data : error.message);
          alert('Error: ' + (error.response ? error.response.data.message : "Server not reachable"));
        }
      }
    }
  };
  </script>
  