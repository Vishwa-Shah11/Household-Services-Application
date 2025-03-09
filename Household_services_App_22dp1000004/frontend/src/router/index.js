import { createRouter, createWebHistory } from 'vue-router';
//import HomeView from '../views/HomeView.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import CustomerDashboard from '../components/CustomerDashboard.vue';
import CategoryServices from '@/components/CategoryServices.vue';
import ProfessionalDashboard from '../components/ProfessionalDashboard.vue';
import ServiceRemarks from '@/components/ServiceRemarks.vue';
import SearchService from '@/components/SearchService.vue';
import ServiceDetails from '@/components/ServiceDetails.vue';

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/admin/dashboard', component: AdminDashboard, meta: { requiresAuth: true } },
    { path: '/customer/dashboard', component: CustomerDashboard, meta: { requiresAuth: true } },
    { path: '/category/:category', component: CategoryServices, meta: { requiresAuth: true } },
    { path: "/service-remarks/:requestId", component: ServiceRemarks },
    { path: "/service/search", component: SearchService },
    { path: '/service/:id', component: ServiceDetails },
    { path: '/professional/dashboard', component: ProfessionalDashboard, meta: { requiresAuth: true } },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// 🔐 Navigation Guard to protect routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token'); // Check if token exists
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // Redirect to login if not authenticated
  } else {
    next();
  }
});

export default router;
