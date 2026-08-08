<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-bold">معاملات مشتری</h3>
      <button class="btn-secondary btn-sm">
        <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        معامله جدید
      </button>
    </div>

    <div v-if="deals.length === 0" class="flex flex-col items-center justify-center py-12 text-center">
      <div class="mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-base-100 dark:bg-base-800">
        <svg class="h-7 w-7 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <p class="text-sm font-semibold">معامله‌ای وجود ندارد</p>
      <p class="mt-1 text-xs text-base-500">هنوز معامله‌ای برای این مشتری ثبت نشده است</p>
    </div>

    <div v-else class="space-y-3">
      <div v-for="deal in deals" :key="deal.id" class="rounded-lg border border-app-border p-4 transition-all hover:border-base-300 dark:border-app-border-dark dark:hover:border-base-700">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0 flex-1">
            <h4 class="font-semibold">{{ deal.title }}</h4>
            <p class="mt-1 text-xs text-base-500">{{ deal.property_title }}</p>
          </div>
          <span :class="['badge', dealStatusBadge(deal.status)]">{{ dealStatusLabel(deal.status) }}</span>
        </div>
        <div class="mt-3 flex items-center justify-between text-xs">
          <span class="text-base-500">ارزش:</span>
          <span class="font-bold tabular-nums text-brand-600" dir="ltr">{{ formatCurrency(deal.amount) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  clientId: { type: String, required: true }
})

const deals = ref([
  { id: 1, title: 'آپارتمان سعادت‌آباد', property_title: 'آپارتمان ۱۲۰ متری', status: 'Negotiating', amount: 2500000000 },
  { id: 2, title: 'ویلای لواسان', property_title: 'ویلای ۵۰۰ متری', status: 'Won', amount: 1800000000 }
])

function formatCurrency(amount) {
  if (!amount) return '—'
  if (amount >= 1e9) return (amount / 1e9).toFixed(1) + 'B'
  if (amount >= 1e6) return (amount / 1e6).toFixed(1) + 'M'
  return amount.toLocaleString()
}

function dealStatusBadge(status) {
  const map = {
    'New': 'badge-brand',
    'Negotiating': 'badge-warning',
    'Won': 'badge-success',
    'Lost': 'badge-danger'
  }
  return map[status] || 'badge-neutral'
}

function dealStatusLabel(status) {
  const map = {
    'New': 'جدید',
    'Negotiating': 'در حال مذاکره',
    'Won': 'برنده',
    'Lost': 'باخته'
  }
  return map[status] || status
}
</script>
