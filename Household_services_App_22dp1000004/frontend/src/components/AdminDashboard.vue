<template>
  <div class="container">
    <h2>Admin Dashboard</h2>

    <!-- CREATE SERVICE BUTTON -->
    <button @click="showCreateModal = true" class="btn btn-primary">Create New Service</button> <br /> <br />

    <!-- SERVICE LIST -->
    <h3>Services</h3>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Category</th>
          <th>Base Price</th>
          <th>Description</th>
          <th>Time Required</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in services" :key="service.id">
          <td>{{ service.id }}</td>
          <td>{{ service.name }}</td>
          <td>{{ service.category }}</td>
          <td>{{ service.base_price }}</td>
          <td>{{ service.description }}</td>
          <td>{{ service.time_required }} minutes</td>
          <td>
            <button @click="editService(service)" class="btn btn-warning">Update</button>
            <button @click="deleteService(service.id)" class="btn btn-danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- CREATE SERVICE MODAL -->
<!-- Modal Overlay -->
<div v-if="showCreateModal" class="modal-overlay"></div>
<div v-if="showCreateModal" class="custom-modal">
  <div class="modal-content">
    <h3>Create New Service</h3>
    <input v-model="newService.name" placeholder="Service Name" />
    <input v-model="newService.category" placeholder="Category" />
    <input v-model="newService.base_price" placeholder="Base Price" type="number" />
    <textarea v-model="newService.description" placeholder="Description"></textarea>
    <input v-model="newService.time_required" placeholder="Time Required (minutes)" type="number" />
    <button @click="createService" class="btn btn-success">Submit</button>
    <button @click="showCreateModal = false" class="btn btn-danger">Close</button>
  </div>
</div>

    <!-- UPDATE SERVICE MODAL -->
    <div v-if="showUpdateModal" class="custom-modal">
      <div class="modal-content">
        <h3>Update Service</h3>
        <input v-model="selectedService.name" placeholder="Service Name" />
        <input v-model="selectedService.category" placeholder="Category" />
        <input v-model="selectedService.base_price" placeholder="Base Price" type="number" />
        <textarea v-model="selectedService.description" placeholder="Description"></textarea>
        <input v-model="selectedService.time_required" placeholder="Time Required" />
        <button @click="updateService" class="btn btn-success">Submit</button>
        <button @click="showUpdateModal = false" class="btn btn-danger">Close</button>
      </div>
    </div>

    <br><br>
    <!-- EXPORT CSV BATCHJOB -->
    <button @click="startExport" class="btn btn-secondary">Export Closed Service Requests</button>
    <p>{{ exportStatus }}</p>

  </div>
</template>

