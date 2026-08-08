<template>
  <AppLayout>
    <div class="page-container">
      <!-- Header -->
      <header class="page-header">
        <div>
          <h1 class="page-title">مشتریان</h1>
          <p class="page-subtitle">
            <span class="font-semibold tabular-nums">{{ formatNumber(clientsStore.total) }}</span> مشتری در سیستم
          </p>
        </div>
        <div class="flex items-center gap-2">
          <button class="btn-secondary">
            <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            خروجی
          </button>
          <button class="btn-secondary">
            <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            ورود
          </button>
          <button class="btn-brand" @click="openCreateModal">
            <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            مشتری جدید
          </button>
        </div>
      </header>

      <!-- Search & Filters Bar -->
      <div class="card mb-4 p-2">
        <div class="flex items-center gap-2">
          <div class="relative flex-1">
            <svg class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              class="input !border-0 !bg-transparent !pr-9 focus:!ring-0"
              placeholder="جستجو در نام، موبایل یا ایمیل..."
              @input="onSearch"
            />
          </div>
          <div class="h-6 w-px bg-app-border dark:bg-app-border-dark"></div>
          <button class="btn-ghost" @click="toggleFilters">
            <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            فیلترها
            <span v-if="activeFilterCount > 0" class="rounded-full bg-brand-600 px-1.5 text-[10px] font-bold text-white">
              {{ activeFilterCount }}
            </span>
          </button>
        </div>
      </div>

      <!-- Active Filters Pills -->
      <div v-if="hasActiveFilters" class="mb-4 flex flex-wrap items-center gap-2">
        <span class="text-xs text-base-500">فیلترهای فعال:</span>
        <button
          v-for="pill in activeFilterPills"
          :key="pill.key"
          class="group inline-flex items-center gap-1 rounded-full bg-base-100 px-2.5 py-1 text-xs font-medium text-base-700 transition-colors hover:bg-base-200 dark:bg-base-800 dark:text-base-200 dark:hover:bg-base-700"
          @click="removeFilter(pill.key)"
        >
          {{ pill.label }}
          <svg class="h-3 w-3 opacity-60 group-hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <button class="text-xs font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400" @click="clearAllFilters">
          پاک کردن همه
        </button>
      </div>

      <!-- Table -->
      <div class="card overflow-hidden">
        <div v-if="clientsStore.loading" class="p-4 space-y-3">
          <div v-for="i in 8" :key="i" class="skeleton h-14 w-full"></div>
        </div>

        <div v-else-if="clientsStore.error" class="flex flex-col items-center justify-center gap-3 p-12 text-center">
          <div class="flex h-14 w-14 items-center justify-center rounded-full bg-danger-500/10">
            <svg class="h-7 w-7 text-danger-600 dark:text-danger-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <p class="text-sm font-semibold">{{ clientsStore.error }}</p>
          <button class="btn-secondary" @click="applyFilters">تلاش مجدد</button>
        </div>

        <div v-else-if="clientsStore.items.length === 0" class="flex flex-col items-center justify-center gap-3 p-16 text-center">
          <div class="flex h-16 w-16 items-center justify-center rounded-full bg-base-100 dark:bg-base-800">
            <svg class="h-8 w-8 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <p class="text-sm font-semibold">هنوز مشتری‌ای ثبت نشده</p>
          <p class="max-w-xs text-xs text-base-500">اولین مشتری خود را اضافه کنید و شروع به مدیریت ارتباطات کنید</p>
          <button class="btn-brand mt-2" @click="openCreateModal">
            <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            افزودن اولین مشتری
          </button>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="data-table">
            <thead>
              <tr>
                <th class="w-10"><input type="checkbox" class="h-3.5 w-3.5 rounded border-base-300" /></th>
                <th>مشتری</th>
                <th>موبایل</th>
                <th>نوع</th>
                <th>وضعیت</th>
                <th>مسئول</th>
                <th>ایجاد</th>
                <th class="text-left">عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="client in clientsStore.items"
                :key="client.id"
                class="cursor-pointer"
                @click="goToDetail(client)"
              >
                <td><input type="checkbox" class="h-3.5 w-3.5 rounded border-base-300" @click.stop /></td>
                <td>
                  <div class="flex items-center gap-3">
                    <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-brand-500 to-accent-500 text-xs font-bold text-white">
                      {{ client.full_name.slice(0, 1) }}
                    </div>
                    <div class="min-w-0">
                      <p class="truncate font-semibold">{{ client.full_name }}</p>
                      <p class="truncate text-xs text-base-500">{{ client.email || 'بدون ایمیل' }}</p>
                    </div>
                  </div>
                </td>
                <td class="font-mono text-xs" dir="ltr">{{ client.phone }}</td>
                <td>
                  <span class="badge badge-neutral">{{ client.customer_type || '-' }}</span>
                </td>
                <td>
                  <span :class="['badge badge-dot', statusBadge(client.status)]">{{ client.status }}</span>
                </td>
                <td class="text-xs">{{ client.assigned_agent || '—' }}</td>
                <td class="text-xs text-base-500 tabular-nums">{{ formatDate(client.created_at) }}</td>
                <td class="text-left">
                  <div class="flex items-center justify-end gap-1" @click.stop>
                    <button class="btn-icon btn-ghost" @click.stop="openEditModal(client)">
                      <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button class="btn-icon btn-ghost hover:!text-danger-600" @click.stop="confirmDelete(client)">
                      <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="!clientsStore.loading && clientsStore.items.length > 0" class="border-t border-app-border p-4 dark:border-app-border-dark">
          <Pagination
            :page="clientsStore.page"
            :page-size="clientsStore.pageSize"
            :total="clientsStore.total"
            :loading="clientsStore.loading"
            @change="changePage"
          />
        </div>
      </div>

      <!-- Modals -->
      <ClientFormModal
        :open="showFormModal"
        :initial="editingClient"
        :loading="submitting"
        :statuses="settingsStore.lookups.clientStatuses"
        :customer-types="settingsStore.lookups.customerTypes"
        :sources="settingsStore.lookups.leadSources"
        :agents="settingsStore.users"
        @close="closeFormModal"
        @submit="saveClient"
      />

      <ConfirmModal
        :open="Boolean(deletingClient)"
        title="حذف مشتری"
        :message="deleteMessage"
        confirm-label="حذف مشتری"
        cancel-label="انصراف"
        danger
        :loading="deleting"
        @confirm="deleteClient"
        @cancel="deletingClient = null"
      />
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from '@/utils/debounce'
import { formatNumber, formatDate } from '@/utils/format'
import { useClientsStore } from '@/stores/clients'
import { useSettingsStore } from '@/stores/settings'
import { useUiStore } from '@/stores/ui'
import AppLayout from '@/layouts/AppLayout.vue'
import Pagination from '@/components/ui/Pagination.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'
import ClientFormModal from '@/components/clients/ClientFormModal.vue'

