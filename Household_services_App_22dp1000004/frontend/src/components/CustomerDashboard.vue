<template>
  <div class="container mt-5">
    <h2><strong>Customer Dashboard</strong></h2>

    <h3>Service Categories</h3>
    <div class="row">
      <div v-for="category in categories" :key="category" class="col-md-4 mb-3">
        <div class="card p-3 text-center">
          <h5>{{ category }}</h5>
          <button @click="viewCategory(category)" class="btn btn-primary">View Services</button>
        </div>
      </div>
    </div>

    <button @click="toggleServiceRequests" class="btn btn-primary">
      {{ showServiceRequests ? "Hide" : "Your Service Requests" }}
    </button>

    <div v-if="showServiceRequests" class="card p-3 mt-4">
      <h5><strong>Your Service Requests</strong></h5>
      <ul v-if="serviceRequests.length > 0" class="list-group">
        <li v-for="request in serviceRequests" :key="request.id" class="list-group-item">
          <strong>Service Name:</strong> {{ request.service_name }} <br />
          <strong>Allocated Date:</strong> {{ request.date_of_request }} <br />
          <strong>Status:</strong> {{ request.service_status }} <br />
          <button @click="editServiceRequest(request)" class="btn btn-warning btn-sm mt-2">Edit</button>
          <button @click="closeServiceRequest(request.id)" class="btn btn-danger btn-sm mt-2">Close</button>
        </li>
      </ul>
      <p v-else>No service requests found.</p>
    </div>

    <div v-if="showEditForm" class="card p-3 mt-4">
      <h3>Edit Service Request</h3>
      <label><strong>Request Date & Time:</strong></label>
      <input type="datetime-local" v-model="selectedRequest.date_of_request" class="form-control mb-2" />
      <label><strong>Service Status:</strong></label>
      <select v-model="selectedRequest.service_status" class="form-control mb-2">
        <option value="Requested">Requested</option>
        <option value="Assigned">Assigned</option>
        <option value="Closed">Closed</option>
      </select>
      <label><strong>Remarks:</strong></label>
      <textarea v-model="selectedRequest.remarks" class="form-control mb-2"></textarea>
      <button @click="updateServiceRequest" class="btn btn-success">Update</button>
      <button @click="showEditForm = false" class="btn btn-secondary">Cancel</button>
    </div>

    <!-- Edit Form (Initially Hidden) -->
    <!-- <p>{{ showEditForm }}</p> -->
    <!-- <div v-if="showEditForm" class="card p-3 mt-4">
        <h3>Edit Service Request</h3>
        <input v-model="selectedRequest.date_of_request" placeholder="Status" class="form-control mb-2" />
        <input v-model="selectedRequest.service_status" placeholder="Status" class="form-control mb-2" />
        <textarea v-model="selectedRequest.remarks" placeholder="Remarks" class="form-control mb-2"></textarea>
        <button @click="updateServiceRequest" class="btn btn-success">Update</button>
        <button @click="showEditForm = false" class="btn btn-secondary">Cancel</button>
      </div> -->
    <!-- <div v-if="showEditForm" class="card p-3 mt-4">
        <h3>Edit Service Request</h3>

        <label><strong>Request Date & Time:</strong></label>
        <input type="datetime-local" v-model="selectedRequest.date_of_request" class="form-control mb-2"
          @change="formatDateTime" />

        <label><strong>Service Status:</strong></label>
        <select v-model="selectedRequest.service_status" class="form-control mb-2">
          <option value="Requested">Requested</option>
          <option value="Assigned">Assigned</option>
          <option value="Closed">Closed</option>
        </select> -->

    <!-- Remarks -->
    <!-- <label><strong>Remarks:</strong></label>
        <textarea v-model="selectedRequest.remarks" class="form-control mb-2"></textarea>

        <button @click="updateServiceRequest" class="btn btn-success">Update</button>
        <button @click="showEditForm = false" class="btn btn-secondary">Cancel</button>
      </div>

    </div> -->
  </div>
</template>

<script>
import axios from 'axios';
import { getUserName } from '@/router/utils.js';


