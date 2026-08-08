import { defineStore } from 'pinia'
import { authApi } from '@/api'

const TOKEN_KEY = 'auth_token'
const USER_KEY = 'auth_user'

function readUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY) || 'null')
  } catch (error) {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    user: readUser(),
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    role: (state) => state.user?.role || null,
    isAdmin: (state) => state.user?.role === 'Admin',
    isManager: (state) => ['Admin', 'Manager'].includes(state.user?.role),
    displayName: (state) => state.user?.full_name || state.user?.username || 'کاربر'
  },

  actions: {
    setAuth(token, user) {
      this.token = token
      this.user = user
      localStorage.setItem(TOKEN_KEY, token)
      localStorage.setItem(USER_KEY, JSON.stringify(user))
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
    },

    clearError() {
      this.error = null
    },

    async login(payload) {
      this.loading = true
      this.error = null

      try {
        const userData = await authApi.login(payload)
        this.user = userData
        this.token = localStorage.getItem(TOKEN_KEY) || ''
        return true
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'نام کاربری یا رمز عبور اشتباه است.'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchMe() {
      if (!this.token) return
      try {
        const userData = await authApi.me()
        this.user = userData
        localStorage.setItem(USER_KEY, JSON.stringify(userData))
      } catch (error) {
        // Will be handled by interceptor (401 -> logout)
      }
    }
  }
})
