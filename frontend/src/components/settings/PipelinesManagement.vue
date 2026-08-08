<template>
  <section class="card p-6">
    <h2 class="mb-4 text-lg font-semibold">مدیریت Pipelineها</h2>

    <form class="grid gap-4 md:grid-cols-3" @submit.prevent="addPipeline">
      <div>
        <label for="pipeline_name" class="label-base">نام Pipeline *</label>
        <input id="pipeline_name" v-model="newPipelineName" type="text" class="input-base" />
        <p v-if="error" class="error-text">{{ error }}</p>
      </div>

      <div>
        <label for="pipeline_description" class="label-base">توضیحات</label>
        <input id="pipeline_description" v-model="newPipelineDescription" type="text" class="input-base" />
      </div>

      <div class="flex items-end">
        <button type="submit" class="btn-primary">
          افزودن Pipeline
        </button>
      </div>
    </form>

    <div v-if="dealsStore.pipelines.length === 0" class="mt-6 py-8 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark">
      Pipelineای تعریف نشده است.
    </div>

    <ul v-else class="mt-6 space-y-3">
      <li
        v-for="pipeline in dealsStore.pipelines"
        :key="pipeline.id"
        class="rounded-md border border-border-light p-4 dark:border-border-dark"
      >
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p class="font-medium">{{ pipeline.name }}</p>
            <p class="mt-1 text-sm text-text-secondary-light dark:text-text-secondary-dark">
              {{ pipeline.description || 'بدون توضیحات' }}
            </p>
          </div>

          <label class="flex items-center gap-2 text-sm">
            <input
              v-model="pipeline.is_active"
              type="checkbox"
              class="h-4 w-4"
              @change="togglePipeline(pipeline)"
            />
            فعال
          </label>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useDealsStore } from '@/stores/deals'
import { useUiStore } from '@/stores/ui'

const dealsStore = useDealsStore()
const ui = useUiStore()

const newPipelineName = ref('')
const newPipelineDescription = ref('')
const error = ref('')

function addPipeline() {
  if (!newPipelineName.value.trim()) {
    error.value = 'نام Pipeline الزامی است.'
    return
  }

  error.value = ''

  dealsStore.pipelines.push({
    id: Date.now(),
    public_id: 'pipeline-' + Date.now(),
    name: newPipelineName.value.trim(),
    description: newPipelineDescription.value.trim(),
    is_active: true,
    sort_order: dealsStore.pipelines.length + 1
  })

  newPipelineName.value = ''
  newPipelineDescription.value = ''

  ui.pushToast({
    type: 'success',
    title: 'Pipeline اضافه شد',
    message: 'Pipeline جدید با موفقیت اضافه شد.'
  })
}

function togglePipeline(pipeline) {
  ui.pushToast({
    type: 'success',
    title: 'وضعیت Pipeline به‌روزرسانی شد',
    message: pipeline.is_active ? 'Pipeline فعال شد.' : 'Pipeline غیرفعال شد.'
  })
}
</script>
