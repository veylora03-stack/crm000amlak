<template>
  <div
    v-if="ui.commandPaletteOpen"
    class="fixed inset-0 z-command-palette bg-black/50 p-4"
    @click.self="close"
  >
    <div class="mx-auto mt-20 w-full max-w-command-palette rounded-lg border border-border-light bg-surface-light shadow-xl dark:border-border-dark dark:bg-surface-dark">
      <div class="border-b border-border-light p-3 dark:border-border-dark">
        <input
          ref="inputRef"
          v-model="query"
          type="text"
          class="input-base"
          placeholder="جستجو یا فرمان... (Ctrl+K)"
          aria-label="جستجوی سراسری و فرمان‌ها"
          @input="onInput"
          @keydown="onKeydown"
        />
      </div>

      <div class="max-h-96 overflow-y-auto p-2">
        <div v-if="loading" class="space-y-2">
          <div
            v-for="index in 5"
            :key="index"
            class="h-10 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
          ></div>
        </div>

        <div
          v-else-if="flatItems.length === 0"
          class="py-10 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark"
        >
          نتیجه‌ای یافت نشد.
        </div>

        <ul v-else class="space-y-1">
          <li
            v-for="(item, index) in flatItems"
            :key="item.id"
          >
            <div
              v-if="shouldShowGroupHeader(index)"
              class="px-3 pb-1 pt-3 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark"
            >
              {{ item.group }}
            </div>

            <button
              type="button"
              :class="[
                'w-full rounded-md px-3 py-2 text-right transition duration-normal ease-out',
                activeIndex === index
                  ? 'bg-primary-50 dark:bg-primary-900/20'
                  : 'hover:bg-secondary-100 dark:hover:bg-secondary-800'
              ]"
              @click="selectItem(item)"
              @mouseenter="activeIndex = index"
            >
              <span class="block truncate text-sm font-medium text-text-primary-light dark:text-text-primary-dark">
                {{ item.title }}
              </span>

              <span
                v-if="item.subtitle"
                class="mt-0.5 block truncate text-xs text-text-secondary-light dark:text-text-secondary-dark"
              >
                {{ item.subtitle }}
              </span>
            </button>
          </li>
        </ul>
      </div>

      <div class="border-t border-border-light p-3 text-xs text-text-secondary-light dark:border-border-dark dark:text-text-secondary-dark">
        ↑↓ برای پیمایش — Enter برای انتخاب — Esc برای بستن
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUiStore } from '@/stores/ui'
import { useAuthStore } from '@/stores/auth'
import { debounce } from '@/utils/debounce'
import { useGlobalSearch } from '@/composables/useGlobalSearch'

const ui = useUiStore()
const auth = useAuthStore()
const router = useRouter()

const {
  loading,
  clientResults,
  propertyResults,
  dealResults,
  taskResults,
  search,
  clearSearch
} = useGlobalSearch()

const query = ref('')
const activeIndex = ref(0)
const inputRef = ref(null)

const baseCommands = computed(() => {
  const commands = []

  commands.push({
    id: 'command-dashboard',
    group: 'ناوبری',
    title: 'رفتن به داشبورد',
    subtitle: 'مشاهده KPIها و نمودارها',
    action: () => router.push('/dashboard')
  })

  commands.push({
    id: 'command-clients',
    group: 'ناوبری',
    title: 'رفتن به مشتریان',
    subtitle: 'مدیریت مشتریان و لیدها',
    action: () => router.push('/clients')
  })

  commands.push({
    id: 'command-properties',
    group: 'ناوبری',
    title: 'رفتن به املاک',
    subtitle: 'مدیریت فایل‌های املاک',
    action: () => router.push('/properties')
  })

  commands.push({
    id: 'command-pipeline',
    group: 'ناوبری',
    title: 'رفتن به پایپ‌لاین فروش',
    subtitle: 'مدیریت Dealها به‌صورت Kanban',
    action: () => router.push('/pipeline')
  })

  commands.push({
    id: 'command-deals',
    group: 'ناوبری',
    title: 'رفتن به معاملات',
    subtitle: 'لیست معاملات',
    action: () => router.push('/deals')
  })

  commands.push({
    id: 'command-tasks',
    group: 'ناوبری',
    title: 'رفتن به وظایف',
    subtitle: 'مدیریت وظایف و یادآورها',
    action: () => router.push('/tasks')
  })

  if (['Admin', 'Manager'].includes(auth.role)) {
    commands.push({
      id: 'command-reports',
      group: 'ناوبری',
      title: 'رفتن به گزارش‌ها',
      subtitle: 'گزارش‌گیری و خروجی',
      action: () => router.push('/reports')
    })
  }

  commands.push({
    id: 'command-notifications',
    group: 'ناوبری',
    title: 'رفتن به نوتیفیکیشن‌ها',
    subtitle: 'مشاهده نوتیفیکیشن‌های داخلی',
    action: () => router.push('/notifications')
  })

  commands.push({
    id: 'command-profile',
    group: 'ناوبری',
    title: 'رفتن به پروفایل',
    subtitle: 'مشاهده و ویرایش پروفایل',
    action: () => router.push('/profile')
  })

  if (auth.isAdmin) {
    commands.push({
      id: 'command-settings',
      group: 'ناوبری',
      title: 'رفتن به تنظیمات',
      subtitle: 'تنظیمات سیستم و مقادیر پایه',
      action: () => router.push('/settings')
    })

    commands.push({
      id: 'command-users',
      group: 'ناوبری',
      title: 'رفتن به کاربران',
      subtitle: 'مدیریت کاربران و نقش‌ها',
      action: () => router.push('/users')
    })
  }

  commands.push({
    id: 'command-toggle-theme',
    group: 'اقدامات',
    title: ui.resolvedTheme === 'dark' ? 'تغییر به حالت روشن' : 'تغییر به حالت تاریک',
    subtitle: 'تغییر تم نمایشی برنامه',
    action: () => ui.toggleTheme()
  })

  commands.push({
    id: 'command-logout',
    group: 'اقدامات',
    title: 'خروج از حساب کاربری',
    subtitle: 'پایان نشست فعلی',
    action: logout
  })

  return commands
})

