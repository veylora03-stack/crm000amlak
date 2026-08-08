<template>
  <section>
    <form class="mb-6" @submit.prevent="submit">
      <label for="new-note" class="label-base">افزودن یادداشت سریع</label>
      <textarea
        id="new-note"
        v-model="body"
        rows="3"
        class="input-base"
        placeholder="یادداشت خود را بنویسید..."
      ></textarea>
      <p v-if="error" class="error-text">{{ error }}</p>

      <button type="submit" class="btn-primary mt-3">
        ثبت یادداشت
      </button>
    </form>

    <div v-if="loading" class="space-y-3">
      <div
        v-for="index in 3"
        :key="index"
        class="h-14 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="notes.length === 0"
      class="py-8 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark"
    >
      یادداشتی ثبت نشده است.
    </div>

    <ul v-else class="space-y-3">
      <li
        v-for="note in notes"
        :key="note.id"
        class="rounded-md border border-border-light bg-surface-light p-4 dark:border-border-dark dark:bg-surface-dark"
      >
        <p class="text-sm text-text-primary-light dark:text-text-primary-dark">
          {{ note.body }}
        </p>
        <p class="mt-2 text-xs text-text-secondary-light dark:text-text-secondary-dark">
          {{ note.user || 'کاربر' }} — {{ formatDateTime(note.occurred_at) }}
        </p>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { formatDateTime } from '@/utils/format'

defineProps({
  notes: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['add'])

const body = ref('')
const error = ref('')

function submit() {
  if (!body.value.trim()) {
    error.value = 'متن یادداشت الزامی است.'
    return
  }

  error.value = ''
  emit('add', body.value.trim())
  body.value = ''
}
</script>
