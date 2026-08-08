/**
 * API Resource Factory
 * 
 * Eliminates duplicate CRUD code across all API services.
 * Provides a standardized interface for all RESTful endpoints.
 * 
 * @example
 * // Basic CRUD resource
 * const clientsApi = createResource('clients')
 * 
 * // Extended resource with custom endpoints
 * const clientsApi = createResource('clients', {
 *   timeline: (id) => api.get(`/clients/${id}/timeline/`),
 *   assign: (id, agentId) => api.post(`/clients/${id}/assign/`, { assigned_agent: agentId })
 * })
 */
import api from './client'

/**
 * Creates a standard REST resource with CRUD operations
 * 
 * @param {string} endpoint - The API endpoint (without slashes)
 * @param {Object} extensions - Additional custom methods
 * @returns {Object} API resource with standard CRUD + custom methods
 */
export function createResource(endpoint, extensions = {}) {
  const base = `/${endpoint}`
  
  const resource = {
    // ===== Standard CRUD Operations =====
    
    /**
     * List all resources with optional filters
     * @param {Object} params - Query parameters (filters, pagination, search)
     */
    list(params = {}) {
      return api.get(`${base}/`, { params })
    },

    /**
     * Get a single resource by ID
     * @param {string} publicId - Resource UUID
     */
    retrieve(publicId) {
      return api.get(`${base}/${publicId}/`)
    },

    /**
     * Create a new resource
     * @param {Object} payload - Resource data
     */
    create(payload) {
      return api.post(`${base}/`, payload)
    },

    /**
     * Full update of a resource (PUT)
     * @param {string} publicId - Resource UUID
     * @param {Object} payload - Complete resource data
     */
    update(publicId, payload) {
      return api.put(`${base}/${publicId}/`, payload)
    },

    /**
     * Partial update of a resource (PATCH)
     * @param {string} publicId - Resource UUID
     * @param {Object} payload - Partial resource data
     */
    partialUpdate(publicId, payload) {
      return api.patch(`${base}/${publicId}/`, payload)
    },

    /**
     * Delete (soft-delete) a resource
     * @param {string} publicId - Resource UUID
     */
    remove(publicId) {
      return api.delete(`${base}/${publicId}/`)
    },

    // ===== Utility Methods =====
    
    /**
     * Bulk delete multiple resources
     * @param {string[]} publicIds - Array of UUIDs
     */
    async bulkRemove(publicIds) {
      return Promise.all(publicIds.map(id => this.remove(id)))
    },

    /**
     * Export resources as file
     * @param {Object} params - Query parameters
     * @param {string} format - Export format (csv, xlsx)
     */
    export(publicIds = [], format = 'csv') {
      return api.get(`${base}/export/`, {
        params: { format, ids: publicIds.join(',') },
        responseType: 'blob'
      })
    }
  }
  
  // Merge custom extensions (override defaults if needed)
  return { ...resource, ...extensions }
}

/**
 * Creates a sub-resource under a parent endpoint
 * Useful for nested resources like /clients/{id}/notes
 * 
 * @param {string} parentEndpoint - Parent endpoint
 * @param {string} subEndpoint - Sub-resource endpoint
 */
export function createSubResource(parentEndpoint, subEndpoint) {
  const getParent = (parentId) => `/${parentEndpoint}/${parentId}/${subEndpoint}`
  
  return {
    list(parentId, params = {}) {
      return api.get(`${getParent(parentId)}/`, { params })
    },
    
    retrieve(parentId, subId) {
      return api.get(`${getParent(parentId)}/${subId}/`)
    },
    
    create(parentId, payload) {
      return api.post(`${getParent(parentId)}/`, payload)
    },
    
    update(parentId, subId, payload) {
      return api.patch(`${getParent(parentId)}/${subId}/`, payload)
    },
    
    remove(parentId, subId) {
      return api.delete(`${getParent(parentId)}/${subId}/`)
    }
  }
}

/**
 * Creates a singleton resource (no ID, like /settings)
 */
export function createSingleton(endpoint) {
  return {
    get() {
      return api.get(`/${endpoint}/`)
    },
    
    update(payload) {
      return api.patch(`/${endpoint}/`, payload)
    },
    
    replace(payload) {
      return api.put(`/${endpoint}/`, payload)
    }
  }
}
