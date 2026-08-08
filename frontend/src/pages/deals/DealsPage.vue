<template>
  <AppLayout>
    <PageHeader title="معاملات" description="لیست و مدیریت Dealها در نمای جدولی">
      <template #actions>
        <button type="button" class="btn-primary" @click="openCreateDeal">
          ایجاد Deal
        </button>
      </template>
    </PageHeader>

    <DealFilters
      v-model="filters"
      :stages="dealsStore.stages"
      :agents="settingsStore.users"
      @apply="applyFilters"
      @reset="resetFilters"
    />

    <DealsTable
      :items="paginatedItems"
      :stages="dealsStore.stages"
      :loading="pageLoading || dealsStore.loading"
      :error="dealsStore.error"
      @row-click="openDeal"
      @edit="openEditDeal"
      @delete="confirmDeleteDeal"
      @add="openCreateDeal"
      @retry="applyFilters"
    />

    <div class="mt-4">
      <Pagination
        :page="page"
        :page-size="pageSize"
        :total="dealsStore.deals.length"
        :loading="dealsStore.loading"
        @change="changePage"
      />
    </div>

    <DealDrawer
      :open="Boolean(selectedDeal)"
      :deal="selectedDeal"
      :stages="dealsStore.stages"
      @close="closeDealDrawer"
      @edit="openEditDeal"
      @delete="confirmDeleteDeal"
      @move="moveDeal"
    />

    <DealFormModal
      :open="showDealForm"
      :initial="editingDeal"
      :loading="savingDeal"
      :pipelines="dealsStore.activePipelines"
      :stages="dealsStore.stages"
      :clients="clientsStore.items"
      :properties="propertiesStore.items"
      :agents="settingsStore.users"
      :default-pipeline="dealsStore.selectedPipelineId"
      :default-stage="null"
      @close="closeDealForm"
      @submit="saveDeal"
    />

    <ConfirmModal
      :open="Boolean(deletingDeal)"
      title="حذف Deal"
      :message="deleteMessage"
      confirm-label="حذف Deal"
      cancel-label="انصراف"
      danger
      :loading="deleting"
      @confirm="deleteDeal"
      @cancel="deletingDeal = null"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { debounce } from '@/utils/debounce'
import { useDealsStore } from '@/stores/deals'
import { useClientsStore } from '@/stores/clients'
import { usePropertiesStore } from '@/stores/properties'
import { useSettingsStore } from '@/stores/settings'
import { useUiStore } from '@/stores/ui'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Pagination from '@/components/ui/Pagination.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'
import DealFilters from '@/components/deals/DealFilters.vue'
import DealsTable from '@/components/deals/DealsTable.vue'
import DealDrawer from '@/components/pipeline/DealDrawer.vue'
import DealFormModal from '@/components/pipeline/DealFormModal.vue'

const dealsStore = useDealsStore()
const clientsStore = useClientsStore()
const propertiesStore = usePropertiesStore()
const settingsStore = useSettingsStore()
const ui = useUiStore()

const pageLoading = ref(true)
const filters = ref({
  search: '',
  stage: '',
  agent: '',
  status: ''
})

const page = ref(1)
const pageSize = ref(20)

const selectedDeal = ref(null)
const showDealForm = ref(false)
const editingDeal = ref(null)
const savingDeal = ref(false)
const deletingDeal = ref(null)
const deleting = ref(false)

const deleteMessage = computed(() => {
  if (!deletingDeal.value) {
    return ''
  }

  return `معامله «${deletingDeal.value.title}» حذف نرم می‌شود. آیا مطمئن هستید؟`
})

const paginatedItems = computed(() => {
  const start = (page.value - 1) * pageSize.value
  const end = start + pageSize.value

  return dealsStore.deals.slice(start, end)
})

onMounted(async () => {
  try {
    await Promise.all([
      dealsStore.fetchPipelines(),
      dealsStore.fetchStages(),
      dealsStore.fetchDeals(),
      settingsStore.fetchUsers(),
      clientsStore.fetchClients(),
      propertiesStore.fetchProperties()
    ])
  } finally {
    pageLoading.value = false
  }
})

const debouncedSearch = debounce(() => {
  applyFilters()
}, 300)

watch(
  () => filters.value.search,
  () => {
    debouncedSearch()
  }
)

function applyFilters() {
  Object.entries(filters.value).forEach(([key, value]) => {
    dealsStore.filters[key] = value
  })

  page.value = 1
  dealsStore.fetchDeals()
}

function resetFilters() {
  filters.value = {
    search: '',
    stage: '',
    agent: '',
    status: ''
  }

  dealsStore.filters = {
    search: '',
    stage: '',
    agent: '',
    status: ''
  }

  page.value = 1
  dealsStore.fetchDeals()
}

function changePage(newPage) {
  page.value = newPage
}

function openDeal(deal) {
  selectedDeal.value = deal
}

function closeDealDrawer() {
  selectedDeal.value = null
}

function openCreateDeal() {
  editingDeal.value = null
  showDealForm.value = true
}

function openEditDeal(deal) {
  editingDeal.value = deal
  selectedDeal.value = null
  showDealForm.value = true
}

function closeDealForm() {
  showDealForm.value = false
  editingDeal.value = null
}

async function saveDeal(payload) {
  savingDeal.value = true

  let result = null

  if (editingDeal.value) {
    result = await dealsStore.updateDeal(editingDeal.value.id, payload)
  } else {
    result = await dealsStore.createDeal(payload)
  }

  savingDeal.value = false

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'Deal ذخیره شد',
      message: 'اطلاعات معامله با موفقیت ذخیره شد.'
    })

    closeDealForm()
  } else {
    ui.pushToast({
      type: 'error',
      title: 'ذخیره Deal ناموفق بود',
      message: dealsStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

function confirmDeleteDeal(deal) {
  deletingDeal.value = deal
}

async function deleteDeal() {
  if (!deletingDeal.value) {
    return
  }

  deleting.value = true

  const success = await dealsStore.deleteDeal(deletingDeal.value.id)

  deleting.value = false
  deletingDeal.value = null
  selectedDeal.value = null

  if (success) {
    ui.pushToast({
      type: 'success',
      title: 'Deal حذف شد',
      message: 'حذف نرم معامله انجام شد.'
    })
  } else {
    ui.pushToast({
      type: 'error',
      title: 'حذف Deal ناموفق بود',
      message: dealsStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

async function moveDeal(stageId) {
  if (!selectedDeal.value) {
    return
  }

  const success = await dealsStore.moveDeal(selectedDeal.value.id, stageId)

  if (success) {
    selectedDeal.value.stage = stageId

    ui.pushToast({
      type: 'success',
      title: 'Deal منتقل شد',
      message: 'معامله به Stage انتخاب‌شده منتقل شد.'
    })
  } else {
    ui.pushToast({
      type: 'error',
      title: 'انتقال Deal ناموفق بود',
      message: dealsStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}
</script>
