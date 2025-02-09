import { createRouter, createWebHistory } from 'vue-router';
//import HomeView from '../views/HomeView.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import CustomerDashboard from '../components/CustomerDashboard.vue';
import ProfessionalDashboard from '../components/ProfessionalDashboard.vue';

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true } },
    { path: '/customer', component: CustomerDashboard, meta: { requiresAuth: true } },
    { path: '/professional', component: ProfessionalDashboard, meta: { requiresAuth: true } },
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
