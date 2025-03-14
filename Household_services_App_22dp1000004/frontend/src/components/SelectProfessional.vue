<template>
    <div class="container">
      <h2>Select a Professional</h2>
      <div v-if="professionals.length > 0">
        <div v-for="prof in professionals" :key="prof.id" class="professional-card">
          <p><strong>Name:</strong> {{ prof.name }}</p>
          <p><strong>Rating:</strong> ⭐ {{ prof.rating }}</p>
          <p><strong>Price:</strong> ₹{{ prof.base_price }}</p>
          <button @click="selectProfessional(prof.id)">Select</button>
        </div>
      </div>
      <p v-else>No professionals available.</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        professionals: [],
        serviceId: this.$route.query.serviceId,
      };
    },
    async mounted() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          `http://127.0.0.1:5858/customer/get_professionals/${this.serviceId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.professionals = response.data;
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    methods: {
      async selectProfessional(professionalId) {
        try {
          const token = localStorage.getItem("token");
          const response = await axios.post(
            "http://127.0.0.1:5858/customer/service_request",
            { service_id: this.serviceId, professional_id: professionalId, remarks: "Customer requested this service" },
            { headers: { Authorization: `Bearer ${token}` } }
          );
          alert(response.data.message);
          this.$router.push("/customer/dashboard");
        } catch (error) {
          console.error("Error creating service request:", error);
          alert("Failed to create service request.");
        }
      },
    },
  };
  </script>
  
  <style>
  .professional-card {
    border: 1px solid #ddd;
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
  }
  </style>
  