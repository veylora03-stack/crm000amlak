<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-bold">یادداشت‌ها</h3>
      <button class="btn-secondary btn-sm">
        <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        یادداشت جدید
      </button>
    </div>

    <div v-if="notes.length === 0" class="flex flex-col items-center justify-center py-12 text-center">
      <div class="mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-base-100 dark:bg-base-800">
        <svg class="h-7 w-7 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <p class="text-sm font-semibold">یادداشتی وجود ندارد</p>
      <p class="mt-1 text-xs text-base-500">هنوز یادداشتی برای این مشتری ثبت نشده است</p>
    </div>

    <div v-else class="space-y-3">
      <div v-for="note in notes" :key="note.id" class="rounded-lg border border-app-border p-4 dark:border-app-border-dark">
        <div class="flex items-start justify-between gap-3">
          <p class="text-sm">{{ note.content }}</p>
          <button class="btn-icon btn-ghost" @click="deleteNote(note.id)">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
        <div class="mt-3 flex items-center gap-2 text-xs text-base-500">
          <span>{{ note.author }}</span>
          <span>•</span>
          <span dir="ltr">{{ formatDate(note.date) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useJalaaliDate } from '@/composables/useJalaaliDate'

const props = defineProps({
  clientId: { type: String, required: true }
})

const { formatDate } = useJalaaliDate()

const notes = ref([
  { id: 1, content: 'مشتری به دنبال آپارتمان ۲ خوابه در منطقه ۱ است. بودجه حداکثر ۳ میلیارد تومان.', author: 'علی رضایی', date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000) },
  { id: 2, content: 'تماس تلفنی انجام شد. مشتری علاقه‌مند به بازدید از ملک کد ۱۲۳۴ است.', author: 'مدیر سیستم', date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000) }
])

function deleteNote(noteId) {
  // TODO: Delete note
}
</script>
