import api from '../client'

const base = '/reports/'

const reportsApi = {
  leads(params = {}) {
    return api.get(`${base}leads/`, { params })
  },

  deals(params = {}) {
    return api.get(`${base}deals/`, { params })
  },

  agents(params = {}) {
    return api.get(`${base}agents/`, { params })
  },

  funnel(params = {}) {
    return api.get(`${base}funnel/`, { params })
  },

  properties(params = {}) {
    return api.get(`${base}properties/`, { params })
  },

  exportFile(params = {}) {
    return api.get(`${base}export/`, {
      params,
      responseType: 'blob'
    })
  }
}

export default reportsApi
