<template>
  <component
    :is="to ? 'RouterLink' : 'div'"
    :to="to || undefined"
    class="card card-interactive group relative overflow-hidden p-5"
  >
    <div class="flex items-start justify-between gap-3">
      <div class="flex-1">
        <p class="kpi-label">{{ title }}</p>
        <p class="kpi-value mt-2">{{ value }}</p>
        <div v-if="change" class="mt-2">
          <span :class="changeTone === 'danger' ? 'kpi-delta-down' : 'kpi-delta-up'">
            <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="changeTone !== 'danger'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
            {{ change }}
          </span>
        </div>
      </div>
      <div
        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-base-500/5 text-lg"
        aria-hidden="true"
      >
        {{ icon }}
      </div>
    </div>
  </component>
</template>

<script setup>
defineProps({
  title:      { type: String, required: true },
  value:      { type: String, required: true },
  icon:       { type: String, default: '📊' },
  change:     { type: String, default: '' },
  changeTone: { type: String, default: 'success' },
  to:         { type: String, default: '' }
})
</script>
