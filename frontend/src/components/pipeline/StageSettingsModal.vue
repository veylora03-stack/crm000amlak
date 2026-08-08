<template>
  <Modal :open="open" title="تنظیمات Stageها" size="lg" @close="$emit('close')">
    <div v-if="pipelineStages.length === 0" class="py-8 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark">
      Stageای برای این پایپ‌لاین تعریف نشده است.
    </div>

    <ul v-else class="space-y-3">
      <li
        v-for="(stage, index) in pipelineStages"
        :key="stage.id"
        class="rounded-md border border-border-light p-3 dark:border-border-dark"
      >
        <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <div>
            <label class="label-base" :for="`stage-name-${stage.id}`">نام Stage</label>
            <input
              :id="`stage-name-${stage.id}`"
              v-model="stage.name"
              type="text"
              class="input-base"
            />
          </div>

          <div>
            <label class="label-base" :for="`stage-color-${stage.id}`">رنگ Stage</label>
            <input
              :id="`stage-color-${stage.id}`"
              v-model="stage.color"
              type="color"
              class="input-base h-10 p-1"
            />
          </div>

          <div class="flex items-end gap-2">
            <label class="flex items-center gap-2 text-sm">
              <input v-model="stage.is_won_stage" type="checkbox" class="h-4 w-4" />
              Stage برنده
            </label>

            <label class="flex items-center gap-2 text-sm">
              <input v-model="stage.is_lost_stage" type="checkbox" class="h-4 w-4" />
              Stage بازنده
            </label>
          </div>

          <div class="flex items-end gap-2">
            <button
              type="button"
              class="btn-secondary"
              :disabled="index === 0"
              @click="moveStage(stage, -1)"
            >
              ↑
            </button>

            <button
              type="button"
              class="btn-secondary"
              :disabled="index === pipelineStages.length - 1"
              @click="moveStage(stage, 1)"
            >
              ↓
            </button>

            <button type="button" class="btn-danger" @click="deleteStage(stage)">
              حذف
            </button>
          </div>
        </div>
      </li>
    </ul>

    <div class="mt-6 rounded-md border border-border-light p-4 dark:border-border-dark">
      <h3 class="mb-3 text-sm font-semibold">افزودن Stage جدید</h3>

      <div class="grid gap-3 md:grid-cols-3">
        <div>
          <label for="new-stage-name" class="label-base">نام Stage</label>
          <input id="new-stage-name" v-model="newStageName" type="text" class="input-base" />
          <p v-if="newStageError" class="error-text">{{ newStageError }}</p>
        </div>

        <div>
          <label for="new-stage-color" class="label-base">رنگ Stage</label>
          <input id="new-stage-color" v-model="newStageColor" type="color" class="input-base h-10 p-1" />
        </div>

        <div class="flex items-end">
          <button type="button" class="btn-primary" @click="addStage">
            افزودن Stage
          </button>
        </div>
      </div>
    </div>

    <template #footer>
      <button type="button" class="btn-secondary" @click="$emit('close')">
        بستن
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { ref, computed } from 'vue'
import Modal from '@/components/ui/Modal.vue'
import { useDealsStore } from '@/stores/deals'
import { useUiStore } from '@/stores/ui'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  selectedPipelineId: {
    type: Number,
    default: null
  }
})

defineEmits(['close', 'saved'])

const dealsStore = useDealsStore()
const ui = useUiStore()

const newStageName = ref('')
const newStageColor = ref('#3b82f6')
const newStageError = ref('')

const pipelineStages = computed(() => {
  return dealsStore.stages
    .filter((stage) => stage.pipeline === props.selectedPipelineId)
    .sort((a, b) => a.sort_order - b.sort_order)
})

function addStage() {
  if (!newStageName.value.trim()) {
    newStageError.value = 'نام Stage الزامی است.'
    return
  }

  newStageError.value = ''

  const maxSortOrder = pipelineStages.value.reduce((max, stage) => {
    return Math.max(max, stage.sort_order || 0)
  }, 0)

  dealsStore.stages.push({
    id: Date.now(),
    pipeline: props.selectedPipelineId,
    name: newStageName.value.trim(),
    color: newStageColor.value,
    sort_order: maxSortOrder + 1,
    is_won_stage: false,
    is_lost_stage: false
  })

  newStageName.value = ''
  newStageColor.value = '#3b82f6'

  ui.pushToast({
    type: 'success',
    title: 'Stage اضافه شد',
    message: 'Stage جدید به پایپ‌لاین اضافه شد.'
  })
}

function moveStage(stage, direction) {
  const stages = [...dealsStore.stages]
    .filter((item) => item.pipeline === props.selectedPipelineId)
    .sort((a, b) => a.sort_order - b.sort_order)

  const index = stages.findIndex((item) => item.id === stage.id)
  const targetIndex = index + direction

  if (index === -1 || targetIndex < 0 || targetIndex >= stages.length) {
    return
  }

  const firstStage = stages[index]
  const secondStage = stages[targetIndex]

  const tempSortOrder = firstStage.sort_order
  firstStage.sort_order = secondStage.sort_order
  secondStage.sort_order = tempSortOrder
}

function deleteStage(stage) {
  const hasDeals = dealsStore.deals.some((deal) => deal.stage === stage.id)

  if (hasDeals) {
    ui.pushToast({
      type: 'error',
      title: 'حذف Stage امکان‌پذیر نیست',
      message: 'این Stage دارای Deal است و نمی‌توان آن را حذف کرد.'
    })

    return
  }

  const index = dealsStore.stages.findIndex((item) => item.id === stage.id)

  if (index !== -1) {
    dealsStore.stages.splice(index, 1)

    ui.pushToast({
      type: 'success',
      title: 'Stage حذف شد',
      message: 'Stage انتخاب‌شده حذف شد.'
    })
  }
}
</script>
