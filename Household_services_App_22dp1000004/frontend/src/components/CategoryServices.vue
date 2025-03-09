<template>
    <div class="container mt-5">
        <h2>{{ category }} Services</h2>
        <div v-if="services.length === 0">No services available.</div>
        <!-- <p>{{ services.length }}</p> -->
        <div v-for="service in services" :key="service.id" class="card my-3 p-3">
            <h5>{{ service.name }}</h5>
            <p>{{ service.description }}</p>
            <p><strong>Price:</strong> {{ service.base_price }}</p>
            <p><strong>Time Required:</strong> {{ service.time_required }} minutes</p>
            <button @click="requestService(service.id)" class="btn btn-primary">Request Service</button>
        </div>

        <!-- <div v-if="showEditForm" class="card p-3 mt-4">
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
            serviceRequests: [],
            selectedRequest: null,
            showEditForm: false,
            category: this.$route.params.category,
        };
    },
    methods: {
        async fetchServices() {
            try {
                const token = localStorage.getItem('token');
                console.log("Fetching services for category:", this.category);
                const response = await axios.get(`http://127.0.0.1:5858/customer/services/${this.category}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                console.log("Response:", response.data);
                console.log("Services fetched successfully:", response.data.services);

                if (response.data && response.data.services) {
                    this.services = response.data.services;
                    console.log("Services fetched successfully:", this.services);
                } else {
                    this.services = [];
                    console.warn("No services found for this category.");
                }

            } catch (error) {
                console.error('Error fetching services:', error);
                this.services = [];
            }
        },
        async requestService(serviceId) {
            try {
                const token = localStorage.getItem('token');
                const userName = await getUserName();
                const response = await axios.post('http://127.0.0.1:5858/customer/service_request',
                    { service_id: serviceId, remarks: `${userName} requested this service` },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                alert(response.data.message);
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
        // editServiceRequest(request) {
        //     this.selectedRequest = { ...request };
        //     this.showEditForm = true;
        // },
        // async updateServiceRequest() {
        //     try {
        //         const token = localStorage.getItem('token');
        //         const response = await axios.put(`http://127.0.0.1:5858/customer/update_request/${this.selectedRequest.id}`,
        //             this.selectedRequest,
        //             { headers: { Authorization: `Bearer ${token}` } }
        //         );
        //         alert(response.data.message);
        //         this.fetchServiceRequests();
        //         this.showEditForm = false;
        //     } catch (error) {
        //         console.error('Error updating service request:', error);
        //         alert('Failed to update request. Please try again.');
        //     }
        // },
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