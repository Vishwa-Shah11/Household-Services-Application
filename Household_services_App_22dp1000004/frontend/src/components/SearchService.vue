<template>
    <div class="search-container">
        <h2 class="text-center">Search Services</h2>

        <div class="search-box">
            <input v-model="searchQuery" @input="searchServices" placeholder="Search for services..." class="form-control" />
            <ul v-if="searchResults.length" class="search-results">
                <li v-for="service in searchResults" :key="service.id" class="search-item">
                    <router-link :to="'/select-professional?serviceId=' + service.id" class="search-link">
                        {{ service.name }}
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            searchQuery: '',
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
            if (this.searchQuery.length < 3) return;
            try {
                const response = await axios.get(`http://127.0.0.1:5858/service/search?query=${this.searchQuery}`, {
                    headers: { "Authorization": `Bearer ${token}` }
                });
                this.searchResults = response.data.services;
            } catch (error) {
                console.error("Search failed:", error);
                alert("Search failed! Please try again.");
            }
        }
    }
};
</script>

<style scoped>
.search-container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
    text-align: center;
}

h2 {
    color: #333;
    font-weight: 600;
    margin-bottom: 20px;
}

.search-box {
    position: relative;
    display: flex;
    flex-direction: column;
}

.form-control {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ddd;
    font-size: 16px;
    width: 100%;
    transition: all 0.2s ease-in-out;
}

.form-control:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
}

.search-results {
    list-style: none;
    padding: 0;
    margin-top: 10px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.search-item {
    padding: 10px;
    border-bottom: 1px solid #ddd;
    transition: background 0.2s;
}

.search-item:hover {
    background: #f1f1f1;
}

.search-link {
    text-decoration: none;
    color: #007bff;
    font-weight: 500;
    transition: color 0.2s;
}

.search-link:hover {
    color: #0056b3;
}
</style>