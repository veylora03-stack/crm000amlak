<template>
  <AppLayout>
    <PageHeader title="وظایف" description="مدیریت وظایف، یادآورها و کارهای روزانه">
      <template #actions>
        <button type="button" class="btn-primary" @click="openCreateTask">
          افزودن وظیفه
        </button>
      </template>
    </PageHeader>

    <section class="card mb-6 p-4">
      <div class="flex flex-wrap items-center gap-2">
        <button
          type="button"
          :class="[
            'rounded-md px-4 py-2 text-sm font-medium',
            view === 'today'
              ? 'bg-primary-600 text-white'
              : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
          ]"
          @click="changeView('today')"
        >
          امروز
        </button>

        <button
          type="button"
          :class="[
            'rounded-md px-4 py-2 text-sm font-medium',
            view === 'week'
              ? 'bg-primary-600 text-white'
              : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
          ]"
          @click="changeView('week')"
        >
          هفته
        </button>

        <button
          type="button"
          :class="[
            'rounded-md px-4 py-2 text-sm font-medium',
            view === 'month'
              ? 'bg-primary-600 text-white'
              : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
          ]"
          @click="changeView('month')"
        >
          ماه
        </button>
      </div>
    </section>

    <TaskFilters
      v-model="filters"
      :agents="settingsStore.users"
      @apply="applyFilters"
      @reset="resetFilters"
    />

    <TasksList
      v-if="view === 'today'"
      :tasks="todayTasks"
      :loading="pageLoading || tasksStore.loading"
      :error="tasksStore.error"
      @complete="completeTask"
      @edit="openEditTask"
      @delete="confirmDeleteTask"
      @add="openCreateTask"
      @retry="applyFilters"
    />

    <TasksCalendar
      v-else
      :tasks="tasksStore.items"
      :view="view"
      :loading="pageLoading || tasksStore.loading"
      @task-click="openEditTask"
    />

    <TaskFormModal
      :open="showTaskForm"
      :initial="editingTask"
      :loading="savingTask"
      :agents="settingsStore.users"
      :clients="clientsStore.items"
      :deals="dealsStore.deals"
      :properties="propertiesStore.items"
      @close="closeTaskForm"
      @submit="saveTask"
    />

    <ConfirmModal
      :open="Boolean(deletingTask)"
      title="حذف وظیفه"
      :message="deleteMessage"
      confirm-label="حذف وظیفه"
      cancel-label="انصراف"
      danger
      :loading="deleting"
      @confirm="deleteTask"
      @cancel="deletingTask = null"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { useSettingsStore } from '@/stores/settings'
import { useClientsStore } from '@/stores/clients'
import { useDealsStore } from '@/stores/deals'
import { usePropertiesStore } from '@/stores/properties'
import { useUiStore } from '@/stores/ui'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'
import TaskFilters from '@/components/tasks/TaskFilters.vue'
import TasksList from '@/components/tasks/TasksList.vue'
import TasksCalendar from '@/components/tasks/TasksCalendar.vue'
import TaskFormModal from '@/components/tasks/TaskFormModal.vue'

const tasksStore = useTasksStore()
const settingsStore = useSettingsStore()
const clientsStore = useClientsStore()
const dealsStore = useDealsStore()
const propertiesStore = usePropertiesStore()
const ui = useUiStore()

const pageLoading = ref(true)
const view = ref('today')
const filters = ref({
  assigned_user: '',
  priority: '',
  status: ''
})

const showTaskForm = ref(false)
const editingTask = ref(null)
const savingTask = ref(false)
const deletingTask = ref(null)
const deleting = ref(false)

const deleteMessage = computed(() => {
  if (!deletingTask.value) {
    return ''
  }

  return `وظیفه «${deletingTask.value.title}» حذف می‌شود. آیا مطمئن هستید؟`
})

const todayTasks = computed(() => {
  const combined = [
    ...tasksStore.overdueTasks,
    ...tasksStore.todayTasks.filter((task) => {
      return !tasksStore.overdueTasks.some((overdueTask) => overdueTask.id === task.id)
    })
  ]

  return combined.sort((a, b) => {
    if (!a.due_time) {
      return 1
    }

    if (!b.due_time) {
      return -1
    }

    return a.due_time.localeCompare(b.due_time)
  })
})

onMounted(async () => {
  try {
    await Promise.all([
      tasksStore.fetchTasks(),
      settingsStore.fetchUsers(),
      clientsStore.fetchClients(),
      dealsStore.fetchDeals(),
      propertiesStore.fetchProperties()
    ])
  } finally {
    pageLoading.value = false
  }
})

function changeView(nextView) {
  view.value = nextView
  tasksStore.setView(nextView)
}

function applyFilters() {
  Object.entries(filters.value).forEach(([key, value]) => {
    tasksStore.setFilter(key, value)
  })

  tasksStore.fetchTasks()
}

function resetFilters() {
  filters.value = {
    assigned_user: '',
    priority: '',
    status: ''
  }

  tasksStore.resetFilters()
  tasksStore.fetchTasks()
}

function openCreateTask() {
  editingTask.value = null
  showTaskForm.value = true
}

function openEditTask(task) {
  editingTask.value = task
  showTaskForm.value = true
}

function closeTaskForm() {
  showTaskForm.value = false
  editingTask.value = null
}

async function saveTask(payload) {
  savingTask.value = true

  let result = null

  if (editingTask.value) {
    result = await tasksStore.updateTask(editingTask.value.id, payload)
  } else {
    result = await tasksStore.createTask(payload)
  }

  savingTask.value = false

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'وظیفه ذخیره شد',
      message: 'اطلاعات وظیفه با موفقیت ذخیره شد.'
    })

    closeTaskForm()
  } else {
    ui.pushToast({
      type: 'error',
      title: 'ذخیره وظیفه ناموفق بود',
      message: tasksStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

async function completeTask(task) {
  const result = await tasksStore.completeTask(task.id)

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'وظیفه انجام شد',
      message: `وظیفه «${task.title}» به‌عنوان انجام شده علامت‌گذاری شد.`
    })
  } else {
    ui.pushToast({
      type: 'error',
      title: 'تکمیل وظیفه ناموفق بود',
      message: tasksStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

function confirmDeleteTask(task) {
  deletingTask.value = task
}

async function deleteTask() {
  if (!deletingTask.value) {
    return
  }

  deleting.value = true

  const success = await tasksStore.deleteTask(deletingTask.value.id)

  deleting.value = false
  deletingTask.value = null

  if (success) {
    ui.pushToast({
      type: 'success',
      title: 'وظیفه حذف شد',
      message: 'وظیفه انتخاب‌شده حذف شد.'
    })
  } else {
    ui.pushToast({
      type: 'error',
      title: 'حذف وظیفه ناموفق بود',
      message: tasksStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}
</script>
