<template>
  <div class="container">
    <h2>Admin Dashboard</h2>

    <!-- SERVICE LIST -->
    <h3>Services</h3>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Base Price</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in services" :key="service.id">
          <td>{{ service.id }}</td>
          <td>{{ service.name }}</td>
          <td>{{ service.base_price }}</td>
          <td>{{ service.description }}</td>
          <td>
            <button @click="editService(service)" class="btn btn-warning">Update</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- CREATE SERVICE BUTTON -->
    <button @click="showCreateModal = true" class="btn btn-primary">Create Service</button>

    <!-- CREATE SERVICE MODAL -->
    <!-- Modal Overlay -->
    <div v-if="showCreateModal" class="modal-overlay"></div>
    <div v-if="showCreateModal" class="custom-modal">
      <div class="modal-content">
        <h3>Create New Service</h3>
        <input v-model="newService.name" placeholder="Service Name" />
        <input v-model="newService.base_price" placeholder="Base Price" type="number" />
        <textarea v-model="newService.description" placeholder="Description"></textarea>
        <button @click="createService" class="btn btn-success">Submit</button>
        <button @click="showCreateModal = false" class="btn btn-danger">Close</button>
      </div>
    </div>

    <!-- UPDATE SERVICE MODAL -->
    <div v-if="showUpdateModal" class="custom-modal">
      <div class="modal-content">
        <h3>Update Service</h3>
        <input v-model="selectedService.name" placeholder="Service Name" />
        <input v-model="selectedService.base_price" placeholder="Base Price" type="number" />
        <textarea v-model="selectedService.description" placeholder="Description"></textarea>
        <button @click="updateService" class="btn btn-success">Submit</button>
        <button @click="showUpdateModal = false" class="btn btn-danger">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showCreateModal: false,
      showUpdateModal: false,
      newService: { name: "", base_price: "", description: "" },
      services: [], // Stores fetched services
      selectedService: { id: null, name: "", base_price: "", description: "" },
      token: localStorage.getItem("token") // Store JWT token
    };
  },
  methods: {
    async fetchServices() {
      try {
        if (!this.token) {
          throw new Error("User not authenticated.");
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
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },

    async createService() {
      console.log("Create service button clicked!");
      try {
        console.log("Sending request to create service...");

        const response = await fetch("http://127.0.0.1:5858/admin/create_service", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${this.token}`
          },
          body: JSON.stringify(this.newService)
        });

        console.log("Response received:", response);

        const data = await response.json();
        console.log("Response data:", data);

        alert(data.message || data.error);

        if (response.ok) {
          console.log("Service created successfully, closing modal...");
          this.showCreateModal = false;
          this.newService = { name: "", base_price: "", description: "" };
          await this.fetchServices();
        } else {
          console.error("Failed to create service:", data.error);
        }

      } catch (error) {
        console.error("Error creating service:", error);
      }
    },

    editService(service) {
      console.log("Edit service button clicked!", service);
      this.selectedService = { ...service }; // Copy service data
      this.showUpdateModal = true;
    },

    async updateService() {
      console.log("Update service button clicked!");
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
    }
  },

  mounted() {
    console.log("Vue Component Mounted");
    this.fetchServices();
  },

  created() {
    console.log("Vue Instance Created:", this);
  },

  watch: {
    showCreateModal(newVal) {
      console.log("showCreateModal changed:", newVal);
    }
  }

};
</script>

<style>
/* Simple modal styling */
.modal {
  display: block !important; /* Override Bootstrap's display: none */
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


/* Ensure modal is hidden by default and shown only when needed */
.modal.hidden {
  display: none;
}

/* Dark overlay effect */
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
</style>
