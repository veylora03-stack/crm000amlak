import api from '../client'

const base = '/clients/'

const clientsApi = {
  list(params = {}) {
    return api.get(base, { params })
  },

  retrieve(publicId) {
    return api.get(`${base}${publicId}/`)
  },

  create(payload) {
    return api.post(base, payload)
  },

  update(publicId, payload) {
    return api.put(`${base}${publicId}/`, payload)
  },

  partialUpdate(publicId, payload) {
    return api.patch(`${base}${publicId}/`, payload)
  },

  remove(publicId) {
    return api.delete(`${base}${publicId}/`)
  },

  timeline(publicId) {
    return api.get(`${base}${publicId}/timeline/`)
  },

  deals(publicId) {
    return api.get(`${base}${publicId}/deals/`)
  },

  interactions(publicId) {
    return api.get(`${base}${publicId}/interactions/`)
  },

  assign(publicId, assignedAgentPublicId) {
    return api.post(`${base}${publicId}/assign/`, {
      assigned_agent: assignedAgentPublicId
    })
  }
}

export default clientsApi
