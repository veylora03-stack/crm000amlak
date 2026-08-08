<template>
  <article
    class="card cursor-pointer p-3 transition duration-normal ease-out hover:shadow-md"
    @click="$emit('click')"
  >
    <div class="flex items-start justify-between gap-2">
      <h4 class="text-sm font-semibold text-text-primary-light dark:text-text-primary-dark">
        {{ deal.title }}
      </h4>
      <span class="shrink-0 text-xs text-text-secondary-light dark:text-text-secondary-dark">
        {{ formatDate(deal.expected_close_date) }}
      </span>
    </div>

    <p class="mt-1 text-xs text-text-secondary-light dark:text-text-secondary-dark">
      {{ deal.client_name || 'بدون مشتری' }}
    </p>

    <div class="mt-2 flex items-center justify-between gap-2 text-xs">
      <span class="font-medium text-primary-600 dark:text-primary-400">
        {{ formatCurrency(deal.amount) }}
      </span>
      <span class="text-text-secondary-light dark:text-text-secondary-dark">
        {{ deal.agent || '-' }}
      </span>
    </div>

    <div class="mt-2 flex flex-wrap gap-1">
      <span class="rounded-full bg-secondary-100 px-2 py-1 text-xs text-secondary-700 dark:bg-secondary-700 dark:text-secondary-200">
        {{ deal.status }}
      </span>

      <span
        v-if="deal.property_title"
        class="rounded-full bg-secondary-100 px-2 py-1 text-xs text-secondary-700 dark:bg-secondary-700 dark:text-secondary-200"
      >
        {{ deal.property_title }}
      </span>
    </div>
  </article>
</template>

<script setup>
import { formatDate, formatCurrency } from '@/utils/format'

defineProps({
  deal: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])
</script>
