// API Client
export { default as api } from './client'

// Resource Factory (for advanced usage)
export { createResource, createSubResource, createSingleton } from './resourceFactory'

// Composables
export { useApiResource, useSingletonResource } from '@/composables/useApiResource'

// All service APIs
export * from './services'
