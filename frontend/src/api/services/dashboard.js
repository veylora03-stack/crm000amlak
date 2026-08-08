import api from '../client'

const base = '/dashboard/'

const dashboardApi = {
  kpis(params = {}) {
    return api.get(`${base}kpis/`, { params })
  },

  charts(params = {}) {
    return api.get(`${base}charts/`, { params })
  },

  recentActivities(params = {}) {
    return api.get(`${base}recent-activities/`, { params })
  }
}

export default dashboardApi
