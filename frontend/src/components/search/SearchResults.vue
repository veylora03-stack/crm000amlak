<template>
  <div class="space-y-4">
    <div v-if="loading" class="space-y-3">
      <div
        v-for="index in 4"
        :key="index"
        class="h-12 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="hasSearched && !hasResults"
      class="py-8 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark"
    >
      نتیجه‌ای یافت نشد.
    </div>

    <template v-else-if="hasResults">
      <section v-if="clientResults.length > 0">
        <h4 class="mb-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark">
          مشتریان
        </h4>
        <ul class="space-y-1">
          <li v-for="client in clientResults" :key="client.id">
            <button
              type="button"
              class="w-full rounded-md px-3 py-2 text-right text-sm transition duration-normal ease-out hover:bg-secondary-100 dark:hover:bg-secondary-800"
              @click="$emit('select', { type: 'client', item: client })"
            >
              <span class="block font-medium">{{ client.full_name }}</span>
              <span class="mt-0.5 block text-xs text-text-secondary-light dark:text-text-secondary-dark" dir="ltr">
                {{ client.phone }}
              </span>
            </button>
          </li>
        </ul>
      </section>

      <section v-if="propertyResults.length > 0">
        <h4 class="mb-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark">
          املاک
        </h4>
        <ul class="space-y-1">
          <li v-for="property in propertyResults" :key="property.id">
            <button
              type="button"
              class="w-full rounded-md px-3 py-2 text-right text-sm transition duration-normal ease-out hover:bg-secondary-100 dark:hover:bg-secondary-800"
              @click="$emit('select', { type: 'property', item: property })"
            >
              <span class="block font-medium">{{ property.title }}</span>
              <span class="mt-0.5 block text-xs text-text-secondary-light dark:text-text-secondary-dark">
                {{ property.code }} — {{ property.city }}
              </span>
            </button>
          </li>
        </ul>
      </section>

      <section v-if="dealResults.length > 0">
        <h4 class="mb-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark">
          معاملات
        </h4>
        <ul class="space-y-1">
          <li v-for="deal in dealResults" :key="deal.id">
            <button
              type="button"
              class="w-full rounded-md px-3 py-2 text-right text-sm transition duration-normal ease-out hover:bg-secondary-100 dark:hover:bg-secondary-800"
              @click="$emit('select', { type: 'deal', item: deal })"
            >
              <span class="block font-medium">{{ deal.title }}</span>
              <span class="mt-0.5 block text-xs text-text-secondary-light dark:text-text-secondary-dark">
                {{ deal.client_name }} — {{ deal.agent }}
              </span>
            </button>
          </li>
        </ul>
      </section>

      <section v-if="taskResults.length > 0">
        <h4 class="mb-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark">
          وظایف
        </h4>
        <ul class="space-y-1">
          <li v-for="task in taskResults" :key="task.id">
            <button
              type="button"
              class="w-full rounded-md px-3 py-2 text-right text-sm transition duration-normal ease-out hover:bg-secondary-100 dark:hover:bg-secondary-800"
              @click="$emit('select', { type: 'task', item: task })"
            >
              <span class="block font-medium">{{ task.title }}</span>
              <span class="mt-0.5 block text-xs text-text-secondary-light dark:text-text-secondary-dark">
                {{ task.assigned_user }} — {{ task.status }}
              </span>
            </button>
          </li>
        </ul>
      </section>
    </template>

    <div
      v-else
      class="py-8 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark"
    >
      برای جستجو در مشتریان، املاک، معاملات و وظایف تایپ کنید.
    </div>
  </div>
</template>

<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  hasSearched: {
    type: Boolean,
    default: false
  },
  hasResults: {
    type: Boolean,
    default: false
  },
  clientResults: {
    type: Array,
    default: () => []
  },
  propertyResults: {
    type: Array,
    default: () => []
  },
  dealResults: {
    type: Array,
    default: () => []
  },
  taskResults: {
    type: Array,
    default: () => []
  }
})

defineEmits(['select'])
</script>
