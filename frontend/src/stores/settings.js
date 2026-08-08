import { defineStore } from 'pinia'
import { settingsApi, usersApi } from '@/api'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    loading: false,
    error: null,
    settings: {},
    users: [],
    lookups: {
      propertyTypes: [],
      listingTypes: [],
      clientStatuses: [
        { id: 1, title: 'New', is_active: true },
        { id: 2, title: 'Contacted', is_active: true },
        { id: 3, title: 'Qualified', is_active: true },
        { id: 4, title: 'Unqualified', is_active: true },
        { id: 5, title: 'Negotiating', is_active: true },
        { id: 6, title: 'Won', is_active: true },
        { id: 7, title: 'Lost', is_active: true },
        { id: 8, title: 'Archived', is_active: true }
      ],
      customerTypes: [],
      leadSources: [],
      propertyStatuses: [
        { id: 1, title: 'Draft', is_active: true },
        { id: 2, title: 'Published', is_active: true },
        { id: 3, title: 'Reserved', is_active: true },
        { id: 4, title: 'Sold', is_active: true },
        { id: 5, title: 'Rented', is_active: true },
        { id: 6, title: 'Expired', is_active: true },
        { id: 7, title: 'Archived', is_active: true }
      ],
      interactionTypes: [
        { id: 1, title: 'تماس تلفنی', value: 'call', is_active: true },
        { id: 2, title: 'جلسه حضوری', value: 'meeting', is_active: true },
        { id: 3, title: 'ایمیل', value: 'email', is_active: true },
        { id: 4, title: 'پیام داخلی', value: 'message', is_active: true },
        { id: 5, title: 'یادداشت', value: 'note', is_active: true },
        { id: 6, title: 'بازدید ملک', value: 'visit', is_active: true },
        { id: 7, title: 'ارسال فایل', value: 'file', is_active: true },
        { id: 8, title: 'سایر', value: 'other', is_active: true }
      ],
      taskPriorities: [
        { id: 1, title: 'Low', is_active: true },
        { id: 2, title: 'Medium', is_active: true },
        { id: 3, title: 'High', is_active: true },
        { id: 4, title: 'Urgent', is_active: true }
      ],
      taskStatuses: [
        { id: 1, title: 'Todo', is_active: true },
        { id: 2, title: 'In Progress', is_active: true },
        { id: 3, title: 'Done', is_active: true },
        { id: 4, title: 'Cancelled', is_active: true }
      ],
      amenities: [],
      lostReasons: [],
      wonReasons: []
    }
  }),

  actions: {
    async fetchSettings() {
      this.loading = true
      this.error = null
      try {
        const response = await settingsApi.get()
        this.settings = response.data || response
      } catch (error) {
        this.error = 'دریافت تنظیمات با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async updateSettings(payload) {
      this.loading = true
      this.error = null
      try {
        const response = await settingsApi.update(payload)
        this.settings = { ...this.settings, ...(response.data || response) }
        return true
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ذخیره تنظیمات با مشکل مواجه شد.'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchUsers() {
      this.loading = true
      this.error = null
      try {
        const response = await usersApi.list()
        this.users = response.data || []
      } catch (error) {
        this.error = 'دریافت کاربران با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async createUser(payload) {
      this.loading = true
      this.error = null
      try {
        const response = await usersApi.create(payload)
        await this.fetchUsers()
        return response.data || response
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ایجاد کاربر با مشکل مواجه شد.'
        return null
      } finally {
        this.loading = false
      }
    },

    async updateUser(id, payload) {
      this.loading = true
      this.error = null
      try {
        const response = await usersApi.partialUpdate(id, payload)
        await this.fetchUsers()
        return response.data || response
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ویرایش کاربر با مشکل مواجه شد.'
        return null
      } finally {
        this.loading = false
      }
    },

    async toggleUserActive(id) {
      const user = this.users.find(u => String(u.public_id) === String(id))
      if (!user) return false

      try {
        if (user.is_active) {
          await usersApi.deactivate(id)
        } else {
          await usersApi.activate(id)
        }
        await this.fetchUsers()
        return true
      } catch (error) {
        this.error = 'تغییر وضعیت کاربر با مشکل مواجه شد.'
        return false
      }
    }
  }
})
