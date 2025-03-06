<template>
  <div class="container mt-5">
    <h2><strong>Customer Dashboard</strong></h2>

    <h3>Available Services</h3>
    <div v-if="services.length === 0">No services available.</div>
    <div v-for="service in services" :key="service.id" class="card my-3 p-3">
      <h5>{{ service.name }}</h5>
      <p>{{ service.description }}</p>
      <p><strong>Price:</strong> {{ service.base_price }}</p>
      <p><strong>Time Required:</strong> {{ service.time_required }} minutes</p>
      <button @click="requestService(service.id)" class="btn btn-primary">Request Service</button>
    </div>

    <!-- List of Existing Service Requests -->
    <div class="card p-3 mt-4">
      <h5><Strong>Your Service Requests</Strong></h5>
      <ul v-if="serviceRequests.length > 0" class="list-group">
        <li v-for="request in serviceRequests" :key="request.id" class="list-group-item">
        <li v-for="service in services" :key="service.id" class="list-group-item">
          <strong>Service Name:</strong> {{ service.name }} <br />
          <strong>Allocated Date:</strong> {{ request.date_of_request }} <br />
          <strong>Status:</strong> {{ request.status }} <br />
          <!-- <strong>Remarks:</strong> {{ request.remarks }} <br /> -->
          <button @click="editServiceRequest(request)" class="btn btn-warning btn-sm mt-2">Edit</button><br>
          <!-- <button @click="showEditForm = true" class="btn btn-primary btn-sm mt-2">Edit Details</button><br> -->
          <button @click="closeServiceRequest(request.id)" class="btn btn-danger btn-sm mt-2">Close</button>
        </li>
        </li>
      </ul>
      <p v-else>No service requests found.</p>

      <!-- <div v-if="selectedRequest.id"> -->
      <!-- <div v-if="selectedRequest">
        <h4>Selected Service Request</h4>
        <p><strong>ID:</strong> {{ selectedRequest.id }}</p>
        <p><strong>Name:</strong> {{ selectedRequest.name }}</p>
        <p><strong>Status:</strong> {{ selectedRequest.service_status }}</p>
      </div> -->


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
      <div v-if="showEditForm" class="card p-3 mt-4">
        <h3>Edit Service Request</h3>

        <!-- Date Picker -->
        <label><strong>Request Date & Time:</strong></label>
        <input type="datetime-local" v-model="selectedRequest.date_of_request" class="form-control mb-2"
          @change="formatDateTime" />

        <!-- Service Status -->
        <label><strong>Service Status:</strong></label>
        <select v-model="selectedRequest.service_status" class="form-control mb-2">
          <option value="Requested">Requested</option>
          <option value="Assigned">Assigned</option>
          <option value="Closed">Closed</option>
        </select>

        <!-- Remarks -->
        <label><strong>Remarks:</strong></label>
        <textarea v-model="selectedRequest.remarks" class="form-control mb-2"></textarea>

        <button @click="updateServiceRequest" class="btn btn-success">Update</button>
        <button @click="showEditForm = false" class="btn btn-secondary">Cancel</button>
      </div>

    </div>
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
      selectedRequest: null, // Store selected request for editing
      showEditForm: false // Controls form visibility
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
        if (!token) {
          console.error("No token found. User might not be logged in.");
          return;
        }
        const response = await fetch('http://127.0.0.1:5858/customer/fetch_requests', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        // console.log("Fetched Service Requests:", data);
        this.serviceRequests = data || [];
      } catch (error) {
        console.error('Error fetching service requests:', error);
      }
    },

    // async editServiceRequest(requestId, updatedData) {
    //   try {
    //     console.log("Editing request ID:", requestId);
    //     const token = localStorage.getItem('token');
    //     console.log("token : ",token)
    //     if (!token) {
    //       alert('User is not authenticated');
    //       return;
    //     }
    //     console.log(await fetch(`http://127.0.0.1:5858/customer/fetch_requests/${requestId}`));

    //     const response = await fetch(`http://127.0.0.1:5858/customer/fetch_requests/${requestId}`, {
    //       method: 'PUT',
    //       headers: {
    //         'Content-Type': 'application/json',
    //         'Authorization': `Bearer ${token}`
    //       },
    //       body: JSON.stringify(updatedData)
    //     });

    //     if (!response.ok) {
    //       const errorData = await response.json();
    //       throw new Error(errorData.error || 'Failed to update service request');
    //     }

    //     const responseData = await response.json();
    //     alert(responseData.message);  // Show success message
    //     this.fetchServiceRequests();  // Refresh list after update

    //   } catch (error) {
    //     console.error('Error updating service request:', error);
    //     alert(error.message);
    //   }
    // },




    //     async editServiceRequest(requestId, updatedData) {
    //     try {
    //         const token = localStorage.getItem("token");

    //         console.log("Sending PUT request to:", `http://127.0.0.1:5858/customer/fetch_requests/${requestId}`);
    //         console.log("Request Data:", updatedData);

    //         const response = await fetch(
    //             `http://127.0.0.1:5858/customer/fetch_requests/${requestId}`,
    //             {
    //                 method: "PUT",
    //                 headers: {
    //                     "Content-Type": "application/json",
    //                     Authorization: `Bearer ${token}`,
    //                 },
    //                 body: JSON.stringify(updatedData), // Ensure data is correctly formatted
    //             }
    //         );

    //         if (!response.ok) {
    //             const errorData = await response.json();
    //             throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorData.error}`);
    //         }

    //         const result = await response.json();
    //         console.log("Response:", result);
    //         alert("Service request updated successfully!");
    //     } catch (error) {
    //         console.error("Error updating service request:", error);
    //         alert(`Failed to update service request: ${error.message}`);
    //     }
    // },

    // async editServiceRequest(requestId) {
    //   try {
    //     const token = localStorage.getItem('token');
    //     console.log("Sending PUT request to:", `http://127.0.0.1:5858/customer/fetch_requests/${requestId}`);

    //     const response = await fetch(
    //       `http://127.0.0.1:5858/customer/fetch_requests/${requestId}`,
    //       {
    //         method: 'PUT',
    //         headers: {
    //           'Authorization': `Bearer ${token}`,
    //           // Content-Type 'application/json',
    //           'accept': 'application/json',
    //         }
    //       }
    //     );
    //     console.log("Heetguijkmkl;,");
    //     if (!response.ok) {
    //       console.log("response.ok:", response.ok);
    //       const errorData = await response.json();
    //       throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorData.error}`);
    //     }
    //     console.log("Heet Shah:");
    //     const result = await response.json();
    //     console.log("Response:", result);
    //     alert("Service request updated successfully!");
    //   }
    //   catch (error) {
    //     console.error("Error updating service request:", error);
    //     alert(`Failed to update service request: ${error.message}`);
    //   }
    // },




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
    this.fetchServices();
    this.fetchServiceRequests();
  }
};
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>