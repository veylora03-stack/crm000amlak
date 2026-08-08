<template>
  <div
    class="deal-card group relative overflow-hidden rounded-xl border border-app-border bg-app-panel p-4 transition-all duration-200 hover:-translate-y-0.5 hover:border-base-300 hover:shadow-lg dark:border-app-border-dark dark:hover:border-base-700"
    :class="{ 'opacity-60': isDragging }"
    @click="$emit('click', deal)"
  >
    <!-- Drag Handle -->
    <div class="absolute left-2 top-2 opacity-0 transition-opacity group-hover:opacity-100">
      <div class="flex h-6 w-6 items-center justify-center rounded text-base-400">
        <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
          <circle cx="9" cy="6" r="1.5" />
          <circle cx="15" cy="6" r="1.5" />
          <circle cx="9" cy="12" r="1.5" />
          <circle cx="15" cy="12" r="1.5" />
          <circle cx="9" cy="18" r="1.5" />
          <circle cx="15" cy="18" r="1.5" />
        </svg>
      </div>
    </div>

    <!-- Header: Title + Status -->
    <div class="mb-3 flex items-start justify-between gap-2">
      <h3 class="flex-1 text-sm font-bold leading-tight text-base-900 dark:text-base-50 line-clamp-2">
        {{ deal.title }}
      </h3>
      <span v-if="deal.probability" :class="['badge flex-shrink-0 text-[10px]', probabilityBadge(deal.probability)]" dir="ltr">
        {{ deal.probability }}%
      </span>
    </div>

    <!-- Client & Property -->
    <div class="mb-3 space-y-1.5">
      <div v-if="deal.client_name" class="flex items-center gap-2 text-xs text-base-600 dark:text-base-400">
        <svg class="h-3 w-3 flex-shrink-0 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span class="truncate">{{ deal.client_name }}</span>
      </div>
      <div v-if="deal.property_title" class="flex items-center gap-2 text-xs text-base-600 dark:text-base-400">
        <svg class="h-3 w-3 flex-shrink-0 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        <span class="truncate">{{ deal.property_title }}</span>
      </div>
    </div>

    <!-- Amount -->
    <div class="mb-3 rounded-lg bg-base-500/5 p-2.5">
      <p class="text-[10px] font-medium uppercase tracking-wider text-base-500">ارزش معامله</p>
      <p class="mt-0.5 text-base font-bold tabular-nums text-brand-600 dark:text-brand-400" dir="ltr">
        {{ formatAmount(deal.amount) }}
      </p>
    </div>

    <!-- Footer: Agent + Due Date -->
    <div class="flex items-center justify-between gap-2 border-t border-app-border pt-3 dark:border-app-border-dark">
      <div class="flex items-center gap-1.5">
        <div class="flex h-5 w-5 items-center justify-center rounded-full bg-gradient-to-br from-brand-500 to-accent-500 text-[9px] font-bold text-white">
          {{ getInitials(deal.agent_name) }}
        </div>
        <span class="text-[11px] text-base-600 dark:text-base-400">{{ deal.agent_name || 'بدون مسئول' }}</span>
      </div>
      <div v-if="deal.expected_close_date" class="flex items-center gap-1 text-[11px] text-base-500">
        <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span class="tabular-nums" dir="ltr">{{ formatDate(deal.expected_close_date) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  deal: { type: Object, required: true },
  isDragging: { type: Boolean, default: false }
})

defineEmits(['click'])

function formatAmount(amount) {
  if (!amount) return '—'
  if (amount >= 1e12) return (amount / 1e12).toFixed(1) + 'T'
  if (amount >= 1e9) return (amount / 1e9).toFixed(1) + 'B'
  if (amount >= 1e6) return (amount / 1e6).toFixed(1) + 'M'
  return amount.toLocaleString()
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    return new Intl.DateTimeFormat('fa-IR', { month: 'short', day: 'numeric' }).format(date)
  } catch {
    return dateStr
  }
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

function probabilityBadge(prob) {
  if (prob >= 70) return 'badge-success'
  if (prob >= 40) return 'badge-warning'
  return 'badge-danger'
}
</script>

<style scoped>
.deal-card {
  cursor: grab;
  user-select: none;
}

.deal-card:active {
  cursor: grabbing;
}
</style>
