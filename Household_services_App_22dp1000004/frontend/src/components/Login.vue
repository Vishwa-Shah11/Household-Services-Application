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
      <button type="submit" class="btn btn-primary">Login</button><br><br><br>
      New user?
      <router-link to="/register">Create Account</router-link>
      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
    </form>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const email = ref('');
const password = ref('');
const errorMessage = ref('');

const loginUser = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5858/auth/login', {
      email: email.value,
      password: password.value
    });

    // console.log("API Response:", response);

    if (response.data.token) {
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("role", response.data.role); // Stores correct role
      localStorage.setItem("username", response.data.username); // Stores correct username
    }
    // console.log("Stored username:", localStorage.getItem("username"));
    // console.log("Stored role:", localStorage.getItem("role"));

    // Redirect user based on role
    if (response.data.role === 'Admin') {
      router.push('/admin/dashboard');
    } else if (response.data.role === 'Professional') {
      router.push('/professional/dashboard');
    } else  {
      router.push('/customer/dashboard');
    }
  } catch (error) {
    // errorMessage.value = 'Invalid credentials';
    console.error("Login failed:", error.response?.data || error);
    alert(error.response?.data?.error || "Invalid credentials");
  }
};

</script>