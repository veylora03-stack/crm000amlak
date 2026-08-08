<template>
  <AppLayout>
    <PageHeader title="نوتیفیکیشن‌ها" description="مشاهده و مدیریت نوتیفیکیشن‌های داخلی">
      <template #actions>
        <button
          type="button"
          class="btn-secondary"
          :disabled="notificationsStore.loading || notificationsStore.items.length === 0"
          @click="markAll"
        >
          علامت‌گذاری همه به‌عنوان خوانده‌شده
        </button>
      </template>
    </PageHeader>

    <section class="card mb-6 p-4">
      <div class="flex flex-wrap items-center gap-2">
        <button
          type="button"
          :class="[
            'rounded-md px-4 py-2 text-sm font-medium',
            filter === 'all'
              ? 'bg-primary-600 text-white'
              : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
          ]"
          @click="filter = 'all'"
        >
          همه
        </button>

        <button
          type="button"
          :class="[
            'rounded-md px-4 py-2 text-sm font-medium',
            filter === 'unread'
              ? 'bg-primary-600 text-white'
              : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
          ]"
          @click="filter = 'unread'"
        >
          خوانده‌نشده
        </button>

        <span class="mr-auto text-sm text-text-secondary-light dark:text-text-secondary-dark">
          {{ formatNumber(notificationsStore.unreadCount) }} نوتیفیکیشن خوانده‌نشده
        </span>
      </div>
    </section>

    <section class="card p-4">
      <div v-if="notificationsStore.loading" class="space-y-3">
        <div
          v-for="index in 6"
          :key="index"
          class="h-16 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
        ></div>
      </div>

      <div
        v-else-if="notificationsStore.error"
        class="flex flex-col items-center justify-center gap-3 py-12 text-center"
      >
        <p class="text-danger-600 dark:text-danger-400">
          دریافت نوتیفیکیشن‌ها با مشکل مواجه شد.
        </p>
        <button type="button" class="btn-primary" @click="retry">
          تلاش مجدد
        </button>
      </div>

      <div
        v-else-if="visibleNotifications.length === 0"
        class="flex flex-col items-center justify-center gap-3 py-12 text-center"
      >
        <p class="text-text-secondary-light dark:text-text-secondary-dark">
          نوتیفیکیشنی وجود ندارد.
        </p>
      </div>

      <ul v-else class="space-y-3">
        <li
          v-for="notification in visibleNotifications"
          :key="notification.id"
          :class="[
            'rounded-md border p-4 transition duration-normal ease-out',
            notification.is_read
              ? 'border-border-light bg-surface-light dark:border-border-dark dark:bg-surface-dark'
              : 'border-primary-200 bg-primary-50 dark:border-primary-900 dark:bg-primary-900/10'
          ]"
        >
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0">
              <p class="font-medium text-text-primary-light dark:text-text-primary-dark">
                {{ notification.title }}
              </p>

              <p class="mt-1 text-sm text-text-secondary-light dark:text-text-secondary-dark">
                {{ notification.body }}
              </p>

              <p class="mt-2 text-xs text-text-muted-light dark:text-text-muted-dark">
                {{ formatDateTime(notification.created_at) }}
              </p>
            </div>

            <div class="flex shrink-0 items-center gap-2">
              <span
                v-if="!notification.is_read"
                class="rounded-full bg-primary-600 px-2 py-1 text-xs font-medium text-white"
              >
                جدید
              </span>

              <button
                v-if="!notification.is_read"
                type="button"
                class="btn-secondary"
                @click="markRead(notification)"
              >
                خوانده شد
              </button>

              <button
                v-if="notification.payload && notification.payload.route"
                type="button"
                class="btn-primary"
                @click="goToNotification(notification)"
              >
                مشاهده
              </button>
            </div>
          </div>
        </li>
      </ul>
    </section>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationsStore } from '@/stores/notifications'
import { useUiStore } from '@/stores/ui'
import { formatDateTime, formatNumber } from '@/utils/format'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'

const notificationsStore = useNotificationsStore()
const ui = useUiStore()
const router = useRouter()

const filter = ref('all')

const visibleNotifications = computed(() => {
  if (filter.value === 'unread') {
    return notificationsStore.items.filter((notification) => !notification.is_read)
  }

  return notificationsStore.items
})

onMounted(() => {
  notificationsStore.fetchNotifications()
})

async function retry() {
  await notificationsStore.fetchNotifications()
}

async function markRead(notification) {
  const success = await notificationsStore.markRead(notification.id)

  if (success) {
    ui.pushToast({
      type: 'success',
      title: 'نوتیفیکیشن خوانده شد',
      message: notification.title
    })
  }
}

async function markAll() {
  const success = await notificationsStore.markAllRead()

  if (success) {
    ui.pushToast({
      type: 'success',
      title: 'همه نوتیفیکیشن‌ها خوانده شدند',
      message: 'وضعیت همه نوتیفیکیشن‌ها به خوانده‌شده تغییر کرد.'
    })
  }
}

function goToNotification(notification) {
  if (!notification.is_read) {
    notificationsStore.markRead(notification.id)
  }

  if (notification.payload && notification.payload.route) {
    router.push(notification.payload.route)
  }
}
</script>
