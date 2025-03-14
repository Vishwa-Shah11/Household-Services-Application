<template>
    <div class="container">
        <h2 class="text-center my-4">All Users</h2>

        <p v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</p>

        <div class="table-responsive">
            <table class="table table-bordered table-striped text-center">
                <thead class="thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Profile Docs</th>
                        <th>Approved</th>
                        <th>Blocked</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.role }}</td>
                        <td>
                            <span v-if="user.role === 'Customer'" class="text-muted">
                                Not required
                            </span>
                            <span v-if="user.role === 'Professional' && user.profile_docs === 'Not Uploaded'" class="text-danger">
                                Not Uploaded
                            </span>
                            <a v-else-if="user.role === 'Professional'" :href="'http://127.0.0.1:5858/professional/' + user.profile_docs" target="_blank">
                                View Document
                            </a>
                        </td>
                        <td>{{ user.is_approved !== null ? (user.is_approved ? 'Yes' : 'No') : 'N/A' }}</td>
                        <td>{{ user.is_blocked ? "Blocked" : "Active" }}</td>
                        /if professional has not uploaded profile docs, admin can not perform approve/reject actions
                        <td v-if="user.role === 'Professional'">
                            <button class="btn btn-success btn-sm mx-1" @click="approveUser(user.id)"
                                :disabled="!user.profile_docs || user.is_approved || user.profile_docs === null"
                                :title="!user.profile_docs ? 'Profile docs not uploaded' : ''">
                                Approve
                            </button>
                            <button class="btn btn-danger btn-sm mx-1" @click="rejectUser(user.id)"
                                :disabled="!user.profile_docs || user.is_approved === false || user.profile_docs === null"
                                :title="!user.profile_docs ? 'Profile docs not uploaded' : ''">
                                Reject
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const users = ref([]);
const errorMessage = ref("");

// Fetch users on component mount
const fetchUsers = async () => {
    try {
        const token = localStorage.getItem("token"); // Get Admin token

        if (!token) {
            errorMessage.value = "Unauthorized access! Please log in as Admin.";
            return;
        }

        const response = await axios.get("http://127.0.0.1:5858/admin/users", {
            headers: { "Authorization": `Bearer ${token}` },
        });

        users.value = response.data.users; // ✅ Store users in Vue state

    } catch (error) {
        console.error("Error fetching users:", error);
        errorMessage.value = "Failed to load users.";
    }
};

// Approve Professional
const approveUser = async (userId) => {
    if (!confirm("Are you sure you want to approve this professional?")) {
        return;
    }
    try {
        const token = localStorage.getItem("token");

        const response = await axios.post(`http://127.0.0.1:5858/admin/approve/${userId}`, {}, {
            headers: { "Authorization": `Bearer ${token}` },
        });

        if (response.status === 200) {
            const username = response.data.username;
            // Update UI
            const user = users.value.find(user => user.id === userId);
            if (user) {
                user.is_approved = true;
                alert(`User ${username} has been approved!`);
            }
        } else {
            console.error("Unexpected response:", response);
            errorMessage.value = "Unexpected response received.";
        }

    } catch (error) {
        console.error("Approval failed:", error);
        if (error.response) {
            console.error("Server response:", error.response.data);
        }
        errorMessage.value = "Failed to approve user.";
    }
};

// Reject Professional
const rejectUser = async (userId) => {
    if (!confirm("Are you sure you want to reject this professional?")) {
        return;
    }
    try {
        const token = localStorage.getItem("token");

        const response = await axios.post(`http://127.0.0.1:5858/admin/reject/${userId}`, {}, {
            headers: { "Authorization": `Bearer ${token}` },
        });

        if (response.status === 200) {
            const username = response.data.username;
            // Update UI
            const user = users.value.find(user => user.id === userId);
            if (user) {
                user.is_approved = false;
                alert(`User ${username} has been rejected!`);
            }
        } else {
            console.error("Unexpected response:", response);
            errorMessage.value = "Unexpected response received.";
        }
    } catch (error) {
        console.error("Rejection failed:", error);
        if (error.response) {
            console.error("Server response:", error.response.data);
        }
        errorMessage.value = "Failed to reject user.";
    }
};

// Load users when component is mounted
onMounted(fetchUsers);
</script>

<style scoped>
.container {
    max-width: 900px;
    margin: auto;
    background: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

h2 {
    color: #2c3e50;
}

.table {
    background: white;
}

th {
    background: #343a40;
    color: white;
}

.table-bordered {
    border: 1px solid #dddddd;
}

.alert {
    text-align: center;
    font-weight: bold;
}
</style>