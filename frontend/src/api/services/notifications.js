import api from '../client'

const base = '/notifications/'

const notificationsApi = {
  list(params = {}) {
    return api.get(base, { params })
  },

  retrieve(publicId) {
    return api.get(`${base}${publicId}/`)
  },

  create(payload) {
    return api.post(base, payload)
  },

  remove(publicId) {
    return api.delete(`${base}${publicId}/`)
  },

  markRead(publicId) {
    return api.post(`${base}${publicId}/read/`)
  },

  markAllRead() {
    return api.post(`${base}read-all/`)
  }
}

export default notificationsApi
