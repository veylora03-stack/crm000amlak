import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy load all pages for code splitting
const LoginPage = () => import('@/pages/auth/LoginPage.vue')
const ForgotPasswordPage = () => import('@/pages/auth/ForgotPasswordPage.vue')
const ResetPasswordPage = () => import('@/pages/auth/ResetPasswordPage.vue')
const DashboardPage = () => import('@/pages/dashboard/DashboardPage.vue')
const ClientsPage = () => import('@/pages/clients/ClientsPage.vue')
const ClientDetailPage = () => import('@/pages/clients/ClientDetailPage.vue')
const PropertiesPage = () => import('@/pages/properties/PropertiesPage.vue')
const PropertyDetailPage = () => import('@/pages/properties/PropertyDetailPage.vue')
const PipelinePage = () => import('@/pages/pipeline/PipelinePage.vue')
const DealsPage = () => import('@/pages/deals/DealsPage.vue')
const TasksPage = () => import('@/pages/tasks/TasksPage.vue')
const ReportsPage = () => import('@/pages/reports/ReportsPage.vue')
const NotificationsPage = () => import('@/pages/notifications/NotificationsPage.vue')
const SettingsPage = () => import('@/pages/settings/SettingsPage.vue')
const UsersPage = () => import('@/pages/users/UsersPage.vue')
const ProfilePage = () => import('@/pages/profile/ProfilePage.vue')

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/reset-password/:token',
    name: 'reset-password',
    component: ResetPasswordPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/clients',
    name: 'clients',
    component: ClientsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/clients/:id',
    name: 'client-detail',
    component: ClientDetailPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/properties',
    name: 'properties',
    component: PropertiesPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/properties/:id',
    name: 'property-detail',
    component: PropertyDetailPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/pipeline',
    name: 'pipeline',
    component: PipelinePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/deals',
    name: 'deals',
    component: DealsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: TasksPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'reports',
    component: ReportsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: NotificationsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/users',
    name: 'users',
    component: UsersPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresGuest && auth.isAuthenticated) {
    next({ name: 'dashboard' })
  } else if (to.meta.requiresAdmin && !auth.isAdmin) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
