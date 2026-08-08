import { defineStore } from 'pinia'
import { salesApi } from '@/api'

export const useDealsStore = defineStore('deals', {
  state: () => ({
    pipelines: [],
    stages: [],
    deals: [],
    selectedPipelineId: null,
    loading: false,
    error: null,
    filters: {
      search: '',
      stage: '',
      agent: '',
      status: ''
    }
  }),

  getters: {
    activePipelines: (state) => state.pipelines.filter((p) => p.is_active),
    stagesBySelectedPipeline: (state) => {
      const idStr = state.selectedPipelineId ? String(state.selectedPipelineId) : null
      return state.stages
        .filter((s) => idStr && String(s.pipeline) === idStr)
        .sort((a, b) => a.sort_order - b.sort_order)
    },
    dealsByStage: (state) => {
      return (stageId) => state.deals.filter((d) => String(d.stage) === String(stageId) && !d.is_deleted)
    }
  },

  actions: {
    selectPipeline(pipelineId) {
      this.selectedPipelineId = pipelineId
    },

    async fetchPipelines() {
      this.loading = true
      this.error = null
      try {
        const response = await salesApi.pipelines.list()
        this.pipelines = response.data || []
      } catch (error) {
        this.error = 'دریافت پایپ‌لاین‌ها با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async fetchStages() {
      this.loading = true
      this.error = null
      try {
        const response = await salesApi.stages.list()
        this.stages = response.data || []
      } catch (error) {
        this.error = 'دریافت Stageها با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async fetchDeals() {
      this.loading = true
      this.error = null
      try {
        const params = { ...this.filters }
        Object.keys(params).forEach(k => { if (!params[k]) delete params[k] })

        const response = await salesApi.deals.list(params)
        this.deals = response.data || []
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'دریافت معاملات با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async createDeal(payload) {
      this.loading = true
      this.error = null
      try {
        const response = await salesApi.deals.create(payload)
        await this.fetchDeals()
        return response.data || response
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ذخیره معامله با مشکل مواجه شد.'
        return null
      } finally {
        this.loading = false
      }
    },

    async updateDeal(id, payload) {
      this.loading = true
      this.error = null
      try {
        const response = await salesApi.deals.partialUpdate(id, payload)
        await this.fetchDeals()
        return response.data || response
      } catch (error) {
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'ویرایش معامله با مشکل مواجه شد.'
        return null
      } finally {
        this.loading = false
      }
    },

    async moveDeal(dealId, stageId) {
      // Optimistic update
      const dealIndex = this.deals.findIndex(d => String(d.public_id) === String(dealId))
      const previousStage = dealIndex !== -1 ? this.deals[dealIndex].stage : null
      
      if (dealIndex !== -1) {
        this.deals[dealIndex].stage = stageId
      }

      try {
        await salesApi.deals.move(dealId, stageId)
        return true
      } catch (error) {
        // Revert optimistic update
        if (dealIndex !== -1 && previousStage !== null) {
          this.deals[dealIndex].stage = previousStage
        }
        const errors = error?.response?.data?.errors || []
        this.error = errors.length > 0 ? errors[0].message : 'جابجایی معامله با مشکل مواجه شد.'
        return false
      }
    },

    async deleteDeal(id) {
      this.loading = true
      this.error = null
      try {
        await salesApi.deals.remove(id)
        await this.fetchDeals()
        return true
      } catch (error) {
        this.error = 'حذف معامله با مشکل مواجه شد.'
        return false
      } finally {
        this.loading = false
      }
    }
  }
})
