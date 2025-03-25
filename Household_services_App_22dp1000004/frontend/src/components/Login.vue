<template>
  <div class="d-flex flex-column justify-content-center align-items-center vh-200">
    <h3 class="text-center text-primary fw-bold mb-4">Quique Care</h3>
    <div class="card shadow-lg p-4" style="width: 400px;">
      <h2 class="text-center text-primary mb-4">Login</h2>
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label class="form-label">Email:</label>
          <input type="email" v-model="email" class="form-control" placeholder="Enter your email" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password:</label>
          <input type="password" v-model="password" class="form-control" placeholder="Enter your password" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
        <div class="text-center mt-3">
          <small>New user? <router-link to="/register" class="text-decoration-none">Create Account</router-link></small>
        </div>
        <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
      </form>
    </div>
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

    if (response.data.token) {
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("role", response.data.role);
      localStorage.setItem("username", response.data.username);
    }

    if (response.data.role === 'Admin') {
      router.push('/admin/dashboard');
    } else if (response.data.role === 'Professional') {
      router.push('/professional/dashboard');
    } else {
      router.push('/customer/dashboard');
    }
  } catch (error) {
    console.error("Login failed:", error.response?.data || error);
    if (error.response?.status === 403) {
      alert("Your account is blocked. Please contact support.");
    } else {
      alert(error.response?.data?.error || "Invalid credentials");
    }
  }
};
</script>
