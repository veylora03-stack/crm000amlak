import api from '../client'

export default {
  kpis(params = {}) {
    return api.get('/dashboard/kpis/', { params })
  },
  
  charts(params = {}) {
    return api.get('/dashboard/charts/', { params })
  },
  
  recentActivities(params = {}) {
    return api.get('/dashboard/recent-activities/', { params })
  }
}