const router = useRouter()
const clientsStore = useClientsStore()
const settingsStore = useSettingsStore()
const ui = useUiStore()

const searchQuery = ref('')
const showFormModal = ref(false)
const editingClient = ref(null)
const submitting = ref(false)
const deletingClient = ref(null)
const deleting = ref(false)
const filtersOpen = ref(false)

const deleteMessage = computed(() => {
  if (!deletingClient.value) return ''
  return `مشتری «${deletingClient.value.full_name}» حذف نرم می‌شود. آیا مطمئن هستید؟`
})

const hasActiveFilters = computed(() => Object.values(clientsStore.filters).some(v => v))
const activeFilterCount = computed(() => Object.values(clientsStore.filters).filter(v => v).length)

const activeFilterPills = computed(() => {
  const pills = []
  const f = clientsStore.filters
  if (f.status) pills.push({ key: 'status', label: `وضعیت: ${f.status}` })
  if (f.customer_type) pills.push({ key: 'customer_type', label: `نوع: ${f.customer_type}` })
  if (f.source) pills.push({ key: 'source', label: `منبع: ${f.source}` })
  if (f.assigned_agent) pills.push({ key: 'assigned_agent', label: `مسئول: ${f.assigned_agent}` })
  return pills
})

onMounted(async () => {
  await Promise.all([
    settingsStore.fetchUsers(),
    clientsStore.fetchClients()
  ])
})

const debouncedSearch = debounce(() => applyFilters(), 300)

function onSearch() {
  debouncedSearch()
}

function applyFilters() {
  clientsStore.setFilter('search', searchQuery.value)
  clientsStore.fetchClients()
}

function toggleFilters() {
  filtersOpen.value = !filtersOpen.value
}

function removeFilter(key) {
  clientsStore.setFilter(key, '')
  clientsStore.fetchClients()
}

function clearAllFilters() {
  clientsStore.resetFilters()
  searchQuery.value = ''
  clientsStore.fetchClients()
}

function changePage(page) {
  clientsStore.setPage(page)
  clientsStore.fetchClients()
}

function openCreateModal() {
  editingClient.value = null
  showFormModal.value = true
}

function openEditModal(client) {
  editingClient.value = client
  showFormModal.value = true
}

function closeFormModal() {
  showFormModal.value = false
  editingClient.value = null
}

async function saveClient(payload) {
  submitting.value = true
  const result = editingClient.value
    ? await clientsStore.updateClient(editingClient.value.id, payload)
    : await clientsStore.createClient(payload)
  submitting.value = false

  if (result) {
    ui.pushToast({ type: 'success', title: 'مشتری ذخیره شد' })
    closeFormModal()
  } else {
    ui.pushToast({ type: 'error', title: 'ذخیره ناموفق', message: clientsStore.error })
  }
}

function confirmDelete(client) {
  deletingClient.value = client
}

async function deleteClient() {
  if (!deletingClient.value) return
  deleting.value = true
  const success = await clientsStore.deleteClient(deletingClient.value.id)
  deleting.value = false
  deletingClient.value = null

  if (success) {
    ui.pushToast({ type: 'success', title: 'مشتری حذف شد' })
  } else {
    ui.pushToast({ type: 'error', title: 'حذف ناموفق', message: clientsStore.error })
  }
}

function goToDetail(client) {
  router.push(`/clients/${client.id}`)
}

function statusBadge(status) {
  if (['Won', 'Qualified'].includes(status)) return 'badge-success'
  if (['Lost', 'Unqualified'].includes(status)) return 'badge-danger'
  if (['Negotiating'].includes(status)) return 'badge-warning'
  return 'badge-brand'
}
</script>
