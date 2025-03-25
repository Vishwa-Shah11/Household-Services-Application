<template>
    <div class="container mt-5">
        <h2 class="text-center text-primary">{{ category }} Services</h2>
        <div v-if="services.length === 0" class="text-muted text-center">No services available.</div>
        <div class="row justify-content-center">
            <div v-for="service in services" :key="service.id" class="col-md-6 col-lg-4">
                <div class="card service-card shadow-sm my-3 p-3">
                    <h5 class="text-dark">{{ service.name }}</h5>
                    <p class="text-secondary">{{ service.description }}</p>
                    <p><strong>Price:</strong> <span class="text-success">{{ service.base_price }}</span></p>
                    <p><strong>Time Required:</strong> <span class="text-info">{{ service.time_required }} minutes</span></p>
                    <button @click="requestService(service.id)" class="btn btn-primary btn-block">Request Service</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

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
                const response = await axios.get(`http://127.0.0.1:5858/customer/services/${this.category}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                this.services = response.data.services || [];
            } catch (error) {
                console.error('Error fetching services:', error);
                this.services = [];
            }
        },
        async requestService(serviceId) {
            try {
                const token = localStorage.getItem('token');
                const professionalsResponse = await axios.get(`http://127.0.0.1:5858/customer/professionals/${serviceId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (professionalsResponse.data.length === 0) {
                    alert("No professionals available for this service.");
                    return;
                }
                this.$router.push({ name: "selectProfessional", query: { serviceId: serviceId } });
            } catch (error) {
                console.error('Error requesting service:', error);
                alert('Failed to request service. Please try again.');
            }
        }
    },
    mounted() {
        this.fetchServices();
    }
};
</script>

<style scoped>
.container {
    max-width: 900px;
    margin: auto;
}
.service-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    transition: transform 0.3s ease-in-out;
    background: #f9f9f9;
}
.service-card:hover {
    transform: scale(1.05);
}
.service-card h5 {
    color: #007bff;
}
.btn-primary {
    width: 100%;
    border-radius: 5px;
}
</style>
