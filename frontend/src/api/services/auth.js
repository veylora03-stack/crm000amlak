import api, { getRefreshToken, setTokens, clearAuthStorage } from '../client'

function unwrap(response) {
  if (!response) {
    return null
  }

  if (response.success && 'data' in response) {
    return response.data
  }

  return response
}

const authApi = {
  async login(payload) {
    const body = unwrap(await api.post('/auth/login/', payload))

    if (body?.access && body?.refresh) {
      setTokens({
        access: body.access,
        refresh: body.refresh
      })
    }

    return body?.user || body
  },

  async logout() {
    const refresh = getRefreshToken()

    try {
      await api.post('/auth/logout/', { refresh })
    } finally {
      clearAuthStorage()
    }
  },

  async refresh() {
    const refresh = getRefreshToken()
    const body = unwrap(await api.post('/auth/refresh/', { refresh }))

    if (body?.access) {
      setTokens(body)
    }

    return body
  },

  async me() {
    return unwrap(await api.get('/auth/me/'))
  },

  async updateMe(payload) {
    return unwrap(await api.patch('/auth/me/', payload))
  },

  async changePassword(payload) {
    return unwrap(await api.post('/auth/change-password/', payload))
  }
}

export default authApi
