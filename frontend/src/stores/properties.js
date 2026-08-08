import { defineStore } from 'pinia'
import { propertiesApi } from '@/api'

export const usePropertiesStore = defineStore('properties', {
  state: () => ({
    items: [],
    total: 0,
    page: 1,
    pageSize: 20,
    loading: false,
    error: null,
    filters: {
      search: '',
      property_type: '',
      listing_type: '',
      status: '',
      city: ''
    },
    currentItem: null,
    images: [],
    matches: []
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
      this.filters = { search: '', property_type: '', listing_type: '', status: '', city: '' }
      this.page = 1
    },

    setPage(page) {
      this.page = page
    },

    async fetchProperties() {
      this.loading = true
      this.error = null
      try {
        const params = { page: this.page, page_size: this.pageSize, ...this.filters }
        Object.keys(params).forEach(k => { if (!params[k]) delete params[k] })

        const response = await propertiesApi.list(params)
        this.items = response.data || []
        this.total = response.meta?.total || this.items.length
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'دریافت لیست املاک با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async fetchProperty(id) {
      this.loading = true
      this.error = null
      try {
        const response = await propertiesApi.retrieve(id)
        this.currentItem = response.data || response
        this.images = this.currentItem.images || []
      } catch (error) {
        this.currentItem = null
        this.images = []
        this.error = 'ملک مورد نظر یافت نشد.'
      } finally {
        this.loading = false
      }
    },

    async createProperty(payload) {
      this.loading = true
      this.error = null
      try {
        const response = await propertiesApi.create(payload)
        await this.fetchProperties()
        return response.data || response
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ذخیره ملک با مشکل مواجه شد.'
        return null
      } finally {
        this.loading = false
      }
    },

    async updateProperty(id, payload) {
      this.loading = true
      this.error = null
      try {
        const response = await propertiesApi.partialUpdate(id, payload)
        if (this.currentItem && this.currentItem.public_id === id) {
          this.currentItem = response.data || response
        }
        await this.fetchProperties()
        return response.data || response
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ویرایش ملک با مشکل مواجه شد.'
        return null
      } finally {
        this.loading = false
      }
    },

    async deleteProperty(id) {
      this.loading = true
      this.error = null
      try {
        await propertiesApi.remove(id)
        await this.fetchProperties()
        return true
      } catch (error) {
        this.error = 'حذف ملک با مشکل مواجه شد.'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchMatches(id) {
      this.loading = true
      this.error = null
      try {
        const response = await propertiesApi.matches(id)
        this.matches = response.data || []
      } catch (error) {
        this.error = 'دریافت Smart Match با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },
    
    async uploadImage(id, file, options) {
      try {
        const response = await propertiesApi.uploadImage(id, file, options)
        await this.fetchProperty(id)
        return response.data || response
      } catch (error) {
        this.error = 'آپلود تصویر با مشکل مواجه شد.'
        return null
      }
    },
    
    async publishProperty(id) {
      try {
        const response = await propertiesApi.publish(id)
        if (this.currentItem && this.currentItem.public_id === id) {
          this.currentItem = response.data || response
        }
        return response.data || response
      } catch (error) {
        this.error = 'انتشار ملک با مشکل مواجه شد.'
        return null
      }
    },
    
    async archiveProperty(id) {
      try {
        const response = await propertiesApi.archive(id)
        if (this.currentItem && this.currentItem.public_id === id) {
          this.currentItem = response.data || response
        }
        return response.data || response
      } catch (error) {
        this.error = 'آرشیو ملک با مشکل مواجه شد.'
        return null
      }
    }
  }
})