export default {
  data() {
    return {
      services: [],
      newServiceId: "",
      remarks: "",
      serviceRequests: [],
      showServiceRequests: false,
      selectedRequest: null, // Store selected request for editing
      showEditForm: false, // Controls form visibility
      categories: [],
      // categories: ['Saloon & Spa', 'Cleaning', 'Plumbing', 'Electrical', 'Carpentry', 'Appliance Repair', 'Pest Control', 'Others']
    };
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await fetch("http://127.0.0.1:5858/customer/categories", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        const result = await response.json();
        this.categories = result;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },
    viewCategory(category) {
      this.$router.push(`/category/${category}`);
    },

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
        const userName = await getUserName(); // Get name from utility function

        const response = await axios.post('http://127.0.0.1:5858/customer/service_request',
          { service_id: serviceId, remarks: `${userName} requested this service` },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        console.log(response.data.message);
        alert(response.data.message); // Show success message
      } catch (error) {
        console.error('Error requesting service:', error);
        alert('Failed to request service. Please try again.');
      }
    },

    async fetchServiceRequests() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5858/customer/fetch_requests', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log("🛠️ API Response:", response.data.service_requests);
        this.serviceRequests = response.data.service_requests || [];
        console.log("✅ Updated serviceRequests:", this.serviceRequests);
      } catch (error) {
        console.error("❌ Error fetching service requests:", error);
      }
    },

    toggleServiceRequests() {
      this.showServiceRequests = !this.showServiceRequests;
      if (this.showServiceRequests) {
        this.fetchServiceRequests(); // Fetch data only when displaying
      }
    },

    editServiceRequest(request) {
      console.log("Editing Service Request:", request); // Debugging log
      // Store selected request data without opening the form
      this.selectedRequest = { ...request };  // Create a copy to avoid modifying original data
      // Log the stored data for debugging
      console.log("Stored Data:", this.selectedRequest);
      this.showEditForm = true; // Show the form
    },

    formatDateTime(event) {
      let dateObj = new Date(event.target.value);

      // Convert to DD-MM-YYYY format
      let day = String(dateObj.getDate()).padStart(2, '0');
      let month = String(dateObj.getMonth() + 1).padStart(2, '0'); // Months are 0-based
      let year = dateObj.getFullYear();

      // Convert to 12-hour format with AM/PM
      let hours = dateObj.getHours();
      let minutes = String(dateObj.getMinutes()).padStart(2, '0');
      let ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12 || 12; // Convert 0 to 12-hour format

      // Format: "10-03-2025 02:15 PM"
      let formattedDate = `${day}-${month}-${year} ${hours}:${minutes} ${ampm}`;
      console.log("Formatted Date:", formattedDate);
      this.selectedRequest.date_of_request = formattedDate;
    },

    async updateServiceRequest() {
      if (!this.selectedRequest) return;
      const token = localStorage.getItem("token"); // Get the JWT token from storage
      if (!token) {
        alert("You are not authenticated! Please log in again.");
        return;
      }
      try {
        const response = await fetch(`http://127.0.0.1:5858/customer/fetch_requests/${this.selectedRequest.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(this.selectedRequest)
        });

        const result = await response.json();
        console.log("Update Response:", response.ok, result);
        if (response.ok) {
          alert("Service Request Updated Successfully!");
          this.showEditForm = false;
          await this.fetchServiceRequests();
        } else {
          alert(result.error || "Failed to update request");
        }
      } catch (error) {
        console.error("Error updating service request:", error);
      }
    },

    async closeServiceRequest(requestId) {
      const token = localStorage.getItem("token"); // Get the JWT token from storage
      if (!token) {
        alert("You are not authenticated! Please log in again.");
        return;
      }
      const response = await fetch(`http://127.0.0.1:5858/customer/fetch_requests/${requestId}/close`, {
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
    this.fetchCategories();
    // this.fetchServices();
    // this.fetchServiceRequests();
  }
};
</script>

<style scoped>
.card {
  border: 1px solid #e6c0c0;
  border-radius: 8px;
}
</style>