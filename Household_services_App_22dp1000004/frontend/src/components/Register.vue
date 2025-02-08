<template>
    <div class="container mt-5">
      <h2>Register</h2>
      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" class="form-control" v-model="form.name" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input type="email" class="form-control" v-model="form.email" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" v-model="form.password" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Role</label>
          <select class="form-control" v-model="form.role" required>
            <option value="admin">Admin</option>
            <option value="professional">Professional</option>
            <option value="customer">Customer</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        form: {
          name: '',
          email: '',
          password: '',
          role: '',
        },
      };
    },
    methods: {
      async registerUser() {
        try {
          const response = await axios.post('http://localhost:5000/api/register', this.form);
          alert('Registration Successful!');
          this.$router.push(`/${this.form.role}`);
        } catch (error) {
          alert('Registration Failed: ' + error.response.data.message);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 500px;
  }
  </style>
  