import { createResource } from '../resourceFactory'
import api from '../client'

const base = createResource('notifications')

export default {
  ...base,
  
  markRead(publicId) {
    return api.post(`/notifications/${publicId}/read/`)
  },
  
  markAllRead() {
    return api.post('/notifications/read-all/')
  }
}
