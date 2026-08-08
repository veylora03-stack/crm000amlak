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
    filters: { search: '', stage: '', agent: '', status: '' },
    // برای undo
    lastMove: null,
    undoTimeout: null
  }),

  getters: {
    activePipelines: (state) => state.pipelines.filter((p) => p.is_active),
    
    selectedPipeline: (state) => {
      return state.pipelines.find(p => String(p.public_id) === String(state.selectedPipelineId))
    },
    
    stagesBySelectedPipeline: (state) => {
      if (!state.selectedPipelineId) return []
      return state.stages
        .filter((s) => String(s.pipeline) === String(state.selectedPipelineId))
        .sort((a, b) => a.sort_order - b.sort_order)
    },
    
    dealsByStage: (state) => {
      return (stageId) => state.deals.filter((d) => 
        String(d.stage) === String(stageId) && 
        !d.is_deleted &&
        (state.filters.status === '' || d.status === state.filters.status)
      )
    },
    
    stageStats: (state) => {
      return (stageId) => {
        const deals = state.deals.filter(d => String(d.stage) === String(stageId) && !d.is_deleted)
        return {
          count: deals.length,
          total: deals.reduce((sum, d) => sum + (d.amount || 0), 0)
        }
      }
    }
  },

  actions: {
    selectPipeline(pipelineId) {
      this.selectedPipelineId = pipelineId
    },

    async fetchPipelines() {
      this.loading = true
      try {
        const response = await salesApi.pipelines.list()
        this.pipelines = response.data || []
        if (!this.selectedPipelineId && this.pipelines.length > 0) {
          this.selectedPipelineId = this.pipelines[0].public_id
        }
      } catch (error) {
        this.error = 'دریافت پایپ‌لاین‌ها با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async fetchStages() {
      try {
        const response = await salesApi.stages.list()
        this.stages = response.data || []
      } catch (error) {
        this.error = 'دریافت Stageها با مشکل مواجه شد.'
      }
    },

    async fetchDeals() {
      this.loading = true
      try {
        const params = { ...this.filters }
        Object.keys(params).forEach(k => { if (!params[k]) delete params[k] })
        const response = await salesApi.deals.list(params)
        this.deals = response.data || []
      } catch (error) {
        this.error = 'دریافت معاملات با مشکل مواجه شد.'
      } finally {
        this.loading = false
      }
    },

    async createDeal(payload) {
      try {
        const response = await salesApi.deals.create(payload)
        await this.fetchDeals()
        return response.data || response
      } catch (error) {
        this.error = 'ذخیره معامله با مشکل مواجه شد.'
        return null
      }
    },

    async updateDeal(id, payload) {
      try {
        const response = await salesApi.deals.partialUpdate(id, payload)
        return response.data || response
      } catch (error) {
        this.error = 'ویرایش معامله با مشکل مواجه شد.'
        return null
      }
    },

    // Optimistic move with undo
    optimisticMoveDeal(dealId, newStageId) {
      const dealIndex = this.deals.findIndex(d => String(d.public_id) === String(dealId))
      if (dealIndex === -1) return null
      
      const deal = this.deals[dealIndex]
      const oldStageId = deal.stage
      
      // Optimistic update
      this.deals[dealIndex] = { ...deal, stage: newStageId }
      
      // Save for undo
      this.lastMove = {
        dealId,
        oldStageId,
        newStageId,
        timestamp: Date.now()
      }
      
      return oldStageId
    },

    async moveDeal(dealId, newStageId) {
      const oldStageId = this.optimisticMoveDeal(dealId, newStageId)
      if (!oldStageId) return false
      
      // Clear previous undo timeout
      if (this.undoTimeout) clearTimeout(this.undoTimeout)
      
      try {
        await salesApi.deals.move(dealId, newStageId)
        
        // Set undo timeout (5 seconds)
        this.undoTimeout = setTimeout(() => {
          this.lastMove = null
        }, 5000)
        
        return true
      } catch (error) {
        // Revert on error
        this.revertMove(dealId, oldStageId)
        this.error = 'جابجایی معامله با مشکل مواجه شد.'
        return false
      }
    },

    async undoLastMove() {
      if (!this.lastMove) return false
      
      const { dealId, oldStageId } = this.lastMove
      
      try {
        await salesApi.deals.move(dealId, oldStageId)
        this.revertMove(dealId, oldStageId)
        this.lastMove = null
        if (this.undoTimeout) {
          clearTimeout(this.undoTimeout)
          this.undoTimeout = null
        }
        return true
      } catch (error) {
        this.error = 'برگرداندن معامله با مشکل مواجه شد.'
        return false
      }
    },

    revertMove(dealId, stageId) {
      const dealIndex = this.deals.findIndex(d => String(d.public_id) === String(dealId))
      if (dealIndex !== -1) {
        this.deals[dealIndex] = { ...this.deals[dealIndex], stage: stageId }
      }
    },

    async deleteDeal(id) {
      try {
        await salesApi.deals.remove(id)
        await this.fetchDeals()
        return true
      } catch (error) {
        this.error = 'حذف معامله با مشکل مواجه شد.'
        return false
      }
    }
  }
})
