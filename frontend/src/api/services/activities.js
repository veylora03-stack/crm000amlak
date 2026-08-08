import api from '../client'

const base = '/interactions/'

const activitiesApi = {
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
  }
}

export default activitiesApi
