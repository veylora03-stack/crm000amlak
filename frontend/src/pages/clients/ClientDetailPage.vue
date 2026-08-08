<template>
  <AppLayout>
    <PageHeader
      :title="pageTitle"
      :description="client ? `${client.customer_type || 'مشتری'} — ${client.status || ''}` : 'جزئیات مشتری'"
      :breadcrumbs="breadcrumbs"
    >
      <template #actions>
        <button type="button" class="btn-secondary" @click="openEditModal">
          ویرایش مشتری
        </button>

        <button type="button" class="btn-secondary" @click="openAssignDrawer">
          تخصیص Agent
        </button>

        <button type="button" class="btn-secondary" @click="goToPipeline">
          ایجاد Deal
        </button>

        <button type="button" class="btn-primary" @click="openInteractionModal">
          ثبت تعامل
        </button>
      </template>
    </PageHeader>

    <div v-if="pageLoading" class="space-y-6">
      <div class="card h-40 animate-pulse bg-surface-muted-light dark:bg-surface-muted-dark"></div>
      <div class="card h-80 animate-pulse bg-surface-muted-light dark:bg-surface-muted-dark"></div>
    </div>

    <div
      v-else-if="!client && clientsStore.error"
      class="card flex flex-col items-center justify-center gap-3 p-10 text-center"
    >
      <p class="text-danger-600 dark:text-danger-400">
        دریافت اطلاعات مشتری با مشکل مواجه شد.
      </p>
      <button type="button" class="btn-primary" @click="loadClient">
        تلاش مجدد
      </button>
    </div>

    <div
      v-else-if="!client"
      class="card flex flex-col items-center justify-center gap-3 p-10 text-center"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        مشتری مورد نظر یافت نشد.
      </p>
      <RouterLink to="/clients" class="btn-primary">
        بازگشت به لیست مشتریان
      </RouterLink>
    </div>

    <template v-else>
      <section class="card mb-6 p-6">
        <h2 class="mb-4 text-lg font-semibold">اطلاعات اصلی مشتری</h2>

        <dl class="grid gap-4 text-sm md:grid-cols-2 xl:grid-cols-3">
          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">موبایل</dt>
            <dd class="font-medium" dir="ltr">{{ client.phone }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">ایمیل</dt>
            <dd class="font-medium" dir="ltr">{{ client.email || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">منبع لید</dt>
            <dd class="font-medium">{{ client.source || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">وضعیت لید</dt>
            <dd class="font-medium">{{ client.status || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">نوع مشتری</dt>
            <dd class="font-medium">{{ client.customer_type || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">مسئول پیگیری</dt>
            <dd class="font-medium">{{ client.assigned_agent || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">بودجه</dt>
            <dd class="font-medium">
              {{ formatCurrency(client.budget_min) }} تا {{ formatCurrency(client.budget_max) }}
            </dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">مناطق مورد نظر</dt>
            <dd class="font-medium">
              {{ client.preferred_areas?.length ? client.preferred_areas.join('، ') : '-' }}
            </dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">نوع ملک مورد نظر</dt>
            <dd class="font-medium">
              {{ client.preferred_property_types?.length ? client.preferred_property_types.join('، ') : '-' }}
            </dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">امتیاز مشتری</dt>
            <dd class="font-medium">{{ formatNumber(client.score || 0) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">تاریخ ایجاد</dt>
            <dd class="font-medium">{{ formatDate(client.created_at) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">تاریخ به‌روزرسانی</dt>
            <dd class="font-medium">{{ formatDate(client.updated_at) }}</dd>
          </div>
        </dl>

        <div v-if="client.notes" class="mt-4 rounded-md border border-border-light p-3 text-sm dark:border-border-dark">
          <p class="mb-1 font-medium">توضیحات</p>
          <p class="text-text-secondary-light dark:text-text-secondary-dark">{{ client.notes }}</p>
        </div>
      </section>

      <section class="card p-4">
        <div class="mb-4 flex flex-wrap gap-2">
          <button
            type="button"
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium',
              activeTab === 'timeline'
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
            ]"
            @click="activeTab = 'timeline'"
          >
            تایم‌لاین تعامل‌ها
          </button>

          <button
            type="button"
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium',
              activeTab === 'deals'
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
            ]"
            @click="activeTab = 'deals'"
          >
            Dealها
          </button>

          <button
            type="button"
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium',
              activeTab === 'notes'
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
            ]"
            @click="activeTab = 'notes'"
          >
            یادداشت‌ها
          </button>
        </div>

        <ClientTimeline
          v-if="activeTab === 'timeline'"
          :items="clientsStore.timeline"
          :loading="pageLoading"
        />

        <ClientDeals
          v-if="activeTab === 'deals'"
          :deals="clientsStore.deals"
          :loading="pageLoading"
          @create="goToPipeline"
        />

        <ClientNotes
          v-if="activeTab === 'notes'"
          :notes="notes"
          :loading="pageLoading"
          @add="addNote"
        />
      </section>
    </template>

    <ClientFormModal
      :open="showEditModal"
      :initial="client"
      :loading="savingEdit"
      :statuses="settingsStore.lookups.clientStatuses"
      :customer-types="settingsStore.lookups.customerTypes"
      :sources="settingsStore.lookups.leadSources"
      :agents="settingsStore.users"
      @close="closeEditModal"
      @submit="saveClient"
    />

    <ClientDetailDrawer
      :open="showAssignDrawer"
      :client="client"
      :agents="settingsStore.users"
      @close="closeAssignDrawer"
      @assign="saveAssign"
      @edit="openEditModalFromDrawer"
    />

    <Modal
      :open="showInteractionModal"
      title="ثبت تعامل"
      size="md"
      @close="closeInteractionModal"
    >
      <form novalidate @submit.prevent="saveInteraction">
        <div class="grid gap-4 md:grid-cols-2">
          <div>
            <label for="interaction_type" class="label-base">نوع تعامل *</label>
            <select id="interaction_type" v-model="interactionForm.interaction_type" class="input-base">
              <option v-for="type in interactionTypes" :key="type.value" :value="type.value">
                {{ type.label }}
              </option>
            </select>
          </div>

          <div>
            <label for="interaction_title" class="label-base">عنوان *</label>
            <input id="interaction_title" v-model="interactionForm.title" type="text" class="input-base" />
            <p v-if="interactionErrors.title" class="error-text">{{ interactionErrors.title }}</p>
          </div>

          <div class="md:col-span-2">
            <label for="interaction_body" class="label-base">توضیحات</label>
            <textarea id="interaction_body" v-model="interactionForm.body" rows="4" class="input-base"></textarea>
          </div>

          <div>
            <label for="occurred_at" class="label-base">تاریخ وقوع *</label>
            <input id="occurred_at" v-model="interactionForm.occurred_at" type="date" class="input-base" />
            <p v-if="interactionErrors.occurred_at" class="error-text">{{ interactionErrors.occurred_at }}</p>
          </div>

          <div>
            <label for="duration_minutes" class="label-base">مدت زمان (دقیقه)</label>
            <input id="duration_minutes" v-model.number="interactionForm.duration_minutes" type="number" min="0" class="input-base" />
          </div>

          <div class="md:col-span-2">
            <label class="flex items-center gap-2 text-sm">
              <input id="needs_followup" v-model="interactionForm.needs_followup" type="checkbox" class="h-4 w-4" />
              نیاز به پیگیری دارد
            </label>
          </div>

          <div v-if="interactionForm.needs_followup">
            <label for="followup_at" class="label-base">تاریخ پیگیری بعدی *</label>
            <input id="followup_at" v-model="interactionForm.followup_at" type="date" class="input-base" />
            <p v-if="interactionErrors.followup_at" class="error-text">{{ interactionErrors.followup_at }}</p>
          </div>
        </div>
      </form>

      <template #footer>
        <div class="flex items-center justify-between gap-2">
          <button type="button" class="btn-secondary" @click="closeInteractionModal">
            انصراف
          </button>

          <button type="button" class="btn-primary" @click="saveInteraction">
            ثبت تعامل
          </button>
        </div>
      </template>
    </Modal>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useClientsStore } from '@/stores/clients'
import { useSettingsStore } from '@/stores/settings'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import { formatDate, formatDateTime, formatCurrency, formatNumber } from '@/utils/format'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Modal from '@/components/ui/Modal.vue'
import ClientFormModal from '@/components/clients/ClientFormModal.vue'
import ClientDetailDrawer from '@/components/clients/ClientDetailDrawer.vue'
import ClientTimeline from '@/components/clients/ClientTimeline.vue'
import ClientDeals from '@/components/clients/ClientDeals.vue'
import ClientNotes from '@/components/clients/ClientNotes.vue'

const route = useRoute()
const router = useRouter()
const clientsStore = useClientsStore()
const settingsStore = useSettingsStore()
const auth = useAuthStore()
const ui = useUiStore()

const pageLoading = ref(true)
const activeTab = ref('timeline')
const showEditModal = ref(false)
const savingEdit = ref(false)
const showAssignDrawer = ref(false)
const showInteractionModal = ref(false)

const today = new Date().toISOString().slice(0, 10)

const interactionForm = ref({
  interaction_type: 'call',
  title: '',
  body: '',
  occurred_at: today,
  duration_minutes: null,
  needs_followup: false,
  followup_at: ''
})

const interactionErrors = ref({})

const interactionTypes = [
  { value: 'call', label: 'تماس تلفنی' },
  { value: 'meeting', label: 'جلسه حضوری' },
  { value: 'email', label: 'ایمیل' },
  { value: 'message', label: 'پیام داخلی' },
  { value: 'note', label: 'یادداشت' },
  { value: 'visit', label: 'بازدید ملک' },
  { value: 'file', label: 'ارسال فایل' },
  { value: 'other', label: 'سایر' }
]

const client = computed(() => clientsStore.currentItem)

const pageTitle = computed(() => {
  return client.value ? client.value.full_name : 'جزئیات مشتری'
})

const breadcrumbs = computed(() => {
  const items = [
    {
      label: 'مشتریان',
      to: '/clients'
    }
  ]

  if (client.value) {
    items.push({
      label: client.value.full_name
    })
  }

  return items
})

const notes = computed(() => {
  return clientsStore.timeline.filter((item) => item.interaction_type === 'note')
})

onMounted(() => {
  loadClient()
})

async function loadClient() {
  pageLoading.value = true

  try {
    await Promise.all([
      settingsStore.fetchUsers(),
      clientsStore.fetchClient(route.params.id),
      clientsStore.fetchTimeline(route.params.id),
      clientsStore.fetchDeals(route.params.id)
    ])
  } catch (error) {
    clientsStore.error = 'دریافت اطلاعات مشتری با مشکل مواجه شد.'
  } finally {
    pageLoading.value = false
  }
}

function openEditModal() {
  showEditModal.value = true
}

function openEditModalFromDrawer() {
  showAssignDrawer.value = false
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
}

async function saveClient(payload) {
  if (!client.value) {
    return
  }

  savingEdit.value = true

  const result = await clientsStore.updateClient(client.value.id, payload)

  savingEdit.value = false

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'مشتری به‌روزرسانی شد',
      message: 'اطلاعات مشتری با موفقیت ذخیره شد.'
    })

    closeEditModal()
  } else {
    ui.pushToast({
      type: 'error',
      title: 'به‌روزرسانی مشتری ناموفق بود',
      message: clientsStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

function openAssignDrawer() {
  showAssignDrawer.value = true
}

function closeAssignDrawer() {
  showAssignDrawer.value = false
}

async function saveAssign(agentName) {
  if (!client.value) {
    return
  }

  const result = await clientsStore.updateClient(client.value.id, {
    assigned_agent: agentName
  })

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'تخصیص Agent انجام شد',
      message: 'مشتری به Agent انتخاب‌شده تخصیص یافت.'
    })

    closeAssignDrawer()
  } else {
    ui.pushToast({
      type: 'error',
      title: 'تخصیص Agent ناموفق بود',
      message: clientsStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

function openInteractionModal() {
  interactionForm.value = {
    interaction_type: 'call',
    title: '',
    body: '',
    occurred_at: today,
    duration_minutes: null,
    needs_followup: false,
    followup_at: ''
  }

  interactionErrors.value = {}
  showInteractionModal.value = true
}

function closeInteractionModal() {
  showInteractionModal.value = false
}

function validateInteraction() {
  const errors = {}

  if (!interactionForm.value.title.trim()) {
    errors.title = 'عنوان تعامل الزامی است.'
  }

  if (!interactionForm.value.occurred_at) {
    errors.occurred_at = 'تاریخ وقوع الزامی است.'
  }

  if (interactionForm.value.needs_followup && !interactionForm.value.followup_at) {
    errors.followup_at = 'تاریخ پیگیری بعدی الزامی است.'
  }

  interactionErrors.value = errors
  return Object.keys(errors).length === 0
}

function saveInteraction() {
  if (!validateInteraction()) {
    return
  }

  const typeLabel = interactionTypes.find(
    (item) => item.value === interactionForm.value.interaction_type
  )?.label || 'سایر'

  clientsStore.timeline.unshift({
    id: Date.now(),
    interaction_type: interactionForm.value.interaction_type,
    title: interactionForm.value.title.trim(),
    body: interactionForm.value.body.trim() || typeLabel,
    occurred_at: new Date(interactionForm.value.occurred_at).toISOString(),
    duration_minutes: Number(interactionForm.value.duration_minutes || 0),
    needs_followup: interactionForm.value.needs_followup,
    followup_at: interactionForm.value.followup_at
      ? new Date(interactionForm.value.followup_at).toISOString()
      : null,
    user: auth.displayName
  })

  ui.pushToast({
    type: 'success',
    title: 'تعامل ثبت شد',
    message: 'تعامل جدید در تایم‌لاین مشتری ثبت شد.'
  })

  closeInteractionModal()
  activeTab.value = 'timeline'
}

function addNote(body) {
  clientsStore.timeline.unshift({
    id: Date.now(),
    interaction_type: 'note',
    title: 'یادداشت',
    body,
    occurred_at: new Date().toISOString(),
    duration_minutes: 0,
    needs_followup: false,
    followup_at: null,
    user: auth.displayName
  })

  ui.pushToast({
    type: 'success',
    title: 'یادداشت ثبت شد',
    message: 'یادداشت جدید برای مشتری ثبت شد.'
  })
}

function goToPipeline() {
  router.push({
    path: '/pipeline',
    query: {
      client: client.value?.id
    }
  })
}
</script>
