import { defineStore } from 'pinia'
import { notificationsApi } from '@/api'

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),

  getters: {
    unreadCount: (state) => state.items.filter((item) => !item.is_read).length
  },

  actions: {
    async fetchNotifications() {
      this.loading = true
      this.error = null
      try {
        const response = await notificationsApi.list()
        this.items = response.data || []
      } catch (error) {
        this.error = 'دریافت نوتیفیکیشن‌ها با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async markRead(id) {
      try {
        const response = await notificationsApi.markRead(id)
        const index = this.items.findIndex(i => String(i.public_id) === String(id))
        if (index !== -1) {
          this.items[index].is_read = true
        }
        return response
      } catch (error) {
        this.error = 'خوانده‌شدن نوتیفیکیشن با مشکل مواجه شد.'
        return false
      }
    },

    async markAllRead() {
      try {
        await notificationsApi.markAllRead()
        this.items = this.items.map(item => ({ ...item, is_read: true }))
        return true
      } catch (error) {
        this.error = 'خوانده‌شدن همه نوتیفیکیشن‌ها با مشکل مواجه شد.'
        return false
      }
    }
  }
})
