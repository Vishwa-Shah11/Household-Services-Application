<template>
  <div class="container mt-4">
    <h2 class="mb-3">Service Requests</h2>

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
            <th>Customer ID</th>
            <th>Service ID</th>
            <th>Date of Request</th>
            <th>Status</th>
            <th>Remarks</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.customer_id }}</td>
            <td>{{ request.service_id }}</td>
            <td>{{ request.date_of_request }}</td>
            <td>
              <span class="badge" :class="statusClass(request.service_status)">
                {{ request.service_status }}
              </span>
            </td>
            <td>{{ request.remarks || 'N/A' }}</td>
            <td>
              <button v-if="request.service_status === 'Requested'"
                class="btn btn-success btn-sm me-2" @click="acceptRequest(request.id)">
                Accept
              </button>
              <button v-if="request.service_status === 'Requested'"
                class="btn btn-danger btn-sm me-2" @click="rejectRequest(request.id)">
                Reject
              </button>
              <button v-if="request.service_status === 'Assigned'"
                class="btn btn-primary btn-sm" @click="closeRequest(request.id)">
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
      loading: false
    };
  },
  methods: {
    async fetchServiceRequests() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const response = await fetch("http://127.0.0.1:5858/professional/service_requests", {
          headers: { Authorization: `Bearer ${token}` }
        });

        const result = await response.json();
        if (response.ok) {
          this.serviceRequests = result;
        } else {
          alert(result.message || "Failed to fetch requests");
        }
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        this.loading = false;
      }
    },

    async acceptRequest(requestId) {
      if (!confirm("Are you sure you want to accept this request?")) return;

      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5858/professional/service_requests/${requestId}/action`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ action: "Accepted" })
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
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5858/professional/service_requests/${requestId}/action`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ action: "Rejected" })
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
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5858/professional/service_requests/${requestId}/close`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`
          }
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
        "badge-primary": status === "Closed"
      };
    }
  },
  mounted() {
    this.fetchServiceRequests();
  }
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
