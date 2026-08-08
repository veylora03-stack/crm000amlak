<template>
  <component
    :is="to ? 'RouterLink' : 'div'"
    :to="to || undefined"
    class="ultra-kpi-card group relative overflow-hidden rounded-2xl border border-app-border bg-app-panel p-5 transition-all duration-300 hover:border-base-300 hover:shadow-xl dark:border-app-border-dark dark:hover:border-base-700"
  >
    <div class="pointer-events-none absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-brand-500/0 opacity-0 transition-opacity duration-300 group-hover:opacity-100" aria-hidden="true"></div>

    <div class="relative flex items-start justify-between gap-3">
      <div class="min-w-0 flex-1">
        <div class="flex items-center gap-2">
          <span class="truncate text-[11px] font-semibold uppercase tracking-wide text-base-500 dark:text-base-400">
            {{ title }}
          </span>
          <span v-if="badge" :class="['badge flex-shrink-0', badgeVariant]">{{ badge }}</span>
        </div>

        <p class="mt-2.5 min-w-0 overflow-hidden text-ellipsis whitespace-nowrap text-2xl font-bold tabular-nums text-base-900 dark:text-base-50 sm:text-3xl" dir="ltr">
          <CountUp :end-val="numericValue" :duration="1.5" :prefix="prefix" :suffix="suffix" />
        </p>

        <div class="mt-2.5 flex flex-wrap items-center gap-2">
          <div v-if="change" :class="changeClasses" class="flex items-center gap-1 text-xs">
            <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="changeTone !== 'danger'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
            <span class="font-semibold tabular-nums">{{ change }}</span>
          </div>

          <Sparkline
            v-if="sparklineData && sparklineData.length > 1"
            :data="sparklineData"
            :color="sparklineColor"
            :width="56"
            :height="20"
            class="flex-shrink-0 opacity-60 transition-opacity group-hover:opacity-100"
          />
        </div>
      </div>

      <div
        class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl text-xl transition-transform duration-300 group-hover:scale-110"
        :class="iconBgClass"
        aria-hidden="true"
      >
        {{ icon }}
      </div>
    </div>

    <div v-if="progress !== null" class="mt-4">
      <div class="flex items-center justify-between text-xs text-base-500 dark:text-base-400">
        <span>پیشرفت</span>
        <span class="font-semibold tabular-nums" dir="ltr">{{ progress }}%</span>
      </div>
      <div class="mt-1.5 h-1.5 overflow-hidden rounded-full bg-base-200 dark:bg-base-800">
        <div
          class="h-full rounded-full bg-gradient-to-r transition-all duration-500"
          :class="progressColor"
          :style="{ width: Math.min(progress, 100) + '%' }"
        ></div>
      </div>
    </div>
  </component>
</template>

<script setup>
import { computed } from 'vue'
import CountUp from '@/components/ui/CountUp.vue'
import Sparkline from '@/components/ui/Sparkline.vue'

const props = defineProps({
  title: { type: String, required: true },
  value: { type: String, required: true },
  icon: { type: String, default: '📊' },
  change: { type: String, default: '' },
  changeTone: { type: String, default: 'success' },
  to: { type: String, default: '' },
  badge: { type: String, default: '' },
  badgeVariant: { type: String, default: 'badge-brand' },
  sparklineData: { type: Array, default: null },
  sparklineColor: { type: String, default: '#10b981' },
  progress: { type: Number, default: null },
  progressColor: { type: String, default: 'from-brand-500 to-accent-500' },
  prefix: { type: String, default: '' },
  suffix: { type: String, default: '' }
})

const numericValue = computed(() => {
  const cleaned = String(props.value).replace(/[^\d]/g, '')
  return parseInt(cleaned) || 0
})

const changeClasses = computed(() => {
  return props.changeTone === 'danger'
    ? 'text-danger-600 dark:text-danger-400'
    : 'text-success-600 dark:text-success-400'
})

const iconBgClass = computed(() => {
  const tones = {
    success: 'bg-success-500/10 text-success-600 dark:text-success-400',
    danger: 'bg-danger-500/10 text-danger-600 dark:text-danger-400',
    warning: 'bg-warning-500/10 text-warning-600 dark:text-warning-400',
    default: 'bg-base-500/10 text-base-600 dark:text-base-400'
  }
  return tones[props.changeTone] || tones.default
})
</script>

<style scoped>
.ultra-kpi-card {
  backdrop-filter: blur(8px);
  contain: layout style;
}

.ultra-kpi-card:hover {
  transform: translateY(-2px);
}
</style>
