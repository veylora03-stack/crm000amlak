// API Client
export { default as api } from './client'

// Resource Factory (for advanced usage)
export { createResource, createSubResource, createSingleton } from './resourceFactory'

// Composables
export { useApiResource, useSingletonResource } from '@/composables/useApiResource'

// Error Handler
export { handleApiError, parseApiError, withErrorHandling } from './errorHandler'

// All service APIs
export { default as authApi } from './services/auth'
export { default as usersApi } from './services/users'
export { default as clientsApi } from './services/clients'
export { default as propertiesApi } from './services/properties'
export { default as salesApi } from './services/sales'
export { default as activitiesApi } from './services/activities'
export { default as tasksApi } from './services/tasks'
export { default as notificationsApi } from './services/notifications'
export { default as dashboardApi } from './services/dashboard'
export { default as reportsApi } from './services/reports'
export { default as settingsApi } from './services/settings'
export { default as searchApi } from './services/search'
