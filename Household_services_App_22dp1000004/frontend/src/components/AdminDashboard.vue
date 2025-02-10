<template>
  <div class="container mt-5">
    <h2>Create a New Service</h2>
    <form @submit.prevent="createService">
      <div class="mb-3">
        <label class="form-label">Service Name</label>
        <input type="text" v-model="service.name" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Base Price</label>
        <input type="number" v-model="service.base_price" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea v-model="service.description" class="form-control" required></textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">Time Required (minutes)</label>
        <input type="number" v-model="service.time_required" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Create Service</button>
    </form>

    <p v-if="message" class="mt-3 alert alert-success">{{ message }}</p>
    <p v-if="errorMessage" class="mt-3 alert alert-danger">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return { 
      service: {
        name: '',
        base_price: '',
        description: '',
        time_required: 0
      },
      message: '',
      errorMessage: ''
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      this.$router.push('/login');
    },

    async createService() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://localhost:5858/admin/create_service', this.service, {
          headers: { Authorization: `Bearer ${token}` }
        });

        this.message = response.data.message;
        this.errorMessage = '';
        this.service = { name: '', base_price: '', description: '', time_required: 0 };
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'An error occurred';
        this.message = '';
      }
    }
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>