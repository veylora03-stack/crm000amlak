<template>
  <section class="card p-4">
    <div v-if="loading" class="space-y-3">
      <div
        v-for="index in 8"
        :key="index"
        class="h-10 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="error"
      class="flex flex-col items-center justify-center gap-3 py-12 text-center"
    >
      <p class="text-danger-600 dark:text-danger-400">
        دریافت گزارش با مشکل مواجه شد.
      </p>
      <button type="button" class="btn-primary" @click="$emit('retry')">
        تلاش مجدد
      </button>
    </div>

    <div
      v-else-if="rows.length === 0"
      class="flex flex-col items-center justify-center gap-3 py-12 text-center"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        با فیلترهای انتخاب‌شده داده‌ای یافت نشد.
      </p>
    </div>

    <div v-else class="max-h-[600px] overflow-auto rounded-md border border-border-light dark:border-border-dark">
      <table class="w-full min-w-[900px] border-collapse text-sm">
        <thead class="sticky top-0 z-sticky">
          <tr class="bg-secondary-100 text-right text-text-secondary-light dark:bg-secondary-800 dark:text-text-secondary-dark">
            <th
              v-for="column in columns"
              :key="column.key"
              class="cursor-pointer p-3 font-semibold"
              @click="toggleSort(column.key)"
            >
              <span class="inline-flex items-center gap-1">
                {{ column.label }}
                <span v-if="sortKey === column.key" aria-hidden="true">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </span>
            </th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="(row, rowIndex) in sortedRows"
            :key="rowIndex"
            class="border-t border-border-light bg-surface-light hover:bg-secondary-100 dark:border-border-dark dark:bg-surface-dark dark:hover:bg-secondary-800"
          >
            <td
              v-for="column in columns"
              :key="column.key"
              class="p-3"
            >
              {{ formatCell(row[column.key]) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  rows: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

defineEmits(['retry'])

const sortKey = ref('')
const sortDirection = ref('asc')

function toggleSort(key) {
  if (sortKey.value !== key) {
    sortKey.value = key
    sortDirection.value = 'asc'
    return
  }

  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
}

const sortedRows = computed(() => {
  if (!sortKey.value) {
    return props.rows
  }

  const key = sortKey.value
  const direction = sortDirection.value === 'asc' ? 1 : -1

  return [...props.rows].sort((a, b) => {
    const firstValue = a[key]
    const secondValue = b[key]

    if (typeof firstValue === 'number' && typeof secondValue === 'number') {
      return (firstValue - secondValue) * direction
    }

    const firstText = String(firstValue ?? '')
    const secondText = String(secondValue ?? '')

    return firstText.localeCompare(secondText, 'fa') * direction
  })
})

function formatCell(value) {
  if (value === null || value === undefined || value === '') {
    return '-'
  }

  return value
}
</script>
