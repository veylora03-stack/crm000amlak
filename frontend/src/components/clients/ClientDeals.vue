<template>
  <section>
    <div v-if="loading" class="space-y-3">
      <div
        v-for="index in 3"
        :key="index"
        class="h-16 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="deals.length === 0"
      class="flex flex-col items-center justify-center gap-3 py-10 text-center"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        معامله‌ای برای این مشتری ثبت نشده است.
      </p>
      <button type="button" class="btn-primary" @click="$emit('create')">
        ایجاد Deal
      </button>
    </div>

    <div v-else class="grid gap-4 md:grid-cols-2">
      <article
        v-for="deal in deals"
        :key="deal.id"
        class="rounded-md border border-border-light bg-surface-light p-4 dark:border-border-dark dark:bg-surface-dark"
      >
        <div class="flex items-start justify-between gap-2">
          <h3 class="font-medium text-text-primary-light dark:text-text-primary-dark">
            {{ deal.title }}
          </h3>
          <span
            class="rounded-full bg-secondary-100 px-2 py-1 text-xs text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300"
          >
            {{ deal.stage }}
          </span>
        </div>

        <dl class="mt-3 space-y-2 text-sm">
          <div class="flex items-center justify-between gap-2">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">مبلغ</dt>
            <dd class="font-medium">{{ formatCurrency(deal.amount) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-2">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">وضعیت</dt>
            <dd class="font-medium">{{ deal.status }}</dd>
          </div>

          <div class="flex items-center justify-between gap-2">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">تاریخ ایجاد</dt>
            <dd class="font-medium">{{ formatDate(deal.created_at) }}</dd>
          </div>
        </dl>
      </article>
    </div>
  </section>
</template>

<script setup>
import { formatDate, formatCurrency } from '@/utils/format'

defineProps({
  deals: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['create'])
</script>
