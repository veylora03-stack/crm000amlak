import axios from 'axios'
import router from '@/router'

export const TOKEN_KEY = 'auth_token'
export const REFRESH_TOKEN_KEY = 'refresh_token'
export const USER_KEY = 'auth_user'

const baseURL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

const api = axios.create({
  baseURL,
  timeout: 20000,
  headers: {
    Accept: 'application/json'
  }
})

let isRefreshing = false
let failedQueue = []

function processQueue(error, token = null) {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error)
    } else {
      promise.resolve(token)
    }
  })
  failedQueue = []
}

export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY) || ''
}

export function setTokens(tokens) {
  if (!tokens) return
  if (tokens.access) localStorage.setItem(TOKEN_KEY, tokens.access)
  if (tokens.refresh) localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh)
}

export function clearAuthStorage() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

api.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => {
    if (response.config.responseType === 'blob') {
      return response
    }
    return response.data
  },
  async (error) => {
    const originalRequest = error.config

    if (!originalRequest) {
      return Promise.reject(error)
    }

    const isUnauthorized = error.response && error.response.status === 401
    const isRefreshRequest = originalRequest.url && originalRequest.url.includes('/auth/refresh/')
    const isLoginRequest = originalRequest.url && originalRequest.url.includes('/auth/login/')
    const shouldRetry = isUnauthorized && !originalRequest._retry && !isRefreshRequest && !isLoginRequest

    if (!shouldRetry) {
      if (isUnauthorized && !isLoginRequest) {
        clearAuthStorage()
        if (router.currentRoute.value.name !== 'login') {
          router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } })
        }
      }
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      }).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`
        return api(originalRequest)
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    try {
      const refreshToken = getRefreshToken()
      if (!refreshToken) throw new Error('NO_REFRESH_TOKEN')

      const refreshResponse = await axios.post(`${baseURL}/auth/refresh/`, { refresh: refreshToken })
      const responseData = refreshResponse.data || {}
      const tokens = responseData.data || responseData

      if (tokens.access) setTokens(tokens)
      
      processQueue(null, tokens.access)
      originalRequest.headers.Authorization = `Bearer ${tokens.access}`
      return api(originalRequest)
    } catch (refreshError) {
      processQueue(refreshError, null)
      clearAuthStorage()
      if (router.currentRoute.value.name !== 'login') {
        router.push('/login')
      }
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)

export default api
