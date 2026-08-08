<template>
  <!-- Skeleton Loading -->
  <div v-if="type === 'skeleton' && loading" class="loading-state-skeleton">
    <div v-for="i in count" :key="i" class="skeleton-item">
      <div class="skeleton skeleton-title"></div>
      <div class="skeleton skeleton-text"></div>
      <div class="skeleton skeleton-text w-2/3"></div>
    </div>
  </div>

  <!-- Spinner Loading -->
  <div v-else-if="type === 'spinner' && loading" class="loading-state-spinner flex items-center justify-center py-12">
    <div class="flex flex-col items-center gap-3">
      <svg class="animate-spin h-8 w-8 text-brand-600" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="text-sm text-base-500">{{ message || 'در حال بارگذاری...' }}</p>
    </div>
  </div>

  <!-- Empty State -->
  <div v-else-if="!loading && empty" class="loading-state-empty flex flex-col items-center justify-center py-16 text-center">
    <div class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-base-100 dark:bg-base-800">
      <svg class="h-8 w-8 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
    </div>
    <p class="text-base font-semibold text-base-700 dark:text-base-300">{{ emptyTitle || 'داده‌ای وجود ندارد' }}</p>
    <p class="mt-1 text-sm text-base-500">{{ emptyMessage || 'هنوز هیچ آیتمی اضافه نشده است' }}</p>
    <slot name="action" />
  </div>

  <!-- Error State -->
  <div v-else-if="error" class="loading-state-error flex flex-col items-center justify-center py-12 text-center">
    <div class="mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-danger-500/10">
      <svg class="h-7 w-7 text-danger-600 dark:text-danger-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    </div>
    <p class="text-sm font-semibold text-danger-700 dark:text-danger-400">{{ error }}</p>
    <button v-if="retryable" class="btn-secondary btn-sm mt-3" @click="$emit('retry')">
      تلاش مجدد
    </button>
  </div>

  <!-- Content -->
  <slot v-else />
</template>

<script setup>
defineProps({
  loading: { type: Boolean, default: false },
  error: { type: [String, null], default: null },
  empty: { type: Boolean, default: false },
  type: { type: String, default: 'skeleton', validator: v => ['skeleton', 'spinner'].includes(v) },
  count: { type: Number, default: 3 },
  message: { type: String, default: '' },
  emptyTitle: { type: String, default: '' },
  emptyMessage: { type: String, default: '' },
  retryable: { type: Boolean, default: true }
})

defineEmits(['retry'])
</script>

<style scoped>
.loading-state-skeleton {
  @apply space-y-4;
}

.skeleton-item {
  @apply space-y-2;
}

.skeleton {
  @apply animate-pulse rounded-md bg-base-200 dark:bg-base-800;
}

.skeleton-title {
  @apply h-4 w-1/3;
}

.skeleton-text {
  @apply h-3 w-full;
}
</style>
