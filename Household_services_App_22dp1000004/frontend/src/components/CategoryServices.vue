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
            <p>{{ service.id }}</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { getUserName } from '@/router/utils.js';
import router from '@/router/index.js';

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
        // async requestService(serviceId) {
        //     try {
        //         const token = localStorage.getItem('token');
        //         const userName = await getUserName();
        //         const response = await axios.post('http://127.0.0.1:5858/customer/service_request',
        //             { service_id: serviceId, remarks: `${userName} requested this service` },
        //             { headers: { Authorization: `Bearer ${token}` } }
        //         );
        //         alert(response.data.message);
        //     } catch (error) {
        //         console.error('Error requesting service:', error);
        //         alert('Failed to request service. Please try again.');
        //     }
        // },

        async requestService(serviceId) {
            try {
                const token = localStorage.getItem('token');
                // console.log("🔐 JWT Token:", token);
                // Step 1: Fetch professionals who offer this service
                const professionalsResponse = await axios.get(`http://127.0.0.1:5858/customer/professionals/${serviceId}`,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                console.log("professionalsResponse", professionalsResponse.data)

                if (professionalsResponse.data.length === 0) {
                    alert("No professionals available for this service.");
                    return;
                }
                if (!serviceId) {
                    console.error("🚨 serviceId is undefined or null!");
                    alert("Service ID is missing. Please try again.");
                    return;
                }
                console.log("🔄 Navigating to selectProfessional with serviceId:", serviceId);

                // Redirect customer to professional selection page
                this.$router.push({
                    name: "selectProfessional",
                    query: { serviceId: serviceId },
                });

                // // Step 2: Ask the customer to choose a professional
                // let professionalOptions = professionalsResponse.data.map(prof => `${prof.id}: ${prof.name}`).join('\n');
                // let selectedProfId = prompt(`Select a professional by entering their ID:\n${professionalOptions}`);

                // if (!selectedProfId) {
                //     alert("You must select a professional to proceed.");
                //     return;
                // }

                // const userName = await getUserName(); // Get name from utility function
                // console.log("👤 User Name:", userName);

                // const response = await axios.post('http://127.0.0.1:5858/customer/service_request',
                //     {
                //         service_id: serviceId,
                //         professional_id: parseInt(selectedProfId),
                //         remarks: `${userName} requested this service`
                //     },
                //     { headers: { Authorization: `Bearer ${token}` } }
                // );
                // console.log(serviceId),
                //     console.log(response.data.message);
                // console.log(professionalsResponse.data.message)
                // alert(professionalsResponse.data.message); // Show success message
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