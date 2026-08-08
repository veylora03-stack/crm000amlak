<template>
  <AppLayout>
    <PageHeader title="پایپ‌لاین فروش" description="مدیریت Dealها به‌صورت Kanban">
      <template #actions>
        <button
          v-if="auth.isManager"
          type="button"
          class="btn-secondary"
          @click="openStageSettings"
        >
          تنظیمات Stageها
        </button>

        <button type="button" class="btn-primary" @click="openCreateDeal">
          ایجاد Deal
        </button>
      </template>
    </PageHeader>

    <div class="mb-4">
      <PipelineSelector
        v-model="dealsStore.selectedPipelineId"
        :pipelines="dealsStore.activePipelines"
      />
    </div>

    <KanbanBoard
      :loading="pageLoading"
      :error="dealsStore.error"
      @retry="loadData"
      @open-deal="openDeal"
      @quick-add="openQuickAdd"
    />

    <DealDrawer
      :open="Boolean(selectedDeal)"
      :deal="selectedDeal"
      :stages="dealsStore.stagesBySelectedPipeline"
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
      :default-stage="dealFormDefaultStage"
      @close="closeDealForm"
      @submit="saveDeal"
    />

    <StageSettingsModal
      :open="showStageSettings"
      :selected-pipeline-id="dealsStore.selectedPipelineId"
      @close="closeStageSettings"
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
import { ref, computed, onMounted } from 'vue'
import { useDealsStore } from '@/stores/deals'
import { useClientsStore } from '@/stores/clients'
import { usePropertiesStore } from '@/stores/properties'
import { useSettingsStore } from '@/stores/settings'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'
import PipelineSelector from '@/components/pipeline/PipelineSelector.vue'
import KanbanBoard from '@/components/pipeline/KanbanBoard.vue'
import DealDrawer from '@/components/pipeline/DealDrawer.vue'
import DealFormModal from '@/components/pipeline/DealFormModal.vue'
import StageSettingsModal from '@/components/pipeline/StageSettingsModal.vue'

const dealsStore = useDealsStore()
const clientsStore = useClientsStore()
const propertiesStore = usePropertiesStore()
const settingsStore = useSettingsStore()
const auth = useAuthStore()
const ui = useUiStore()

const pageLoading = ref(true)
const selectedDeal = ref(null)
const showDealForm = ref(false)
const editingDeal = ref(null)
const savingDeal = ref(false)
const showStageSettings = ref(false)
const deletingDeal = ref(null)
const deleting = ref(false)
const dealFormDefaultStage = ref(null)

const deleteMessage = computed(() => {
  if (!deletingDeal.value) {
    return ''
  }

  return `معامله «${deletingDeal.value.title}» حذف نرم می‌شود. آیا مطمئن هستید؟`
})

onMounted(() => {
  loadData()
})

async function loadData() {
  pageLoading.value = true

  try {
    await Promise.all([
      dealsStore.fetchPipelines(),
      dealsStore.fetchStages(),
      dealsStore.fetchDeals(),
      settingsStore.fetchUsers(),
      clientsStore.fetchClients(),
      propertiesStore.fetchProperties()
    ])

    if (!dealsStore.selectedPipelineId && dealsStore.activePipelines.length > 0) {
      dealsStore.selectPipeline(dealsStore.activePipelines[0].id)
    }
  } catch (error) {
    dealsStore.error = 'دریافت اطلاعات پایپ‌لاین با مشکل مواجه شد.'
  } finally {
    pageLoading.value = false
  }
}

function openDeal(deal) {
  selectedDeal.value = deal
}

function closeDealDrawer() {
  selectedDeal.value = null
}

function openCreateDeal() {
  editingDeal.value = null
  dealFormDefaultStage.value = null
  showDealForm.value = true
}

function openQuickAdd(stage) {
  editingDeal.value = null
  dealFormDefaultStage.value = stage.id
  showDealForm.value = true
}

function openEditDeal(deal) {
  editingDeal.value = deal
  dealFormDefaultStage.value = null
  selectedDeal.value = null
  showDealForm.value = true
}

function closeDealForm() {
  showDealForm.value = false
  editingDeal.value = null
  dealFormDefaultStage.value = null
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

function openStageSettings() {
  showStageSettings.value = true
}

function closeStageSettings() {
  showStageSettings.value = false
}
</script>
