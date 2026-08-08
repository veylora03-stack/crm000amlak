<template>
  <section class="card p-4">
    <div v-if="loading" class="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      <div
        v-for="index in 8"
        :key="index"
        class="h-28 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="days.length === 0"
      class="py-10 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark"
    >
      وظیفه‌ای در این نما وجود ندارد.
    </div>

    <div v-else class="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      <article
        v-for="day in days"
        :key="day.key"
        :class="[
          'rounded-md border p-3',
          day.isToday
            ? 'border-primary-500 bg-primary-50 dark:border-primary-400 dark:bg-primary-900/10'
            : 'border-border-light bg-surface-light dark:border-border-dark dark:bg-surface-dark'
        ]"
      >
        <header class="mb-2 flex items-center justify-between gap-2">
          <h3 class="text-sm font-semibold">{{ day.label }}</h3>
          <span class="text-xs text-text-secondary-light dark:text-text-secondary-dark">
            {{ day.tasks.length }} وظیفه
          </span>
        </header>

        <div v-if="day.tasks.length === 0" class="rounded-md border border-dashed border-border-light p-2 text-center text-xs text-text-secondary-light dark:border-border-dark dark:text-text-secondary-dark">
          وظیفه‌ای ندارد
        </div>

        <ul v-else class="space-y-2">
          <li v-for="task in day.tasks" :key="task.id">
            <button
              type="button"
              :class="[
                'w-full rounded-md border px-2 py-1 text-right text-xs transition duration-normal ease-out',
                isOverdue(task)
                  ? 'border-danger-300 bg-danger-50 text-danger-700 hover:bg-danger-100 dark:border-danger-900 dark:bg-danger-900/20 dark:text-danger-400'
                  : 'border-border-light bg-secondary-100 text-text-primary-light hover:bg-secondary-200 dark:border-border-dark dark:bg-secondary-800 dark:text-text-primary-dark dark:hover:bg-secondary-700'
              ]"
              @click="$emit('task-click', task)"
            >
              <span class="block truncate font-medium">{{ task.title }}</span>
              <span class="mt-1 block text-text-secondary-light dark:text-text-secondary-dark">
                {{ task.assigned_user || 'بدون مسئول' }} — {{ task.due_time || 'بدون ساعت' }}
              </span>
            </button>
          </li>
        </ul>
      </article>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => []
  },
  view: {
    type: String,
    default: 'week'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['task-click'])

function toLocalKey(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function todayKey() {
  return toLocalKey(new Date())
}

function formatDateLabel(date, options) {
  return new Intl.DateTimeFormat('fa-IR', options).format(date)
}

function tasksForDate(dateKey) {
  return props.tasks.filter((task) => {
    return task.due_date === dateKey
  })
}

const days = computed(() => {
  const currentTodayKey = todayKey()

  if (props.view === 'week') {
    return Array.from({ length: 7 }, (_, index) => {
      const date = new Date()
      date.setDate(date.getDate() + index)

      const dateKey = toLocalKey(date)

      return {
        key: dateKey,
        label: formatDateLabel(date, {
          weekday: 'long',
          day: 'numeric',
          month: 'long'
        }),
        isToday: dateKey === currentTodayKey,
        tasks: tasksForDate(dateKey)
      }
    })
  }

  if (props.view === 'month') {
    const now = new Date()
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1)
    const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate()

    return Array.from({ length: daysInMonth }, (_, index) => {
      const date = new Date(now.getFullYear(), now.getMonth(), index + 1)
      const dateKey = toLocalKey(date)

      return {
        key: dateKey,
        label: formatDateLabel(date, {
          day: 'numeric',
          month: 'long',
          weekday: 'short'
        }),
        isToday: dateKey === currentTodayKey,
        tasks: tasksForDate(dateKey)
      }
    })
  }

  return []
})

function isOverdue(task) {
  if (!task.due_date) {
    return false
  }

  return task.due_date < todayKey() && task.status !== 'Done' && task.status !== 'Cancelled'
}
</script>
