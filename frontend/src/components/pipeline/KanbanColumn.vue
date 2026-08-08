<template>
  <section class="w-80 shrink-0 rounded-lg border border-border-light bg-secondary-100 p-3 dark:border-border-dark dark:bg-secondary-800">
    <header class="mb-3 flex items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <span class="h-3 w-3 rounded-full" :style="{ backgroundColor: stage.color }" aria-hidden="true"></span>
        <h3 class="text-sm font-semibold text-text-primary-light dark:text-text-primary-dark">
          {{ stage.name }}
        </h3>
        <span class="rounded-full bg-secondary-200 px-2 py-1 text-xs text-secondary-700 dark:bg-secondary-700 dark:text-secondary-200">
          {{ deals.length }}
        </span>
      </div>

      <span class="text-xs text-text-secondary-light dark:text-text-secondary-dark">
        {{ formatCurrency(total) }}
      </span>
    </header>

    <draggable
      :list="deals"
      item-key="id"
      group="deals"
      :animation="150"
      ghost-class="opacity-50"
      class="min-h-16 space-y-2"
      @change="$emit('drag-change', $event)"
    >
      <template #item="{ element }">
        <DealCard :deal="element" @click="$emit('open-deal', element)" />
      </template>
    </draggable>

    <div
      v-if="deals.length === 0"
      class="rounded-md border border-dashed border-border-light p-3 text-center text-xs text-text-secondary-light dark:border-border-dark dark:text-text-secondary-dark"
    >
      Deal به این مرحله اضافه نشده است.
    </div>

    <button type="button" class="btn-secondary mt-3 w-full" @click="$emit('quick-add', stage)">
      افزودن Deal
    </button>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import draggable from 'vuedraggable'
import { formatCurrency } from '@/utils/format'
import DealCard from '@/components/pipeline/DealCard.vue'

const props = defineProps({
  stage: {
    type: Object,
    required: true
  },
  deals: {
    type: Array,
    required: true
  }
})

defineEmits(['open-deal', 'quick-add', 'drag-change'])

const total = computed(() => {
  return props.deals.reduce((sum, deal) => {
    return sum + Number(deal.amount || 0)
  }, 0)
})
</script>
