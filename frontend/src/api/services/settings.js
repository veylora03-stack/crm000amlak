import api from '../client'

const base = '/settings/'

const settingsApi = {
  get() {
    return api.get(base)
  },

  update(payload) {
    return api.patch(base, payload)
  }
}

export default settingsApi
