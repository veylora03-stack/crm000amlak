<template>
  <section class="card p-5">
    <div class="mb-4 flex items-center justify-between gap-2">
      <h3 class="text-sm font-black">{{ title }}</h3>
      <slot name="actions" />
    </div>

    <div v-if="loading" class="skeleton h-64" aria-label="در حال بارگذاری نمودار"></div>

    <div v-else-if="error" class="flex h-64 flex-col items-center justify-center gap-3 text-center">
      <p class="text-sm font-semibold text-danger-600 dark:text-danger-400">نمودار بارگذاری نشد.</p>
      <button type="button" class="btn-secondary" @click="$emit('retry')">تلاش مجدد</button>
    </div>

    <div v-else-if="empty" class="flex h-64 flex-col items-center justify-center gap-2 text-center text-text-secondary-light dark:text-text-secondary-dark">
      <span class="text-3xl" aria-hidden="true">📭</span>
      <p class="text-sm font-semibold">داده‌ای برای نمایش وجود ندارد.</p>
    </div>

    <VueApexCharts v-else :type="type" :height="height" :options="options" :series="series" />
  </section>
</template>

<script setup>
const VueApexCharts = () => import('vue3-apexcharts').then(m => m.default)

defineProps({
  title: { type: String, required: true },
  type: { type: String, default: 'line' },
  height: { type: Number, default: 280 },
  loading: { type: Boolean, default: false },
  error: { type: Boolean, default: false },
  empty: { type: Boolean, default: false },
  options: { type: Object, default: () => ({}) },
  series: { type: Array, default: () => [] }
})

defineEmits(['retry'])
</script>

