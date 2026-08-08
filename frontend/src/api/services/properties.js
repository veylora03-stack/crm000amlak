import api from '../client'

const base = '/properties/'

const propertiesApi = {
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

  uploadImage(publicId, file, options = {}) {
    const formData = new FormData()

    formData.append('image', file)

    if (options.alt_text) {
      formData.append('alt_text', options.alt_text)
    }

    if (options.is_primary) {
      formData.append('is_primary', 'true')
    }

    return api.post(`${base}${publicId}/images/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  publish(publicId) {
    return api.post(`${base}${publicId}/publish/`)
  },

  archive(publicId) {
    return api.post(`${base}${publicId}/archive/`)
  },

  matches(publicId) {
    return api.get(`${base}${publicId}/matches/`)
  }
}

export default propertiesApi
