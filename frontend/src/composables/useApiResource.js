/**
 * useApiResource Composable
 * 
 * Vue 3 composable for managing API resource state in components.
 * Provides loading, error, and data states with automatic CRUD operations.
 * 
 * @example
 * // In a component
 * const { items, loading, error, fetchList, createItem } = useApiResource('clients')
 * 
 * onMounted(() => fetchList())
 */
import { ref, reactive } from 'vue'
import { createResource } from '@/api/resourceFactory'

/**
 * Composable for managing API resource state
 * 
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Configuration options
 * @param {boolean} options.autoFetch - Auto-fetch list on mount (default: false)
 * @param {Object} options.defaultParams - Default query parameters
 */
export function useApiResource(endpoint, options = {}) {
  const { autoFetch = false, defaultParams = {} } = options
  
  // Reactive state
  const items = ref([])
  const currentItem = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const meta = reactive({
    page: 1,
    pageSize: 20,
    total: 0,
    totalPages: 0
  })
  
  // Create API resource
  const resource = createResource(endpoint)
  
  // Error handler
  const handleError = (err) => {
    error.value = err?.response?.data?.errors?.[0]?.message 
      || err?.message 
      || 'خطای ناشناخته'
    loading.value = false
    return null
  }
  
  // List items
  const fetchList = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await resource.list({ ...defaultParams, ...params })
      const data = response.data || response
      
      // Handle paginated response
      if (Array.isArray(data)) {
        items.value = data
        meta.total = data.length
      } else if (data.results) {
        items.value = data.results
        meta.total = data.count || data.results.length
        meta.totalPages = Math.ceil(meta.total / meta.pageSize)
      } else {
        items.value = []
      }
      
      return items.value
    } catch (err) {
      return handleError(err)
    } finally {
      loading.value = false
    }
  }
  
  // Fetch single item
  const fetchItem = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await resource.retrieve(id)
      currentItem.value = response.data || response
      return currentItem.value
    } catch (err) {
      return handleError(err)
    } finally {
      loading.value = false
    }
  }
  
  // Create item
  const createItem = async (payload) => {
    loading.value = true
    error.value = null
    try {
      const response = await resource.create(payload)
      const newItem = response.data || response
      
      // Optimistic update
      items.value.unshift(newItem)
      meta.total++
      
      return newItem
    } catch (err) {
      return handleError(err)
    } finally {
      loading.value = false
    }
  }
  
  // Update item
  const updateItem = async (id, payload) => {
    loading.value = true
    error.value = null
    try {
      const response = await resource.partialUpdate(id, payload)
      const updatedItem = response.data || response
      
      // Update in list
      const index = items.value.findIndex(i => 
        String(i.public_id || i.id) === String(id)
      )
      if (index !== -1) {
        items.value[index] = { ...items.value[index], ...updatedItem }
      }
      
      // Update current item if it matches
      if (currentItem.value && String(currentItem.value.public_id || currentItem.value.id) === String(id)) {
        currentItem.value = { ...currentItem.value, ...updatedItem }
      }
      
      return updatedItem
    } catch (err) {
      return handleError(err)
    } finally {
      loading.value = false
    }
  }
  
  // Delete item
  const deleteItem = async (id) => {
    loading.value = true
    error.value = null
    try {
      await resource.remove(id)
      
      // Optimistic remove
      items.value = items.value.filter(i => 
        String(i.public_id || i.id) !== String(id)
      )
      meta.total--
      
      return true
    } catch (err) {
      return handleError(err)
    } finally {
      loading.value = false
    }
  }
  
  // Reset state
  const reset = () => {
    items.value = []
    currentItem.value = null
    loading.value = false
    error.value = null
    meta.page = 1
    meta.total = 0
  }
  
  // Pagination helpers
  const setPage = (page) => {
    meta.page = page
    return fetchList({ page, page_size: meta.pageSize })
  }
  
  // Auto-fetch if configured
  if (autoFetch) {
    fetchList()
  }
  
  return {
    // State
    items,
    currentItem,
    loading,
    error,
    meta,
    
    // CRUD operations
    fetchList,
    fetchItem,
    createItem,
    updateItem,
    deleteItem,
    
    // Helpers
    reset,
    setPage,
    
    // Raw resource for custom operations
    resource
  }
}

/**
 * Composable for singleton resources (no ID)
 */
export function useSingletonResource(endpoint) {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  const resource = {
    get: () => import('@/api/client').then(m => m.default.get(`/${endpoint}/`)),
    update: (payload) => import('@/api/client').then(m => m.default.patch(`/${endpoint}/`, payload))
  }
  
  const fetch = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await resource.get()
      data.value = response.data || response
      return data.value
    } catch (err) {
      error.value = err?.message || 'خطای ناشناخته'
      return null
    } finally {
      loading.value = false
    }
  }
  
  const update = async (payload) => {
    loading.value = true
    error.value = null
    try {
      const response = await resource.update(payload)
      data.value = { ...data.value, ...(response.data || response) }
      return data.value
    } catch (err) {
      error.value = err?.message || 'خطای ناشناخته'
      return null
    } finally {
      loading.value = false
    }
  }
  
  return { data, loading, error, fetch, update }
}
