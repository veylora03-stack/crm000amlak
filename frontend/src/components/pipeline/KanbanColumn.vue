<template>
  <div
    class="kanban-column flex h-full w-[320px] flex-shrink-0 flex-col rounded-2xl border border-app-border bg-base-50/50 dark:border-app-border-dark dark:bg-base-900/50"
    :style="{ '--stage-color': stage.color }"
  >
    <!-- Header -->
    <div class="relative flex items-center justify-between p-4 pb-3">
      <!-- Color indicator -->
      <div class="absolute inset-x-0 top-0 h-1 rounded-t-2xl" :style="{ backgroundColor: stage.color }"></div>

      <div class="flex min-w-0 items-center gap-2">
        <div class="h-2.5 w-2.5 flex-shrink-0 rounded-full shadow-sm" :style="{ backgroundColor: stage.color }"></div>
        <h3 class="truncate text-sm font-bold text-base-900 dark:text-base-50">{{ stage.name }}</h3>
        <span class="rounded-full bg-base-900 px-2 py-0.5 text-[10px] font-bold text-white dark:bg-base-50 dark:text-base-900">
          {{ stats.count }}
        </span>
      </div>

      <button
        type="button"
        class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg text-base-400 transition-colors hover:bg-base-200 hover:text-base-700 dark:hover:bg-base-800 dark:hover:text-base-200"
        @click="$emit('add-deal', stage)"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
    </div>

    <!-- Stats -->
    <div class="mx-4 mb-3 flex items-baseline gap-1">
      <span class="text-[11px] text-base-500">ارزش:</span>
      <span class="text-xs font-bold tabular-nums text-base-700 dark:text-base-300" dir="ltr">
        {{ formatAmount(stats.total) }}
      </span>
    </div>

    <!-- Drop Zone -->
    <Container
      group-name="kanban"
      :get-child-payload="getDealPayload"
      drag-handle-selector=".deal-card"
      @drop="onDrop"
      class="flex-1 overflow-y-auto px-3 pb-3"
    >
      <Draggable v-for="deal in deals" :key="deal.public_id">
        <DealCard
          :deal="deal"
          @click="$emit('deal-click', deal)"
        />
      </Draggable>

      <!-- Empty state -->
      <div v-if="deals.length === 0" class="flex h-32 flex-col items-center justify-center text-center">
        <div class="mb-2 flex h-10 w-10 items-center justify-center rounded-full bg-base-200 dark:bg-base-800">
          <svg class="h-5 w-5 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <p class="text-xs text-base-400">معامله‌ای نیست</p>
      </div>
    </Container>
  </div>
</template>

<script setup>
import { Container, Draggable } from 'vue-smooth-dnd'
import DealCard from './DealCard.vue'

const props = defineProps({
  stage: { type: Object, required: true },
  deals: { type: Array, default: () => [] },
  stats: { type: Object, default: () => ({ count: 0, total: 0 }) }
})

const emit = defineEmits(['drop', 'add-deal', 'deal-click'])

function getDealPayload(index) {
  return props.deals[index]
}

function onDrop(dropResult) {
  emit('drop', dropResult, props.stage)
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
.kanban-column {
  min-height: 400px;
  transition: border-color 0.2s;
}

.kanban-column:hover {
  border-color: color-mix(in srgb, var(--stage-color) 40%, transparent);
}
</style>
