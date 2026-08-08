<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-bold">تاریخچه فعالیت‌ها</h3>
      <button class="btn-secondary btn-sm">
        <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        فعالیت جدید
      </button>
    </div>

    <ol class="relative space-y-4 pr-4 before:absolute before:bottom-0 before:right-[7px] before:top-0 before:w-0.5 before:bg-gradient-to-b before:from-app-border before:to-transparent dark:before:from-app-border-dark">
      <li v-for="activity in activities" :key="activity.id" class="relative">
        <span
          class="absolute -right-[13px] flex h-5 w-5 items-center justify-center rounded-full border-2 text-[10px]"
          :class="getActivityClass(activity.type)"
        >
          {{ getActivityIcon(activity.type) }}
        </span>
        <div class="rounded-lg border border-app-border p-3 dark:border-app-border-dark">
          <div class="flex items-start justify-between gap-2">
            <div>
              <p class="text-sm font-semibold">{{ activity.title }}</p>
              <p class="mt-0.5 text-xs text-base-500">{{ activity.description }}</p>
            </div>
            <span class="text-[11px] text-base-400 whitespace-nowrap" dir="ltr">
              {{ formatRelative(activity.date) }}
            </span>
          </div>
        </div>
      </li>
    </ol>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useJalaaliDate } from '@/composables/useJalaaliDate'

const props = defineProps({
  clientId: { type: String, required: true }
})

const { formatRelative } = useJalaaliDate()

const activities = ref([
  { id: 1, type: 'call', title: 'تماس تلفنی', description: 'بررسی نیازها و بودجه', date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000) },
  { id: 2, type: 'meeting', title: 'جلسه حضوری', description: 'بازدید از ملک', date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000) },
  { id: 3, type: 'email', title: 'ایمیل', description: 'ارسال لیست املاک', date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) },
  { id: 4, type: 'deal', title: 'معامله جدید', description: 'آپارتمان سعادت‌آباد', date: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000) }
])

function getActivityIcon(type) {
  const icons = { call: '📞', meeting: '👥', email: '✉️', deal: '💼', note: '📝' }
  return icons[type] || '📋'
}

function getActivityClass(type) {
  const classes = {
    call: 'border-brand-500 bg-brand-500/10',
    meeting: 'border-accent-500 bg-accent-500/10',
    email: 'border-success-500 bg-success-500/10',
    deal: 'border-warning-500 bg-warning-500/10',
    note: 'border-base-500 bg-base-500/10'
  }
  return classes[type] || classes.note
}
</script>
