import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/auth/LoginPage.vue'),
    meta: { requiresAuth: false, guestOnly: true, title: 'ورود' }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('@/pages/auth/ForgotPasswordPage.vue'),
    meta: { requiresAuth: false, guestOnly: true, title: 'فراموشی رمز عبور' }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: () => import('@/pages/auth/ResetPasswordPage.vue'),
    meta: { requiresAuth: false, guestOnly: true, title: 'بازنشانی رمز عبور' }
  },
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'dashboard', component: () => import('@/pages/dashboard/DashboardPage.vue'), meta: { requiresAuth: true, title: 'داشبورد' } },
  { path: '/clients', name: 'clients', component: () => import('@/pages/clients/ClientsPage.vue'), meta: { requiresAuth: true, title: 'مشتریان' } },
  { path: '/clients/:id', name: 'client-detail', component: () => import('@/pages/clients/ClientDetailPage.vue'), meta: { requiresAuth: true, title: 'جزئیات مشتری' } },
  { path: '/properties', name: 'properties', component: () => import('@/pages/properties/PropertiesPage.vue'), meta: { requiresAuth: true, title: 'املاک' } },
  { path: '/properties/:id', name: 'property-detail', component: () => import('@/pages/properties/PropertyDetailPage.vue'), meta: { requiresAuth: true, title: 'جزئیات ملک' } },
  { path: '/pipeline', name: 'pipeline', component: () => import('@/pages/pipeline/PipelinePage.vue'), meta: { requiresAuth: true, title: 'پایپ‌لاین فروش' } },
  { path: '/deals', name: 'deals', component: () => import('@/pages/deals/DealsPage.vue'), meta: { requiresAuth: true, title: 'معاملات' } },
  { path: '/tasks', name: 'tasks', component: () => import('@/pages/tasks/TasksPage.vue'), meta: { requiresAuth: true, title: 'وظایف' } },
  { path: '/reports', name: 'reports', component: () => import('@/pages/reports/ReportsPage.vue'), meta: { requiresAuth: true, roles: ['Admin', 'Manager'], title: 'گزارش‌ها' } },
  { path: '/notifications', name: 'notifications', component: () => import('@/pages/notifications/NotificationsPage.vue'), meta: { requiresAuth: true, title: 'نوتیفیکیشن‌ها' } },
  { path: '/settings', name: 'settings', component: () => import('@/pages/settings/SettingsPage.vue'), meta: { requiresAuth: true, roles: ['Admin'], title: 'تنظیمات' } },
  { path: '/profile', name: 'profile', component: () => import('@/pages/profile/ProfilePage.vue'), meta: { requiresAuth: true, title: 'پروفایل' } },
  { path: '/users', name: 'users', component: () => import('@/pages/users/UsersPage.vue'), meta: { requiresAuth: true, roles: ['Admin'], title: 'کاربران' } },
  { path: '/:pathMatch(.*)*', redirect: '/dashboard' }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  if (to.meta && to.meta.title) {
    document.title = `${to.meta.title} — CRM تخصصی املاک`
  } else {
    document.title = 'CRM تخصصی املاک'
  }

  // If route requires auth and user is not authenticated
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  // If route is for guests only and user is authenticated
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return next({ name: 'dashboard' })
  }

  // Check role permissions
  if (to.meta.roles && auth.isAuthenticated && !to.meta.roles.includes(auth.role)) {
    return next({ name: 'dashboard' })
  }

  next()
})

export default router
