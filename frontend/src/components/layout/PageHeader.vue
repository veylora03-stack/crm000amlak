<template>
  <div class="mb-6">
    <Breadcrumbs v-if="breadcrumbs.length" :items="breadcrumbs" />

    <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-text-primary-light dark:text-text-primary-dark">
          {{ title }}
        </h1>
        <p
          v-if="description"
          class="mt-1 text-sm text-text-secondary-light dark:text-text-secondary-dark"
        >
          {{ description }}
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-2">
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import Breadcrumbs from '@/components/layout/Breadcrumbs.vue'

defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  breadcrumbs: {
    type: Array,
    default: () => []
  }
})
</script>
