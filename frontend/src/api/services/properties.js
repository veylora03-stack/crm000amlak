import { createResource } from '../resourceFactory'
import api from '../client'

const base = createResource('properties')

export default {
  ...base,
  
  uploadImage(publicId, file, options = {}) {
    const formData = new FormData()
    formData.append('image', file)
    if (options.alt_text) formData.append('alt_text', options.alt_text)
    if (options.is_primary) formData.append('is_primary', 'true')
    
    return api.post(`/properties/${publicId}/images/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  publish(publicId) {
    return api.post(`/properties/${publicId}/publish/`)
  },
  
  archive(publicId) {
    return api.post(`/properties/${publicId}/archive/`)
  },
  
  matches(publicId) {
    return api.get(`/properties/${publicId}/matches/`)
  }
}
