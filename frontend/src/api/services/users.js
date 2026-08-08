import { createResource } from '../resourceFactory'
import api from '../client'

const base = createResource('users')

export default {
  ...base,
  
  activate(publicId) {
    return api.post(`/users/${publicId}/activate/`)
  },
  
  deactivate(publicId) {
    return api.post(`/users/${publicId}/deactivate/`)
  },
  
  changePassword(publicId, payload) {
    return api.post(`/users/${publicId}/change-password/`, payload)
  }
}
