<template>
  <div class="container">
    <h2>Admin Dashboard</h2>

    <!-- CREATE SERVICE BUTTON -->
    <button @click="showCreateModal = true" class="btn btn-primary">Create Service</button>

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
            <button @click="openUpdateModal(service)" class="btn btn-warning">Update</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- CREATE SERVICE MODAL -->
    <div v-if="showCreateModal" class="modal">
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
    <div v-if="showUpdateModal" class="modal">
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
      selectedService: {}, // Stores selected service details
      token: localStorage.getItem("token") // Store JWT token
    };
  },
  methods: {
    async fetchServices() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          throw new Error("User not authenticated.");
        }
        const response = await fetch("http://127.0.0.1:5858/admin/services", {
          method: "GET",
          headers: { 
            "Authorization": `Bearer ${token}`,
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
      try {
        const response = await fetch("/admin/create_service", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`
          },
          body: JSON.stringify(this.newService)
        });
        const data = await response.json();
        alert(data.message || data.error);
        if (response.ok) {
          this.showCreateModal = false;
          this.newService = { name: "", base_price: "", description: "" };
          await this.fetchServices();
        }
        
      } catch (error) {
        console.error("Error creating service:", error);
      }
    },
    openUpdateModal(service) {
      this.selectedService = { ...service }; // Copy service data
      this.showUpdateModal = true;
    },
    async updateService() {
      try {
        const response = await fetch(`/admin/update_service/${this.selectedService.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`
          },
          body: JSON.stringify(this.selectedService)
        });
        const data = await response.json();
        alert(data.message || data.error);
        this.showUpdateModal = false;
        this.fetchServices();
      } catch (error) {
        console.error("Error updating service:", error);
      }
    }
  },
  mounted() {
    this.fetchServices();
  }
};
</script>

<style>
/* Simple modal styling */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}
</style>
