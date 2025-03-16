<template>
    <div v-if="service">
        <h2>{{ service.name }}</h2>
        <p>{{ service.description }}</p>
        <p>Price: {{ service.base_price }}</p>
        <router-link to="/service/search">Back to Search</router-link>
    </div>

    <div v-else-if="message" class="mt-4 alert alert-warning">
        {{ message }}
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return { service: null };
    },
    async created() {
        const serviceId = this.$route.params.id;
        try {
            const response = await axios.get(`http://127.0.0.1:5858/service/${serviceId}`);
            this.service = response.data;
        } catch (error) {
            console.error("Failed to fetch service:", error);
        }
    }
};
</script>