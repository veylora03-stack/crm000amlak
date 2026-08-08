<template>
  <div class="flex flex-col items-center justify-between gap-3 md:flex-row">
    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark">
      {{ formatNumber(total) }} رکورد — صفحه {{ formatNumber(page) }} از {{ formatNumber(totalPages) }}
    </p>

    <div class="flex items-center gap-2">
      <button
        type="button"
        class="btn-secondary"
        :disabled="page <= 1 || loading"
        @click="$emit('change', page - 1)"
      >
        قبلی
      </button>

      <button
        type="button"
        class="btn-secondary"
        :disabled="page >= totalPages || loading"
        @click="$emit('change', page + 1)"
      >
        بعدی
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatNumber } from '@/utils/format'

const props = defineProps({
  page: {
    type: Number,
    required: true
  },
  pageSize: {
    type: Number,
    default: 20
  },
  total: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['change'])

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(props.total / props.pageSize))
})
</script>