const filteredCommands = computed(() => {
  const q = query.value.trim().toLowerCase()

  if (!q) {
    return baseCommands.value
  }

  return baseCommands.value.filter((command) => {
    return (
      command.title.toLowerCase().includes(q) ||
      command.subtitle.toLowerCase().includes(q) ||
      command.group.toLowerCase().includes(q)
    )
  })
})

const resultItems = computed(() => {
  if (!query.value.trim()) {
    return []
  }

  const items = []

  clientResults.value.forEach((client) => {
    items.push({
      id: `client-${client.id}`,
      group: 'مشتریان',
      title: client.full_name,
      subtitle: client.phone,
      action: () => router.push(`/clients/${client.id}`)
    })
  })

  propertyResults.value.forEach((property) => {
    items.push({
      id: `property-${property.id}`,
      group: 'املاک',
      title: property.title,
      subtitle: `${property.code} — ${property.city}`,
      action: () => router.push(`/properties/${property.id}`)
    })
  })

  dealResults.value.forEach((deal) => {
    items.push({
      id: `deal-${deal.id}`,
      group: 'معاملات',
      title: deal.title,
      subtitle: `${deal.client_name || 'بدون مشتری'} — ${deal.agent || 'بدون Agent'}`,
      action: () => router.push('/pipeline')
    })
  })

  taskResults.value.forEach((task) => {
    items.push({
      id: `task-${task.id}`,
      group: 'وظایف',
      title: task.title,
      subtitle: `${task.assigned_user || 'بدون مسئول'} — ${task.status}`,
      action: () => router.push('/tasks')
    })
  })

  return items
})

const flatItems = computed(() => {
  return [...filteredCommands.value, ...resultItems.value]
})

watch(flatItems, () => {
  activeIndex.value = 0
})

watch(
  () => ui.commandPaletteOpen,
  async (open) => {
    if (open) {
      query.value = ''
      clearSearch()
      activeIndex.value = 0

      await nextTick()
      inputRef.value?.focus()
    }
  }
)

const debouncedSearch = debounce((value) => {
  search(value)
}, 300)

function onInput() {
  debouncedSearch(query.value)
}

function close() {
  ui.closeCommandPalette()
}

function selectItem(item) {
  if (!item) {
    return
  }

  if (item.action) {
    item.action()
  }

  close()
}

function shouldShowGroupHeader(index) {
  if (index === 0) {
    return true
  }

  return flatItems.value[index - 1].group !== flatItems.value[index].group
}

function onKeydown(event) {
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    activeIndex.value = Math.min(activeIndex.value + 1, flatItems.value.length - 1)
  } else if (event.key === 'ArrowUp') {
    event.preventDefault()
    activeIndex.value = Math.max(activeIndex.value - 1, 0)
  } else if (event.key === 'Enter') {
    event.preventDefault()
    selectItem(flatItems.value[activeIndex.value])
  } else if (event.key === 'Escape') {
    close()
  }
}

function logout() {
  auth.logout()
  router.push('/login')
}

function onGlobalKeydown(event) {
  if (event.ctrlKey && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    ui.toggleCommandPalette()
  }
}

onMounted(() => {
  window.addEventListener('keydown', onGlobalKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onGlobalKeydown)
})
</script>
