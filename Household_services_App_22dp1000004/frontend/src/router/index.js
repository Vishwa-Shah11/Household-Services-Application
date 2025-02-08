import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import CustomerDashboard from '../components/CustomerDashboard.vue';
import ProfessionalDashboard from '../components/ProfessionalDashboard.vue';

const routes = [
    { path: '/', component: HomeView },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/admin-dashboard', component: AdminDashboard },
    { path: '/customer-dashboard', component: CustomerDashboard },
    { path: '/professional-dashboard', component: ProfessionalDashboard },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
