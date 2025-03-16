<template>
    <div class="container">
        <h2 class="text-center my-4">Search Professionals</h2>

        <!-- Search Bar -->
        <div class="input-group mb-3">
            <input type="text" v-model="searchQuery" class="form-control" placeholder="Search professionals..." @input="searchProfessionals">
            <button class="btn btn-outline-secondary" @click="searchProfessionals">Search</button>
        </div>

        <p v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</p>

        <!-- Display Search Results -->
        <div class="table-responsive">
            <table class="table table-bordered table-striped text-center" v-if="professionals.length > 0">
                <thead class="thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Rating</th>
                        <th>Blocked</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in professionals" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>
                            <span v-if="user.rating !== null">{{ user.rating.toFixed(1) }} ⭐</span>
                            <span v-else class="text-muted">N/A</span>
                        </td>
                        <td>{{ user.is_blocked ? "Blocked" : "Active" }}</td>
                        <td>
                            <button class="btn btn-danger btn-sm mx-1" @click="toggleBlock(user.id, user.is_blocked)">
                                {{ user.is_blocked ? "Unblock" : "Block" }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <p v-if="professionals.length === 0 && !errorMessage" class="text-muted text-center">No professionals found.</p>
    </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const searchQuery = ref("");
const professionals = ref([]);
const errorMessage = ref("");

// Function to fetch search results
const searchProfessionals = async () => {
    try {
        const token = localStorage.getItem("token");

        if (!searchQuery.value.trim()) {
            errorMessage.value = "Please enter a search term!";
            professionals.value = [];
            return;
        }

        const response = await axios.get(`http://127.0.0.1:5858/admin/search_professionals?q=${searchQuery.value}`, {
            headers: { "Authorization": `Bearer ${token}` },
        });

        professionals.value = response.data.professionals;
        errorMessage.value = professionals.value.length === 0 ? "No professionals found." : "";

    } catch (error) {
        console.error("Error searching professionals:", error);
        errorMessage.value = "Failed to search professionals.";
    }
};

// Function to block/unblock a professional
const toggleBlock = async (userId, isBlocked) => {
    if (!confirm(`Are you sure you want to ${isBlocked ? "unblock" : "block"} this professional?`)) {
        return;
    }
    try {
        const token = localStorage.getItem("token");
        const endpoint = isBlocked ? "unblock" : "block";

        const response = await axios.post(`http://127.0.0.1:5858/admin/${endpoint}/${userId}`, {}, {
            headers: { "Authorization": `Bearer ${token}` },
        });

        if (response.status === 200) {
            // Update UI
            const user = professionals.value.find(user => user.id === userId);
            if (user) {
                user.is_blocked = !isBlocked;
                alert(`User ${user.name} has been ${isBlocked ? "unblocked" : "blocked"}!`);
            }
        } else {
            errorMessage.value = "Unexpected response received.";
        }

    } catch (error) {
        console.error("Failed to update block status:", error);
        errorMessage.value = "Failed to update user status.";
    }
};
</script>

<style scoped>
.input-group {
    max-width: 500px;
    margin: auto;
}
</style>
