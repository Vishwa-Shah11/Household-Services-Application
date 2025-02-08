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
          alert('Login successful');
          this.$router.push('/dashboard');
        } catch (error) {
          alert('Invalid credentials');
        }
      }
    }
  };
  </script>
  