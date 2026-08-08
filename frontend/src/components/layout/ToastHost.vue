<template>
  <div
    class="fixed bottom-4 left-4 z-toast flex w-full max-w-sm flex-col gap-2 px-4"
    aria-live="polite"
  >
    <div
      v-for="toast in ui.toasts"
      :key="toast.id"
      :class="[
        'card flex items-start justify-between gap-3 border-r-4 p-4',
        typeClasses(toast.type)
      ]"
      role="status"
    >
      <div>
        <p class="font-semibold text-text-primary-light dark:text-text-primary-dark">
          {{ toast.title }}
        </p>
        <p
          v-if="toast.message"
          class="mt-1 text-sm text-text-secondary-light dark:text-text-secondary-dark"
        >
          {{ toast.message }}
        </p>
      </div>

      <button
        type="button"
        class="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-text-secondary-light hover:bg-secondary-100 dark:text-text-secondary-dark dark:hover:bg-secondary-800"
        aria-label="بستن پیام"
        @click="ui.removeToast(toast.id)"
      >
        ×
      </button>
    </div>
  </div>
</template>

<script setup>
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

function typeClasses(type) {
  if (type === 'success') {
    return 'border-success-500 bg-success-50 dark:bg-success-900/20'
  }

  if (type === 'warning') {
    return 'border-warning-500 bg-warning-50 dark:bg-warning-900/20'
  }

  if (type === 'error') {
    return 'border-danger-500 bg-danger-50 dark:bg-danger-900/20'
  }

  return 'border-info-500 bg-info-50 dark:bg-info-900/20'
}
</script>
