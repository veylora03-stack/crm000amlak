<template>
  <section class="card p-4">
    <div v-if="loading" class="space-y-3">
      <div
        v-for="index in 5"
        :key="index"
        class="h-12 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="error"
      class="flex flex-col items-center justify-center gap-3 py-12 text-center"
    >
      <p class="text-danger-600 dark:text-danger-400">
        دریافت وظایف با مشکل مواجه شد.
      </p>
      <button type="button" class="btn-primary" @click="$emit('retry')">
        تلاش مجدد
      </button>
    </div>

    <div
      v-else-if="tasks.length === 0"
      class="flex flex-col items-center justify-center gap-3 py-12 text-center"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        وظیفه‌ای برای نمایش وجود ندارد.
      </p>
      <button type="button" class="btn-primary" @click="$emit('add')">
        افزودن وظیفه
      </button>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full min-w-[900px] border-collapse text-sm">
        <thead>
          <tr class="border-b border-border-light text-right text-text-secondary-light dark:border-border-dark dark:text-text-secondary-dark">
            <th class="p-3 font-semibold">عنوان</th>
            <th class="p-3 font-semibold">مسئول</th>
            <th class="p-3 font-semibold">اولویت</th>
            <th class="p-3 font-semibold">وضعیت</th>
            <th class="p-3 font-semibold">سررسید</th>
            <th class="p-3 font-semibold">مرتبط با</th>
            <th class="p-3 font-semibold">اقدامات</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="task in tasks"
            :key="task.id"
            :class="[
              'border-b border-border-light transition duration-normal ease-out dark:border-border-dark',
              isOverdue(task)
                ? 'bg-danger-50 dark:bg-danger-900/10'
                : 'hover:bg-secondary-100 dark:hover:bg-secondary-800'
            ]"
          >
            <td class="p-3">
              <p class="font-medium">{{ task.title }}</p>
              <p v-if="task.description" class="mt-1 line-clamp-1 text-xs text-text-secondary-light dark:text-text-secondary-dark">
                {{ task.description }}
              </p>
            </td>
            <td class="p-3">{{ task.assigned_user || '-' }}</td>
            <td class="p-3">
              <span :class="['rounded-full px-2 py-1 text-xs font-medium', priorityClass(task.priority)]">
                {{ task.priority }}
              </span>
            </td>
            <td class="p-3">
              <span :class="['rounded-full px-2 py-1 text-xs font-medium', statusClass(task.status)]">
                {{ task.status }}
              </span>
            </td>
            <td class="p-3">
              <p>{{ formatDate(task.due_date) }}</p>
              <p v-if="task.due_time" class="mt-1 text-xs text-text-secondary-light dark:text-text-secondary-dark">
                ساعت: {{ task.due_time }}
              </p>
            </td>
            <td class="p-3 text-xs">
              <p v-if="task.client_id">مشتری: {{ task.client_id }}</p>
              <p v-if="task.deal_id">Deal: {{ task.deal_id }}</p>
              <p v-if="task.property_id">ملک: {{ task.property_id }}</p>
              <p v-if="!task.client_id && !task.deal_id && !task.property_id">-</p>
            </td>
            <td class="p-3">
              <div class="flex flex-wrap items-center gap-2">
                <button
                  v-if="task.status !== 'Done' && task.status !== 'Cancelled'"
                  type="button"
                  class="btn-secondary"
                  @click="$emit('complete', task)"
                >
                  انجام شد
                </button>

                <button type="button" class="btn-secondary" @click="$emit('edit', task)">
                  ویرایش
                </button>

                <button type="button" class="btn-danger" @click="$emit('delete', task)">
                  حذف
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { formatDate } from '@/utils/format'

defineProps({
  tasks: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

defineEmits(['complete', 'edit', 'delete', 'add', 'retry'])

function todayKey() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function isOverdue(task) {
  if (!task.due_date) {
    return false
  }

  return task.due_date < todayKey() && task.status !== 'Done' && task.status !== 'Cancelled'
}

function priorityClass(priority) {
  if (priority === 'Urgent') {
    return 'bg-danger-50 text-danger-700 dark:bg-danger-900/20 dark:text-danger-400'
  }

  if (priority === 'High') {
    return 'bg-warning-50 text-warning-700 dark:bg-warning-900/20 dark:text-warning-400'
  }

  if (priority === 'Medium') {
    return 'bg-info-50 text-info-700 dark:bg-info-900/20 dark:text-info-400'
  }

  return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300'
}

function statusClass(status) {
  if (status === 'Done') {
    return 'bg-success-50 text-success-700 dark:bg-success-900/20 dark:text-success-400'
  }

  if (status === 'Cancelled') {
    return 'bg-danger-50 text-danger-700 dark:bg-danger-900/20 dark:text-danger-400'
  }

  if (status === 'In Progress') {
    return 'bg-info-50 text-info-700 dark:bg-info-900/20 dark:text-info-400'
  }

  return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300'
}
</script>
