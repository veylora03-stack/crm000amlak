<template>
  <section class="card p-6">
    <h2 class="mb-4 text-lg font-semibold">مدیریت Stageها</h2>

    <div class="mb-4">
      <label for="stage_pipeline" class="label-base">انتخاب Pipeline</label>
      <select id="stage_pipeline" v-model="selectedPipelineId" class="input-base md:max-w-xs">
        <option v-for="pipeline in dealsStore.pipelines" :key="pipeline.id" :value="pipeline.id">
          {{ pipeline.name }}
        </option>
      </select>
    </div>

    <form class="grid gap-4 md:grid-cols-3" @submit.prevent="addStage">
      <div>
        <label for="stage_name" class="label-base">نام Stage *</label>
        <input id="stage_name" v-model="newStageName" type="text" class="input-base" />
        <p v-if="error" class="error-text">{{ error }}</p>
      </div>

      <div>
        <label for="stage_color" class="label-base">رنگ Stage</label>
        <input id="stage_color" v-model="newStageColor" type="color" class="input-base h-10 p-1" />
      </div>

      <div class="flex items-end">
        <button type="submit" class="btn-primary">
          افزودن Stage
        </button>
      </div>
    </form>

    <div v-if="pipelineStages.length === 0" class="mt-6 py-8 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark">
      Stageای برای این Pipeline تعریف نشده است.
    </div>

    <ul v-else class="mt-6 space-y-3">
      <li
        v-for="(stage, index) in pipelineStages"
        :key="stage.id"
        class="rounded-md border border-border-light p-4 dark:border-border-dark"
      >
        <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <div>
            <label class="label-base">نام Stage</label>
            <input v-model="stage.name" type="text" class="input-base" />
          </div>

          <div>
            <label class="label-base">رنگ Stage</label>
            <input v-model="stage.color" type="color" class="input-base h-10 p-1" />
          </div>

          <div class="flex items-end gap-3">
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
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDealsStore } from '@/stores/deals'
import { useUiStore } from '@/stores/ui'

const dealsStore = useDealsStore()
const ui = useUiStore()

const selectedPipelineId = ref(null)
const newStageName = ref('')
const newStageColor = ref('#3b82f6')
const error = ref('')

onMounted(() => {
  if (dealsStore.pipelines.length > 0 && !selectedPipelineId.value) {
    selectedPipelineId.value = dealsStore.pipelines[0].id
  }
})

const pipelineStages = computed(() => {
  return dealsStore.stages
    .filter((stage) => stage.pipeline === selectedPipelineId.value)
    .sort((a, b) => a.sort_order - b.sort_order)
})

function addStage() {
  if (!newStageName.value.trim()) {
    error.value = 'نام Stage الزامی است.'
    return
  }

  error.value = ''

  const maxSortOrder = pipelineStages.value.reduce((max, stage) => {
    return Math.max(max, stage.sort_order || 0)
  }, 0)

  dealsStore.stages.push({
    id: Date.now(),
    public_id: 'stage-' + Date.now(),
    pipeline: selectedPipelineId.value,
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
    message: 'Stage جدید با موفقیت اضافه شد.'
  })
}

function moveStage(stage, direction) {
  const stages = [...dealsStore.stages]
    .filter((item) => item.pipeline === selectedPipelineId.value)
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
