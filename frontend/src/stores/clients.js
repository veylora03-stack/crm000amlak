import { defineStore } from 'pinia'
import { clientsApi } from '@/api'
import { handleApiError } from '@/api/errorHandler'

export const useClientsStore = defineStore('clients', {
  state: () => ({
    items: [],
    total: 0,
    page: 1,
    pageSize: 20,
    loading: false,
    error: null,
    filters: {
      search: '',
      status: '',
      customer_type: '',
      source: '',
      assigned_agent: ''
    },
    currentItem: null,
    timeline: [],
    deals: [],
    interactions: []
  }),

  getters: {
    hasFilters: (state) => Object.values(state.filters).some(Boolean)
  },

  actions: {
    setFilter(key, value) {
      this.filters[key] = value
      this.page = 1
    },

    resetFilters() {
      this.filters = { search: '', status: '', customer_type: '', source: '', assigned_agent: '' }
      this.page = 1
    },

    setPage(page) {
      this.page = page
    },

    async fetchClients() {
      this.loading = true
      this.error = null

      try {
        const params = { page: this.page, page_size: this.pageSize, ...this.filters }
        Object.keys(params).forEach(k => { if (!params[k]) delete params[k] })

        const response = await clientsApi.list(params)
        this.items = response.data || []
        this.total = response.meta?.total || this.items.length
      } catch (error) {
        handleApiError(error, 'خطا در دریافت مشتریان')
        this.error = 'خطا در دریافت مشتریان'
      } finally {
        this.loading = false
      }
    },

    async fetchClient(id) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.retrieve(id)
        this.currentItem = response.data || response
      } catch (error) {
        handleApiError(error, 'خطا در دریافت مشتریان')
        this.error = 'خطا در دریافت مشتریان'
      } finally {
        this.loading = false
      }
    },

    async createClient(payload) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.create(payload)
        await this.fetchClients()
        return response.data || response
      } catch (error) {
        handleApiError(error, 'خطا در دریافت مشتریان')
        this.error = 'خطا در دریافت مشتریان'
      } finally {
        this.loading = false
      }
    },

    async updateClient(id, payload) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.partialUpdate(id, payload)
        if (this.currentItem && this.currentItem.public_id === id) {
          this.currentItem = response.data || response
        }
        await this.fetchClients()
        return response.data || response
      } catch (error) {
        handleApiError(error, 'خطا در دریافت مشتریان')
        this.error = 'خطا در دریافت مشتریان'
      } finally {
        this.loading = false
      }
    },

    async deleteClient(id) {
      this.loading = true
      this.error = null
      try {
        await clientsApi.remove(id)
        await this.fetchClients()
        return true
      } catch (error) {
        handleApiError(error, 'خطا در دریافت مشتریان')
        this.error = 'خطا در دریافت مشتریان'
      } finally {
        this.loading = false
      }
    },

    async fetchTimeline(id) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.timeline(id)
        this.timeline = response.data || []
      } catch (error) {
        handleApiError(error, 'خطا در دریافت مشتریان')
        this.error = 'خطا در دریافت مشتریان'
      } finally {
        this.loading = false
      }
    },

    async fetchDeals(id) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.deals(id)
        this.deals = response.data || []
      } catch (error) {
        handleApiError(error, 'خطا در دریافت مشتریان')
        this.error = 'خطا در دریافت مشتریان'
      } finally {
        this.loading = false
      }
    },

    async fetchInteractions(id) {
      await this.fetchTimeline(id)
      this.interactions = this.timeline
    }
  }
})

