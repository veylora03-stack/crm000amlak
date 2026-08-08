<template>
  <section>
    <div v-if="loading" class="flex gap-4 overflow-x-auto pb-4">
      <div
        v-for="index in 4"
        :key="index"
        class="h-96 w-80 shrink-0 animate-pulse rounded-lg bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="error"
      class="card flex flex-col items-center justify-center gap-3 p-10 text-center"
    >
      <p class="text-danger-600 dark:text-danger-400">
        دریافت Board با مشکل مواجه شد.
      </p>
      <button type="button" class="btn-primary" @click="$emit('retry')">
        تلاش مجدد
      </button>
    </div>

    <div
      v-else-if="columns.length === 0"
      class="card flex flex-col items-center justify-center gap-3 p-10 text-center"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        هیچ Stageای برای این پایپ‌لاین وجود ندارد.
      </p>
    </div>

    <div v-else class="flex items-start gap-4 overflow-x-auto pb-4">
      <KanbanColumn
        v-for="column in columns"
        :key="column.stage.id"
        :stage="column.stage"
        :deals="column.deals"
        @open-deal="$emit('open-deal', $event)"
        @quick-add="$emit('quick-add', $event)"
        @drag-change="onDragChange($event, column.stage)"
      />
    </div>
  </section>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useDealsStore } from '@/stores/deals'
import { useUiStore } from '@/stores/ui'
import KanbanColumn from '@/components/pipeline/KanbanColumn.vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['retry', 'open-deal', 'quick-add'])

const dealsStore = useDealsStore()
const ui = useUiStore()
const columns = ref([])

onMounted(() => {
  buildBoard()
})

watch(
  () => [dealsStore.deals, dealsStore.stages, dealsStore.selectedPipelineId, props.loading],
  () => {
    if (!props.loading) {
      buildBoard()
    }
  },
  { deep: true }
)

function buildBoard() {
  const stages = dealsStore.stagesBySelectedPipeline

  columns.value = stages.map((stage) => {
    return {
      stage,
      deals: dealsStore.deals.filter((deal) => {
        return deal.stage === stage.id && !deal.is_deleted
      })
    }
  })
}

async function onDragChange(event, stage) {
  if (!event.added) {
    return
  }

  const deal = event.added.element
  const oldStage = deal.stage

  if (oldStage === stage.id) {
    return
  }

  deal.stage = stage.id

  const success = await dealsStore.moveDeal(deal.id, stage.id)

  if (!success) {
    deal.stage = oldStage
    buildBoard()

    ui.pushToast({
      type: 'error',
      title: 'جابجایی معامله ناموفق بود',
      message: dealsStore.error || 'معامله به حالت قبل برگشت.'
    })

    return
  }

  buildBoard()
}
</script>
