<template>
    <div class="container mt-5">
      <h2>Register</h2>
      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" class="form-control" v-model="form.username" required />
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
            <option value="Admin">Admin</option>
            <option value="Professional">Professional</option>
            <option value="Customer">Customer</option>
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
        console.log("Submitting form:", this.form);
        try {
          const response = await axios.post('http://localhost:5858/auth/register', this.form);
          console.log("API Response:", response?.data || "No Data");
          alert('Registration Successful! Please log in.');
          this.$router.push('/login');
        } catch (error) {
          console.error("Error:", error.response ? error.response.data : error.message);
          alert('Error: ' + (error.response ? error.response.data.message : "Server not reachable"));
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