import api from '../client'

export default {
  leads(params = {}) {
    return api.get('/reports/leads/', { params })
  },
  
  deals(params = {}) {
    return api.get('/reports/deals/', { params })
  },
  
  agents(params = {}) {
    return api.get('/reports/agents/', { params })
  },
  
  funnel(params = {}) {
    return api.get('/reports/funnel/', { params })
  },
  
  properties(params = {}) {
    return api.get('/reports/properties/', { params })
  },
  
  exportFile(params = {}) {
    return api.get('/reports/export/', {
      params,
      responseType: 'blob'
    })
  }
}
