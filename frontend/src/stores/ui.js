import { defineStore } from 'pinia'

const THEME_KEY = 'theme'

function getSystemTheme() {
  if (typeof window === 'undefined' || !window.matchMedia) {
    return 'light'
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export const useUiStore = defineStore('ui', {
  state: () => ({
    theme: localStorage.getItem(THEME_KEY) || 'system',
    sidebarOpen: false,
    commandPaletteOpen: false,
    globalLoading: false,
    toasts: []
  }),

  getters: {
    resolvedTheme: (state) => {
      if (state.theme === 'dark' || state.theme === 'light') {
        return state.theme
      }

      return getSystemTheme()
    }
  },

  actions: {
    applyTheme() {
      document.documentElement.classList.toggle('dark', this.resolvedTheme === 'dark')
    },

    initTheme() {
      this.applyTheme()

      if (this.theme === 'system' && window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
          if (this.theme === 'system') {
            this.applyTheme()
          }
        })
      }
    },

    setTheme(theme) {
      this.theme = theme
      localStorage.setItem(THEME_KEY, theme)
      this.applyTheme()
    },

    toggleTheme() {
      this.setTheme(this.resolvedTheme === 'dark' ? 'light' : 'dark')
    },

    openSidebar() {
      this.sidebarOpen = true
    },

    closeSidebar() {
      this.sidebarOpen = false
    },

    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },

    openCommandPalette() {
      this.commandPaletteOpen = true
    },

    closeCommandPalette() {
      this.commandPaletteOpen = false
    },

    toggleCommandPalette() {
      this.commandPaletteOpen = !this.commandPaletteOpen
    },

    pushToast(toast) {
      const id = Date.now() + Math.random()
      const item = {
        id,
        type: toast.type || 'info',
        title: toast.title || '',
        message: toast.message || '',
        duration: typeof toast.duration === 'number' ? toast.duration : 4000
      }

      this.toasts.push(item)

      if (item.duration > 0) {
        setTimeout(() => {
          this.removeToast(id)
        }, item.duration)
      }

      return id
    },

    removeToast(id) {
      this.toasts = this.toasts.filter((toast) => toast.id !== id)
    }
  }
})
