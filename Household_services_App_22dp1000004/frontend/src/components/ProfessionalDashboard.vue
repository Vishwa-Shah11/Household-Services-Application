<template>
  <div class="container mt-4">
    <h2 class="mb-3">Service Requests</h2>

    <!-- Profile Docs Upload Section -->
    <div class="card p-3 mb-4">
      <h4>Upload Profile Documents</h4>
      <form @submit.prevent="uploadProfileDocs" enctype="multipart/form-data">
        <div class="mb-3">
          <input type="file" class="form-control" @change="handleFileUpload" accept=".pdf,.doc,.docx,.jpg,.png"
            required />
        </div>
        <button type="submit" class="btn btn-primary">Upload</button>
      </form>
      <div v-if="uploadMessage" class="alert mt-2" :class="uploadSuccess ? 'alert-success' : 'alert-danger'">
        {{ uploadMessage }}
      </div>
    </div>


    <div v-if="loading" class="text-center">
      <span class="spinner-border text-primary"></span> Loading...
    </div>

    <div v-else-if="serviceRequests.length === 0" class="alert alert-warning">
      No service requests assigned yet.
    </div>

    <div v-else>
      <table class="table table-striped">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Customer Name</th>
            <th>Service Name</th>
            <th>Date of Request</th>
            <th>Status</th>
            <th>Remarks</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.customer_name }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.date_of_request }}</td>
            <td>
              <span class="badge" :class="statusClass(request.service_status)">
                {{ request.service_status }}
              </span>
            </td>
            <td>{{ request.remarks || 'N/A' }}</td>
            <td>
              <button v-if="request.service_status === 'Requested'" class="btn btn-success btn-sm me-2"
                @click="acceptRequest(request.id)">
                Accept
              </button>
              <button v-if="request.service_status === 'Requested'" class="btn btn-danger btn-sm me-2"
                @click="rejectRequest(request.id)">
                Reject
              </button>
              <button v-if="request.service_status === 'Assigned'" class="btn btn-primary btn-sm"
                @click="closeRequest(request.id)">
                Close Request
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      serviceRequests: [],
      loading: false,
      selectedFile: null,
      uploadMessage: "",
      uploadSuccess: false,
    };
  },
  methods: {
    async fetchServiceRequests() {
      this.loading = true;
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:5858/professional/service_requests", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const result = await response.json();
        if (response.ok) {
          this.serviceRequests = result.service_requests || [];
        } else if (response.status === 403) {
          this.serviceRequests = [];
          alert("Access denied. Your account is not approved yet.");
        }
        else {
          this.serviceRequests = [];
          alert(result.message || "Failed to fetch requests");
        }
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        this.loading = false;
      }
    },

    // Handle file selection
    handleFileUpload(event) {
      if (!event || !event.target || !event.target.files || event.target.files.length === 0) {
        console.error("No file selected");
        return;
      }
      this.selectedFile = event.target.files[0]; // Store the selected file
      console.log("Selected file:", this.selectedFile);
    },

    // Handle file upload
    async uploadProfileDocs(event) {
      if (!this.selectedFile) {
        alert("No file selected. Please select a file.");
        return;
      }
      const formData = new FormData();
      formData.append("profile_docs", this.selectedFile);
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:5858/professional/upload_docs", {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
          body: formData,
        });

        const result = await response.json();
        if (response.ok) {
          alert("File uploaded successfully!");
          this.uploadMessage = "File uploaded successfully!";
          this.uploadSuccess = true;
        } else {
          alert("Error uploading file: " + (result.error || "Unknown error"));
          this.uploadMessage = "Error uploading file: " + (result.error || "Unknown error");
          this.uploadSuccess = false;
        }
      } catch (error) {
        console.error("Error uploading file:", error);
        alert("Error uploading file: " + error.message);
        this.uploadMessage = "Error uploading file: " + error.message;
        this.uploadSuccess = false;
      }
    },

    async acceptRequest(requestId) {
      if (!confirm("Are you sure you want to accept this request?")) return;

      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5858/professional/service_requests/${requestId}/action`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ action: "Accepted" }),
        });

        const result = await response.json();
        if (response.ok) {
          alert("Service request Accepted successfully!");
          this.fetchServiceRequests();
        } else {
          alert(result.error || "Failed to accept request");
        }
      } catch (error) {
        console.error("Error accepting request:", error);
      }
    },

    async rejectRequest(requestId) {
      if (!confirm("Are you sure you want to reject this request?")) return;

      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5858/professional/service_requests/${requestId}/action`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ action: "Rejected" }),
        });

        const result = await response.json();
        if (response.ok) {
          alert("Service request Rejected successfully!");
          this.fetchServiceRequests();
        } else {
          alert(result.error || "Failed to reject request");
        }
      } catch (error) {
        console.error("Error rejecting request:", error);
      }
    },

    async closeRequest(requestId) {
      if (!confirm("Are you sure you want to close this request?")) return;

      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5858/professional/service_requests/${requestId}/close`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const result = await response.json();
        if (response.ok) {
          alert("Service request Closed successfully!");
          this.fetchServiceRequests();
        } else {
          alert(result.error || "Failed to close request");
        }
      } catch (error) {
        console.error("Error closing request:", error);
      }
    },

    statusClass(status) {
      return {
        "badge-success": status === "Assigned",
        "badge-danger": status === "Rejected",
        "badge-warning": status === "Requested",
        "badge-primary": status === "Closed",
      };
    },
  },
  mounted() {
    this.fetchServiceRequests();
  },
};
</script>

<style scoped>
.badge-success {
  background-color: green;
  color: white;
}

.badge-danger {
  background-color: red;
  color: white;
}

.badge-warning {
  background-color: orange;
  color: white;
}

.badge-primary {
  background-color: blue;
  color: white;
}
</style>