<script>
import { ref } from "vue";
export default {
  data() {
    return {
      showCreateModal: false,
      showUpdateModal: false,
      newService: { name: "", base_price: "", description: "" },
      services: [], // Stores fetched services
      selectedService: { id: null, name: "", base_price: "", description: "" },
      token: localStorage.getItem("token"), // Store JWT token
      message: "",
      exportStatus: ref("Status will appear here...")
    };
  },
  methods: {
    async fetchServices(retries = 3) {
      try {
        if (!this.token) {
          console.error("Token not found, retrying...");
          setTimeout(() => this.fetchServices(retries - 1), 2000); // Retry after 2 seconds
          return;
        }

        const response = await fetch("http://127.0.0.1:5858/admin/services", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${this.token}`,
            "Content-Type": "application/json"
          }
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API Error: ${errorText}`);
        }

        const data = await response.json();
        this.services = data.services;
        // console.log("Services fetched successfully:", this.services);
      } catch (error) {
        console.error("Error fetching services:", error);
        if (retries > 0) {
          setTimeout(() => this.fetchServices(retries - 1), 2000); // Retry after 2 seconds
        }
      }
    },


    async createService() {
      // console.log("Create service button clicked!");
      try {
        // console.log("Sending request to create service...");

        const response = await fetch("http://127.0.0.1:5858/admin/create_service", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${this.token}`
          },
          body: JSON.stringify(this.newService)
        });

        // console.log("Response received:", response);

        const data = await response.json();
        // console.log("Response data:", data);

        alert(data.message || data.error);

        if (response.ok) {
          // console.log("Service created successfully, closing modal...");
          this.showCreateModal = false;
          this.newService = { name: "", category: "", base_price: "", description: "" };
          await this.fetchServices();
        } else {
          console.error("Failed to create service:", data.error);
        }

      } catch (error) {
        console.error("Error creating service:", error);
      }
    },

    editService(service) {
      // console.log("Edit service button clicked!", service);
      this.selectedService = { ...service }; // Copy service data
      this.showUpdateModal = true;
    },

    async updateService() {
      // console.log("Update service button clicked!");
      try {
        if (!this.token) {
          throw new Error("User not authenticated.");
        }
        const response = await fetch(`http://127.0.0.1:5858/admin/update_service/${this.selectedService.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${this.token}`
          },
          body: JSON.stringify(this.selectedService)
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Failed to update Service.");
        }
        const data = await response.json();
        alert(data.message);
        this.showUpdateModal = false;
        this.fetchServices();
      } catch (error) {
        console.error("Error updating service:", error);
        alert(error.message);
      }
    },

    async deleteService(serviceId) {
      if (confirm("Are you sure you want to delete this service?")) {
        try {
          const response = await fetch(`http://127.0.0.1:5858/admin/delete_service/${serviceId}`, {
            method: "DELETE",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
          });

          if (response.ok) {
            alert("Service deleted successfully!");
            this.fetchServices(); // Refresh the services list
          } else {
            const errorData = await response.json();
            alert("Error: " + errorData.message);
          }
        } catch (error) {
          console.error("Error deleting service:", error);
        }
      }
    },

    async startExport() {
      const response = await fetch("http://127.0.0.1:5858/admin/export_closed_requests", { method: "POST" });
      const data = await response.json();

      if (data.task_id) {
        this.exportStatus = "Export job started...";
        await this.checkJobStatus(data.task_id);
      }
    },

    async checkJobStatus(taskId) {
      let status = "PENDING";

      while (status !== "SUCCESS" && status !== "FAILURE") {
        const response = await fetch(`http://127.0.0.1:5858/admin/task-status/${taskId}`);
        const result = await response.json();
        status = result.status;

        if (status === "SUCCESS") {
          this.exportStatus = "✅ Export job completed! 📧 Check your email.";
          break;
        } else if (status === "FAILURE") {
          this.exportStatus = "❌ Export failed. Please try again.";
          break;
        }

        await new Promise(resolve => setTimeout(resolve, 3000)); // Poll every 3 seconds
      }
    }


  },

  mounted() {
    console.log("Vue Component Mounted");
    // this.fetchServices();
  },

  created() {
    console.log("Vue Instance Created:", this);
    this.token = localStorage.getItem("token"); // Ensure token is fetched again
    this.fetchServices(); // Fetch services on page load
  },

  watch: {
    showCreateModal(newVal) {
      console.log("showCreateModal changed:", newVal);
    },
    showUpdateModal(newVal) {
      console.log("showUpdateModal changed:", newVal);
    }
  }

};
</script>

<style>
.modal {
  display: block !important;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  width: 50%;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1050;
}

.custom-modal {
  display: flex;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1050;
}

.modal.hidden {
  display: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}


.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.custom-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  width: 400px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  text-align: center;
}

.custom-modal h3 {
  font-size: 22px;
  margin-bottom: 15px;
  color: #1f2937;
  font-weight: bold;
}

.custom-modal input,
.custom-modal textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.custom-modal textarea {
  height: 80px;
  resize: none;
}

.custom-modal .btn {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.custom-modal .btn-success {
  background: #198754;
  color: white;
}

.custom-modal .btn-success:hover {
  background: #157347;
}

.custom-modal .btn-danger {
  background: #dc3545;
  color: white;
}

.custom-modal .btn-danger:hover {
  background: #bb2d3b;
}

</style>
