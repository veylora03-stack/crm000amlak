<template>
  <section>
    <div v-if="loading" class="space-y-3">
      <div
        v-for="index in 4"
        :key="index"
        class="h-16 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="items.length === 0"
      class="flex flex-col items-center justify-center gap-3 py-10 text-center"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        هنوز تعاملی ثبت نشده است.
      </p>
    </div>

    <ol v-else class="relative space-y-4 border-r border-border-light pr-4 dark:border-border-dark">
      <li
        v-for="item in items"
        :key="item.id"
        class="relative rounded-md border border-border-light bg-surface-light p-4 dark:border-border-dark dark:bg-surface-dark"
      >
        <span
          class="absolute -right-[41px] top-4 flex h-8 w-8 items-center justify-center rounded-full border border-border-light bg-surface-light text-sm dark:border-border-dark dark:bg-surface-dark"
          aria-hidden="true"
        >
          {{ icon(item.interaction_type) }}
        </span>

        <div class="flex flex-wrap items-center justify-between gap-2">
          <p class="font-medium text-text-primary-light dark:text-text-primary-dark">
            {{ item.title }}
          </p>
          <p class="text-xs text-text-secondary-light dark:text-text-secondary-dark">
            {{ formatDateTime(item.occurred_at) }}
          </p>
        </div>

        <p class="mt-2 text-sm text-text-secondary-light dark:text-text-secondary-dark">
          {{ item.body }}
        </p>

        <div class="mt-3 flex flex-wrap items-center gap-2 text-xs">
          <span class="rounded-full bg-secondary-100 px-2 py-1 text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300">
            {{ item.user || 'کاربر' }}
          </span>

          <span
            v-if="item.needs_followup"
            class="rounded-full bg-warning-50 px-2 py-1 text-warning-700 dark:bg-warning-900/20 dark:text-warning-400"
          >
            پیگیری: {{ formatDate(item.followup_at) }}
          </span>

          <span
            v-if="item.duration_minutes"
            class="rounded-full bg-secondary-100 px-2 py-1 text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300"
          >
            مدت: {{ item.duration_minutes }} دقیقه
          </span>
        </div>
      </li>
    </ol>
  </section>
</template>

<script setup>
import { formatDate, formatDateTime } from '@/utils/format'

defineProps({
  items: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

function icon(type) {
  if (type === 'call') {
    return '📞'
  }

  if (type === 'meeting') {
    return '🤝'
  }

  if (type === 'email') {
    return '✉️'
  }

  if (type === 'message') {
    return '💬'
  }

  if (type === 'note') {
    return '📝'
  }

  if (type === 'visit') {
    return '🏠'
  }

  if (type === 'file') {
    return '📄'
  }

  return '📌'
}
</script>
