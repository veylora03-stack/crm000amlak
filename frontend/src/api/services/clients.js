import { createResource } from '../resourceFactory'
import api from '../client'

const base = createResource('clients')

export default {
  ...base,
  
  // Custom endpoints
  timeline(publicId) {
    return api.get(`/clients/${publicId}/timeline/`)
  },
  
  deals(publicId) {
    return api.get(`/clients/${publicId}/deals/`)
  },
  
  interactions(publicId) {
    return api.get(`/clients/${publicId}/interactions/`)
  },
  
  assign(publicId, agentPublicId) {
    return api.post(`/clients/${publicId}/assign/`, {
      assigned_agent: agentPublicId
    })
  }
}
