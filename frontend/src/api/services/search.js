import api from '../client'

export default {
  global(query) {
    return api.get('/search/', {
      params: { q: query }
    })
  }
}
