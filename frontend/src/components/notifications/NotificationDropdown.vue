<template>
  <div ref="container" class="relative">
    <button
      type="button"
      class="relative inline-flex h-10 w-10 items-center justify-center rounded-md text-text-secondary-light hover:bg-secondary-100 dark:text-text-secondary-dark dark:hover:bg-secondary-800"
      aria-label="نوتیفیکیشن‌ها"
      :aria-expanded="open"
      @click="toggle"
    >
      🔔
      <span
        v-if="notificationsStore.unreadCount > 0"
        class="absolute -left-1 -top-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-danger-600 px-1 text-xs font-bold text-white"
      >
        {{ notificationsStore.unreadCount }}
      </span>
    </button>

    <div
      v-if="open"
      class="absolute left-0 z-dropdown mt-2 w-80 max-w-[calc(100vw-2rem)] rounded-lg border border-border-light bg-surface-light shadow-xl dark:border-border-dark dark:bg-surface-dark"
      role="dialog"
      aria-label="پنل نوتیفیکیشن‌ها"
    >
      <div class="flex items-center justify-between border-b border-border-light p-3 dark:border-border-dark">
        <p class="text-sm font-semibold">نوتیفیکیشن‌ها</p>

        <button
          type="button"
          class="text-xs font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
          @click="markAll"
        >
          خواندن همه
        </button>
      </div>

      <div v-if="notificationsStore.loading" class="space-y-2 p-3">
        <div
          v-for="index in 3"
          :key="index"
          class="h-14 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
        ></div>
      </div>

      <div
        v-else-if="notificationsStore.items.length === 0"
        class="p-6 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark"
      >
        نوتیفیکیشنی وجود ندارد.
      </div>

      <div v-else class="max-h-80 overflow-y-auto p-2">
        <button
          v-for="notification in notificationsStore.items.slice(0, 5)"
          :key="notification.id"
          type="button"
          class="w-full rounded-md p-3 text-right transition duration-normal ease-out hover:bg-secondary-100 dark:hover:bg-secondary-800"
          @click="openNotification(notification)"
        >
          <div class="flex items-start justify-between gap-2">
            <p class="text-sm font-medium text-text-primary-light dark:text-text-primary-dark">
              {{ notification.title }}
            </p>

            <span
              v-if="!notification.is_read"
              class="mt-1 h-2 w-2 shrink-0 rounded-full bg-primary-600"
              aria-hidden="true"
            ></span>
          </div>

          <p class="mt-1 line-clamp-2 text-xs text-text-secondary-light dark:text-text-secondary-dark">
            {{ notification.body }}
          </p>

          <p class="mt-2 text-xs text-text-muted-light dark:text-text-muted-dark">
            {{ formatDateTime(notification.created_at) }}
          </p>
        </button>
      </div>

      <div class="border-t border-border-light p-2 dark:border-border-dark">
        <RouterLink
          to="/notifications"
          class="block rounded-md px-3 py-2 text-center text-sm font-medium text-primary-600 hover:bg-primary-50 dark:text-primary-400 dark:hover:bg-primary-900/20"
          @click="close"
        >
          مشاهده همه نوتیفیکیشن‌ها
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationsStore } from '@/stores/notifications'
import { formatDateTime } from '@/utils/format'

const notificationsStore = useNotificationsStore()
const router = useRouter()

const open = ref(false)
const container = ref(null)

onMounted(() => {
  notificationsStore.fetchNotifications()
  document.addEventListener('click', onDocumentClick)
  document.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
})

function toggle() {
  open.value = !open.value
}

function close() {
  open.value = false
}

function onDocumentClick(event) {
  if (container.value && !container.value.contains(event.target)) {
    open.value = false
  }
}

function onKeydown(event) {
  if (event.key === 'Escape') {
    open.value = false
  }
}

function markAll() {
  notificationsStore.markAllRead()
}

function openNotification(notification) {
  if (!notification.is_read) {
    notificationsStore.markRead(notification.id)
  }

  if (notification.payload && notification.payload.route) {
    router.push(notification.payload.route)
  }

  close()
}
</script>
