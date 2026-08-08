<template>
  <nav aria-label="مسیر صفحات" class="mb-2 text-sm text-text-secondary-light dark:text-text-secondary-dark">
    <ol class="flex flex-wrap items-center gap-1">
      <li
        v-for="(item, index) in items"
        :key="index"
        class="flex items-center gap-1"
      >
        <RouterLink
          v-if="item.to"
          :to="item.to"
          class="hover:text-primary-600 dark:hover:text-primary-400"
        >
          {{ item.label }}
        </RouterLink>

        <span v-else class="text-text-primary-light dark:text-text-primary-dark">
          {{ item.label }}
        </span>

        <span v-if="index < items.length - 1" aria-hidden="true">
          /
        </span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => []
  }
})
</script>
