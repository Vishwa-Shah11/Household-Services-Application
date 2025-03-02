<template>
  <div class="container mt-5">
    <h2><strong>Customer Dashboard</strong></h2>

    <h3>Available Services</h3>
    <!-- <div v-if="services.length === 0">No services available.</div> -->
    <div v-for="service in services" :key="service.id" class="card my-3 p-3">
      <h5>{{ service.name }}</h5>
      <p>{{ service.description }}</p>
      <p><strong>Price:</strong> {{ service.base_price }}</p>
      <p><strong>Time Required:</strong> {{ service.time_required }} minutes</p>
      <button @click="requestService(service.id)" class="btn btn-primary">Request Service</button>
    </div>

    <!-- Create Service Request Form -->
    <!-- <div class="card p-3 mt-4">
      <h5>Create a Service Request</h5>
      <input v-model="newServiceId" type="number" placeholder="Service ID" class="form-control mb-2" />
      <textarea v-model="remarks" placeholder="Remarks" class="form-control mb-2"></textarea>
      <button @click="createServiceRequest" class="btn btn-success">Create Request</button>
    </div> -->

    <!-- List of Existing Service Requests -->
    <div class="card p-3 mt-4">
      <h5>Your Service Requests</h5>
      <ul v-if="serviceRequests.length > 0" class="list-group">
        <li v-for="request in serviceRequests" :key="request.id" class="list-group-item">
          <strong>Service ID:</strong> {{ request.service_id }} <br />
          <strong>Status:</strong> {{ request.service_status }} <br />
          <strong>Remarks:</strong> {{ request.remarks }} <br />
          <button @click="editServiceRequest(request.id)" class="btn btn-warning btn-sm mt-2">Edit</button>
          <button @click="closeServiceRequest(request.id)" class="btn btn-danger btn-sm mt-2">Close</button>
        </li>
      </ul>
      <p v-else>No service requests found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      services: [],
      newServiceId: "",
      remarks: "",
      serviceRequests: []
    };
  },
  methods: {
    async fetchServices() {
      try {
        const token = localStorage.getItem('token'); // Assuming you store JWT in localStorage
        const response = await axios.get('http://127.0.0.1:5858/customer/services', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.services = response.data.services;
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    async requestService(serviceId) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://127.0.0.1:5858/customer/service_request',
          { service_id: serviceId, remarks: 'Customer requested this service' },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert(response.data.message); // Show success message
      } catch (error) {
        console.error('Error requesting service:', error);
      }
    },
    // async createServiceRequest() {
    //   const response = await fetch("http://127.0.0.1:5858/customer/service_request", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //       "Authorization": `Bearer ${localStorage.getItem("token")}`
    //     },
    //     body: JSON.stringify({ service_id: this.newServiceId, remarks: this.remarks })
    //   });
    //   const data = await response.json();
    //   if (response.ok) {
    //     alert("Service request created!");
    //     this.fetchServiceRequests();
    //   } else {
    //     alert("Error: " + data.error);
    //   }
    // },
    // async fetchServiceRequests() {
    //   const response = await fetch("http://127.0.0.1:5858/customer/service_requests", {
    //     headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
    //   });
    //   const data = await response.json();
    //   this.serviceRequests = data.requests || [];
    // },
    async editServiceRequest(requestId) {
      // Logic to edit service request
    },
    async closeServiceRequest(requestId) {
      const response = await fetch(`http://127.0.0.1:5858/customer/service_request/${requestId}/close`, {
        method: "PUT",
        headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      if (response.ok) {
        alert("Service request closed!");
        this.fetchServiceRequests();
      }
    }
  },
  mounted() {
    this.fetchServices();
    // this.fetchServiceRequests();
  }
};
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>