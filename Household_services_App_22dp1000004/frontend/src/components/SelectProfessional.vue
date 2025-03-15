<template>
  <div class="container">
    <h2 class="text-center my-4">Select a Professional</h2>
    
    <div v-if="professionals.length > 0" class="row justify-content-center">
      <div v-for="prof in professionals" :key="prof.id" class="col-md-6 col-lg-4">
        <div class="professional-card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ prof.username }}</h5>
            <p class="card-text"><strong>Rating:</strong><span v-html="'⭐'.repeat(prof.rating)"></span></p>
            <p class="card-text"><strong>Price:</strong> ₹{{ prof.base_price }}</p>
            <button @click="selectProfessional(prof.id)" class="btn btn-primary w-100">
              Select
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <p v-else class="text-center text-muted">No professionals available.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      professionals: [],
      serviceId: null,
    };
  },
  async mounted() {
    this.serviceId = this.$route.query.serviceId;
    console.log("🛠 Received serviceId in SelectProfessional.vue:", this.serviceId);

    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(
        `http://127.0.0.1:5858/customer/professionals/${this.serviceId}`,
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
        const response = await axios.post(`http://127.0.0.1:5858/customer/select-professional/${this.serviceId}`,
          { 
            service_id: this.serviceId, 
            professional_id: professionalId, 
            remarks: "Customer requested this service" 
          },
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

<style scoped>
/* Styling for Professional Cards */
.professional-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  transition: transform 0.2s, box-shadow 0.2s;
}

.professional-card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
}

/* Card Title */
.card-title {
  font-weight: 600;
  color: #333;
}

/* Button Styling */
.btn-primary {
  background-color: #007bff;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  transition: background 0.2s, transform 0.1s;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

</style>
