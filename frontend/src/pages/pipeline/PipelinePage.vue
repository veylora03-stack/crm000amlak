<template>
  <AppLayout>
    <div class="page-container">
      <!-- Hero Header -->
      <header class="mb-6">
        <div class="relative overflow-hidden rounded-2xl border border-app-border bg-gradient-to-br from-brand-500/5 via-accent-500/5 to-transparent p-6 dark:border-app-border-dark">
          <div class="pointer-events-none absolute -top-20 -right-20 h-64 w-64 rounded-full bg-brand-500/15 blur-3xl"></div>
          <div class="pointer-events-none absolute -bottom-20 -left-20 h-64 w-64 rounded-full bg-accent-500/10 blur-3xl"></div>
          
          <div class="relative flex flex-wrap items-center justify-between gap-4">
            <div>
              <h1 class="text-2xl font-bold tracking-tight sm:text-3xl">
                <span class="gradient-text-premium">پایپ‌لاین فروش</span>
              </h1>
              <p class="mt-1 text-sm text-base-500 dark:text-base-400">
                مدیریت <span class="font-semibold">{{ totalDeals }}</span> معامله فعال با ارزش 
                <span class="font-semibold tabular-nums" dir="ltr">{{ formatAmount(totalValue) }}</span>
              </p>
            </div>
            <div class="flex items-center gap-2">
              <button class="btn-secondary" @click="loadPipeline">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" :class="{ 'animate-spin': loading }">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span class="hidden sm:inline">به‌روزرسانی</span>
              </button>
              <button class="btn-brand" @click="openCreateModal">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <span>معامله جدید</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Pipeline Selector -->
      <div class="mb-4 flex items-center justify-between gap-4">
        <div class="flex items-center gap-2 overflow-x-auto">
          <button
            v-for="pipeline in dealsStore.activePipelines"
            :key="pipeline.public_id"
            :class="[
              'flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-semibold transition-all whitespace-nowrap',
              String(dealsStore.selectedPipelineId) === String(pipeline.public_id)
                ? 'border-brand-500 bg-brand-500 text-white shadow-glow-sm'
                : 'border-app-border bg-app-panel text-base-700 hover:border-base-300 dark:border-app-border-dark dark:text-base-300 dark:hover:border-base-700'
            ]"
            @click="dealsStore.selectPipeline(pipeline.public_id)"
          >
            {{ pipeline.name }}
            <span v-if="String(dealsStore.selectedPipelineId) === String(pipeline.public_id)" class="rounded-full bg-white/20 px-1.5 py-0.5 text-[10px] font-bold">
              {{ pipelineDealsCount }}
            </span>
          </button>
        </div>

        <div class="hidden items-center gap-2 sm:flex">
          <button class="btn-ghost btn-sm">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            تنظیمات
          </button>
        </div>
      </div>

      <!-- Kanban Board -->
      <div v-if="loading" class="flex gap-4 overflow-x-auto pb-4">
        <div v-for="i in 4" :key="i" class="w-[320px] flex-shrink-0 rounded-2xl border border-app-border bg-base-50/50 p-4 dark:border-app-border-dark">
          <div class="skeleton mb-3 h-6 w-24"></div>
          <div class="skeleton mb-2 h-3 w-16"></div>
          <div class="skeleton mb-2 h-32 w-full"></div>
          <div class="skeleton mb-2 h-32 w-full"></div>
        </div>
      </div>

      <div v-else class="flex gap-4 overflow-x-auto pb-4">
        <KanbanColumn
          v-for="stage in dealsStore.stagesBySelectedPipeline"
          :key="stage.public_id"
          :stage="stage"
          :deals="dealsStore.dealsByStage(stage.public_id)"
          :stats="dealsStore.stageStats(stage.public_id)"
          @drop="handleDrop"
          @add-deal="openCreateModal"
          @deal-click="openDealDetail"
        />
      </div>

      <!-- Undo Toast -->
      <Teleport to="body">
        <transition name="slide-up">
          <div
            v-if="dealsStore.lastMove"
            class="fixed bottom-6 left-1/2 z-toast flex -translate-x-1/2 items-center gap-3 rounded-xl border border-app-border bg-app-panel px-4 py-3 shadow-xl dark:border-app-border-dark"
          >
            <span class="text-sm font-medium">معامله جابجا شد</span>
            <button
              class="btn-secondary btn-sm"
              @click="handleUndo"
            >
              برگرداندن
            </button>
          </div>
        </transition>
      </Teleport>
    </div>
  </AppLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDealsStore } from '@/stores/deals'
import { useUiStore } from '@/stores/ui'
import AppLayout from '@/layouts/AppLayout.vue'
import KanbanColumn from '@/components/pipeline/KanbanColumn.vue'

const router = useRouter()
const dealsStore = useDealsStore()
const ui = useUiStore()

const loading = computed(() => dealsStore.loading)

const pipelineDealsCount = computed(() => dealsStore.deals.length)

const totalDeals = computed(() => dealsStore.deals.filter(d => !d.is_deleted).length)

const totalValue = computed(() => 
  dealsStore.deals
    .filter(d => !d.is_deleted)
    .reduce((sum, d) => sum + (d.amount || 0), 0)
)

onMounted(async () => {
  await loadPipeline()
})

async function loadPipeline() {
  await Promise.all([
    dealsStore.fetchPipelines(),
    dealsStore.fetchStages(),
    dealsStore.fetchDeals()
  ])
}

async function handleDrop(dropResult, targetStage) {
  const { removedIndex, addedIndex, payload } = dropResult
  if (!payload || removedIndex === null || addedIndex === null) return
  
  // فقط وقتی stage تغییر کرده API call کن
  const currentStageId = payload.stage
  const newStageId = targetStage.public_id
  
  if (String(currentStageId) === String(newStageId)) return
  
  const success = await dealsStore.moveDeal(payload.public_id, newStageId)
  
  if (success) {
    ui.pushToast({ 
      type: 'success', 
      title: 'معامله جابجا شد',
      message: `«${payload.title}» به ${targetStage.name} منتقل شد`
    })
  } else {
    ui.pushToast({ 
      type: 'error', 
      title: 'خطا در جابجایی',
      message: dealsStore.error
    })
  }
}

async function handleUndo() {
  const success = await dealsStore.undoLastMove()
  if (success) {
    ui.pushToast({ type: 'success', title: 'معامله برگردانده شد' })
  } else {
    ui.pushToast({ type: 'error', title: dealsStore.error })
  }
}

function openCreateModal() {
  ui.pushToast({ type: 'info', title: 'Modal معامله جدید در حال توسعه است' })
}

function openDealDetail(deal) {
  ui.pushToast({ type: 'info', title: `باز کردن ${deal.title}` })
}

function formatAmount(amount) {
  if (!amount) return '—'
  if (amount >= 1e12) return (amount / 1e12).toFixed(1) + 'T'
  if (amount >= 1e9) return (amount / 1e9).toFixed(1) + 'B'
  if (amount >= 1e6) return (amount / 1e6).toFixed(1) + 'M'
  return amount.toLocaleString()
}
</script>

<style scoped>
.gradient-text-premium {
  background: linear-gradient(135deg, #10b981 0%, #06b6d4 50%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}
</style>
