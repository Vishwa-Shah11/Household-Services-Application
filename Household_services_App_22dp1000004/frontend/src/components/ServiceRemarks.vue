<template>
  <div class="container mt-5">
    <h2 class="text-primary">Service Remarks</h2>
    <p>Request ID: <strong>{{ requestId }}</strong></p>

    <div class="form-group">
      <label>Service Name:</label>
      <input type="text" class="form-control" v-model="serviceDetails.name" disabled />
    </div>

    <div class="form-group">
      <label>Description:</label>
      <input type="text" class="form-control" v-model="serviceDetails.description" disabled />
    </div>

    <div class="form-group">
      <label>Professional Name:</label>
      <input type="text" class="form-control" v-model="serviceDetails.professionalName" disabled />
    </div>

    <div class="form-group">
      <label>Contact No:</label>
      <input type="text" class="form-control" v-model="serviceDetails.contact" disabled />
    </div>

    <!-- Rating -->
    <div class="form-group">
      <label>Service Rating:</label>
      <div>
        <span v-for="star in 5" :key="star" @click="setRating(star)" class="star">
          {{ star <= rating ? '⭐' : '☆' }} </span>
      </div>
    </div>

    <!-- Remarks -->
    <div class="form-group">
      <label>Remarks (if any):</label>
      <textarea class="form-control" v-model="remarks"></textarea>
    </div>

    <!-- Buttons -->
    <button class="btn btn-primary mt-3" @click="submitRemarks">Submit</button>
    <button class="btn btn-secondary mt-3" @click="goBack">Close</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      requestId: this.$route.params.requestId, // Get request ID from route
      serviceDetails: {},
      rating: 0,
      remarks: "",
    };
  },
  mounted() {
    this.fetchServiceDetails();
  },
  methods: {
    async fetchServiceDetails() {
      try {
        const response = await axios.get(`http://127.0.0.1:5858/customer/service_request/${this.requestId}`);
        this.serviceDetails = response.data;
      } catch (error) {
        console.error("Error fetching service details:", error);
      }
    },
    setRating(value) {
      this.rating = value;
    },
    async submitRemarks() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("You are not authenticated! Please log in again.");
        return;
      }
      if (this.rating === 0) {
        alert("Please provide a rating before submitting.");
        return;
      }
      try {
        const response = await axios.put(`http://127.0.0.1:5858/customer/fetch_requests/${this.requestId}/close`,
          {
            rating: this.rating,
            remarks: this.remarks,
          },
          {
            headers: {
              "Authorization": `Bearer ${token}`, // ✅ Ensure token is sent
              "Content-Type": "application/json", // ✅ Set content type
            },
          }
        );
        if (response.status === 200) {
          alert("Service request closed successfully!");
          this.$router.push("/customer/dashboard");
        }
      } catch (error) {
        console.error("Error closing service request:", error);
        alert("Failed to close service request.");
      }
    },
    goBack() {
      this.$router.push("/customer/dashboard");
    },
  },
};
</script>

<style scoped>
.star {
  font-size: 2rem;
  cursor: pointer;
  margin-right: 5px;
}
</style>