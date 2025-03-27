<template>
  <div class="d-flex flex-column justify-content-center align-items-center vh-200">
    <h3 class="text-center text-primary fw-bold mb-4">Quique Care</h3>
    <div class="card shadow-lg p-4">
      <h2 class="text-center text-primary mb-4">Register</h2>
      
      <!-- Role Selection -->
      <div class="mb-3">
        <label class="form-label fw-bold">Select Role:</label>
        <select v-model="role" class="form-select">
          <option value="">Select</option>
          <option value="Customer">Customer</option>
          <option value="Professional">Professional</option>
        </select>
      </div>

      <!-- Common Fields -->
      <div class="row">
        <div class="col-md-6 mb-3">
          <input v-model="form.username" class="form-control" placeholder="Username" required />
        </div>
        <div class="col-md-6 mb-3">
          <input v-model="form.email" type="email" class="form-control" placeholder="Email" required />
        </div>
        <div class="col-md-6 mb-3">
          <input v-model="form.password" type="password" class="form-control" placeholder="Password" required />
        </div>
        <div class="col-md-6 mb-3">
          <input v-model="form.phone" class="form-control" placeholder="Phone Number" required />
        </div>
        <div class="col-md-6 mb-3">
          <input v-model="form.pincode" class="form-control" placeholder="Pincode" />
        </div>
        <div class="col-md-6 mb-3">
          <input v-model="form.address" class="form-control" placeholder="Address" />
        </div>
      </div>

      <!-- Professional-Specific Fields -->
      <div v-if="role === 'Professional'" class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">Upload Profile Document:</label>
          <input type="file" class="form-control" @change="handleFileUpload" />
        </div>
        <div class="col-md-6 mb-3">
          <input v-model="form.experience" class="form-control" placeholder="Experience" />
        </div>
      </div>

      <div v-if="role === 'Professional'">
        <div class="mb-3">
          <label for="category" class="form-label fw-bold">Select Your Category:</label>
          <select v-model="selectedCategory" class="form-select">
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>
      </div>

      <!-- Register Button -->
      <div class="text-center">
        <button @click="registerUser" class="btn btn-primary w-100">Register</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      role: "",
      form: {
        username: "",
        email: "",
        password: "",
        pincode: "",
        address: "",
        phone: "",
        experience: "", // Professional field
        profile_docs: null, // File upload
      },
      selectedCategory: null,
      categories: [],
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    handleFileUpload(event) {
      this.form.profile_docs = event.target.files[0];
    },
    async fetchCategories() {
      try {
        const response = await fetch("http://127.0.0.1:5858/auth/get_categories"); // API call

        if (!response.ok) {
          throw new Error("Failed to fetch categories");
        }
        const data = await response.json(); // Parse JSON response
        // console.log("Categories received:", data); // Debugging
        this.categories = data.categories; // Store categories in Vue data
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },
    async registerUser() {
      // console.log("🚀 Register button clicked!");
      const formData = new FormData();
      formData.append("role", this.role);
      formData.append("username", this.form.username);
      formData.append("email", this.form.email);
      formData.append("password", this.form.password);
      formData.append("pincode", this.form.pincode);
      formData.append("address", this.form.address);
      formData.append("phone", this.form.phone);
      if (this.role === "Professional") {
        formData.append("experience", this.form.experience);
        if (this.form.profile_docs) {
          formData.append("profile_docs", this.form.profile_docs);
        }
        formData.append("category", this.selectedCategory);
      }
      // console.log("Form Data:", Object.fromEntries(formData));

      try {
        const response = await axios.post("http://127.0.0.1:5858/auth/register", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        alert('Registration Successful! Please log in.');
        this.$router.push('/login');
      } catch (error) {
        console.error("Registration failed:", error);
        alert(error.response?.data?.error || "Registration failed");
      }
    },
  },
};
</script>

<style scoped>
.card {
  max-width: 600px;
  margin: auto;
  border-radius: 15px;
  background-color: #f8f9fa;
}

.form-control {
  border-radius: 8px;
}

.btn-primary {
  border-radius: 8px;
}
</style>
