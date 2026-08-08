import { defineStore } from 'pinia'
import { tasksApi } from '@/api'

const today = new Date().toISOString().slice(0, 10)

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    items: [],
    total: 0,
    loading: false,
    error: null,
    view: 'today',
    filters: {
      assigned_user: '',
      priority: '',
      status: ''
    }
  }),

  getters: {
    todayTasks: (state) => {
      return state.items.filter((task) => task.due_date === today && task.status !== 'Cancelled')
    },
    overdueTasks: (state) => {
      return state.items.filter((task) => {
        return task.due_date && task.due_date < today && task.status !== 'Done' && task.status !== 'Cancelled'
      })
    }
  },

  actions: {
    setView(view) { this.view = view },
    setFilter(key, value) { this.filters[key] = value },
    resetFilters() { this.filters = { assigned_user: '', priority: '', status: '' } },

    async fetchTasks() {
      this.loading = true
      this.error = null
      try {
        const params = { ...this.filters }
        Object.keys(params).forEach(k => { if (!params[k]) delete params[k] })

        const response = await tasksApi.list(params)
        this.items = response.data || []
        this.total = response.meta?.total || this.items.length
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'دریافت وظایف با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async createTask(payload) {
      this.loading = true
      this.error = null
      try {
        const response = await tasksApi.create(payload)
        await this.fetchTasks()
        return response.data || response
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ذخیره وظیفه با مشکل مواجه شد.'
        return null
      } finally {
        this.loading = false
      }
    },

    async updateTask(id, payload) {
      this.loading = true
      this.error = null
      try {
        const response = await tasksApi.partialUpdate(id, payload)
        await this.fetchTasks()
        return response.data || response
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ویرایش وظیفه با مشکل مواجه شد.'
        return null
      } finally {
        this.loading = false
      }
    },

    async completeTask(id) {
      try {
        const response = await tasksApi.complete(id)
        await this.fetchTasks()
        return response.data || response
      } catch (error) {
        this.error = 'تکمیل وظیفه با مشکل مواجه شد.'
        return null
      }
    },

    async deleteTask(id) {
      this.loading = true
      this.error = null
      try {
        await tasksApi.remove(id)
        await this.fetchTasks()
        return true
      } catch (error) {
        this.error = 'حذف وظیفه با مشکل مواجه شد.'
        return false
      } finally {
        this.loading = false
      }
    }
  }
})
