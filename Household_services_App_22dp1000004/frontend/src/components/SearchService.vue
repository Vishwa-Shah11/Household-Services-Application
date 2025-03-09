<template>
    <div class="container mt-4">
        <h2>Search Services</h2>

        <div>
            <input v-model="searchQuery" @input="searchServices" placeholder="Search for services..." />
            <ul v-if="searchResults.length">
                <li v-for="service in searchResults" :key="service.id">
                    <router-link :to="'/service/' + service.id">{{ service.name }}</router-link>
                </li>
            </ul>
        </div>

        <!-- Search Form -->
        <!-- <form @submit.prevent="searchServices">
            <div class="mb-3">
                <input v-model="searchQuery.name" type="text" class="form-control"
                    placeholder="Search by Service Name" />
            </div>
            <div class="mb-3">
                <input v-model="searchQuery.category" type="text" class="form-control"
                    placeholder="Search by Category" />
            </div>
            <div class="mb-3">
                <input v-model="searchQuery.pin_code" type="text" class="form-control"
                    placeholder="Search by Pin Code" />
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
        </form> -->

        <!-- Display Search Results -->
        <!-- <div v-if="services.length" class="mt-4">
            <h3>Search Results</h3>
            <ul class="list-group">
                <li v-for="service in services" :key="service.id" class="list-group-item">
                    <h5>{{ service.name }}</h5>
                    <p>{{ service.description }}</p>
                    <p><strong>Base Price:</strong> {{ service.base_price }}</p>
                    <p><strong>Category:</strong> {{ service.category }}</p>
                </li>
            </ul>
        </div>

        <div v-else-if="message" class="mt-4 alert alert-warning">
            {{ message }}
        </div> -->
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            // searchQuery: {
            //     name: "",
            //     category: "",
            //     pin_code: "",
            // },
            searchQuery: '',
            services: [],
            message: "",
            searchResults: []
        };
    },
    methods: {
        async searchServices() {
            const token = localStorage.getItem("token");
            if (!token) {
                alert("You are not authenticated! Please log in again.");
                return;
            }
            console.log(token);
            if (this.searchQuery.length < 3) return;
            console.log(this.searchQuery);
            try {
                // const response = await axios.get("http://127.0.0.1:5858/customer/search_services", {
                //     params: this.searchQuery,
                //     headers: { Authorization: `Bearer ${token}` }
                // });

                const response = await axios.get(`http://127.0.0.1:5858/service/search?query=${this.searchQuery}`, {
                    headers: {
                        "Authorization": `Bearer ${token}` // Attach JWT token
                    }
                });

                console.log(response.data.services);
                this.searchResults = response.data.services;

                // this.services = response.data.services;
                // this.message = "";
            } catch (error) {
                console.error("Search failed:", error);
                alert("Search failed! Please try again.");
                // this.services = [];
                // if (error.response && error.response.status === 404) {
                //     this.message = "No matching services found.";
                // } else {
                //     this.message = "Error fetching services.";
                // }
            }
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 600px;
    margin: auto;
}
</style>