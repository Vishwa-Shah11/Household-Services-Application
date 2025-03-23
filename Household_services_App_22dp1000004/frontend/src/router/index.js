import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import CustomerDashboard from '../components/CustomerDashboard.vue';
import CategoryServices from '@/components/CategoryServices.vue';
import ProfessionalDashboard from '../components/ProfessionalDashboard.vue';
import ServiceRemarks from '@/components/ServiceRemarks.vue';
import SearchService from '@/components/SearchService.vue';
import ServiceDetails from '@/components/ServiceDetails.vue';
import ManageUsers from '@/components/ManageUsers.vue';
//import SelectProfessional from '@/components/SelectProfessional.vue';
import SearchProfessionals from '../components/SearchProfessionals.vue';
import AdminSummary from '@/components/AdminSummary.vue';
import CustomerSummary from '@/components/CustomerSummary.vue';
import ProfessionalSummary from '@/components/ProfessionalSummary.vue';

const routes = [
    { path: '/', redirect: '/home' },
    { path: '/home', component: HomeView },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/admin/dashboard', component: AdminDashboard, meta: { requiresAuth: true } },
    { path: '/admin/users', component: ManageUsers, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/search-professionals', component: SearchProfessionals, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/summary', component: AdminSummary, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/customer/summary', component: CustomerSummary, meta: { requiresAuth: true, role: 'Customer' } },
    { path: '/customer/dashboard', component: CustomerDashboard, meta: { requiresAuth: true } },
    { path: '/category/:category', component: CategoryServices, meta: { requiresAuth: true } },
    //{ path: '/select-professional/:serviceId', component: SelectProfessional, meta: { requiresAuth: true } },
    {
      path: "/select-professional",
      name: "selectProfessional", // ✅ Ensure lowercase if you're using it in push()
      component: () => import("@/components/SelectProfessional.vue")
  },
    { path: "/service-remarks/:requestId", component: ServiceRemarks },
    { path: "/service/search", component: SearchService },
    { path: '/service/:id', component: ServiceDetails },
    { path: '/professional/dashboard', component: ProfessionalDashboard, meta: { requiresAuth: true } },
    { path: '/professional/summary', component: ProfessionalSummary, meta: { requiresAuth: true, role: 'Professional' } },
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
