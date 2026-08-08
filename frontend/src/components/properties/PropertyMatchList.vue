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
      v-else-if="matches.length === 0"
      class="flex flex-col items-center justify-center gap-3 rounded-md border border-dashed border-border-light py-14 text-center dark:border-border-dark"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        هنوز تطابق مناسبی یافت نشده است.
      </p>
    </div>

    <div v-else class="grid gap-4 md:grid-cols-2">
      <article
        v-for="match in matches"
        :key="match.id"
        class="rounded-md border border-border-light bg-surface-light p-4 dark:border-border-dark dark:bg-surface-dark"
      >
        <div class="flex items-center justify-between gap-2">
          <h3 class="font-medium text-text-primary-light dark:text-text-primary-dark">
            {{ match.client_name }}
          </h3>
          <span class="text-sm font-bold text-primary-600 dark:text-primary-400">
            {{ match.score }}٪ تطابق
          </span>
        </div>

        <div class="mt-3 h-2 rounded-full bg-secondary-100 dark:bg-secondary-800">
          <div
            class="h-2 rounded-full bg-primary-600 dark:bg-primary-400"
            :style="{ width: match.score + '%' }"
          ></div>
        </div>

        <div class="mt-3 flex flex-wrap gap-2">
          <span
            v-for="field in match.matched_fields"
            :key="field"
            class="rounded-full bg-secondary-100 px-2 py-1 text-xs text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300"
          >
            {{ field }}
          </span>
        </div>

        <button
          type="button"
          class="btn-secondary mt-4"
          @click="$emit('view-client', match.client_id)"
        >
          مشاهده مشتری
        </button>
      </article>
    </div>
  </section>
</template>

<script setup>
defineProps({
  matches: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['view-client'])
</script>
