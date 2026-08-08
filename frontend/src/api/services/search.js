import api from '../client'

const searchApi = {
  global(query) {
    return api.get('/search/', {
      params: {
        q: query
      }
    })
  }
}

export default searchApi
