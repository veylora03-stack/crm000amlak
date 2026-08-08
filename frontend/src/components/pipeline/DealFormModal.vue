<template>
  <Modal
    :open="open"
    :title="initial ? 'ویرایش Deal' : 'ایجاد Deal'"
    size="lg"
    :closable="!loading"
    @close="closeModal"
  >
    <form novalidate @submit.prevent="submit">
      <div class="grid gap-4 md:grid-cols-2">
        <div class="md:col-span-2">
          <label for="deal_title" class="label-base">عنوان معامله *</label>
          <input id="deal_title" v-model="form.title" type="text" class="input-base" />
          <p v-if="errors.title" class="error-text">{{ errors.title }}</p>
        </div>

        <div>
          <label for="deal_client" class="label-base">مشتری مرتبط *</label>
          <select id="deal_client" v-model="form.client_id" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="client in clients" :key="client.id" :value="client.id">
              {{ client.full_name }}
            </option>
          </select>
          <p v-if="errors.client_id" class="error-text">{{ errors.client_id }}</p>
        </div>

        <div>
          <label for="deal_property" class="label-base">ملک مرتبط</label>
          <select id="deal_property" v-model="form.property_id" class="input-base">
            <option value="">بدون ملک</option>
            <option v-for="property in properties" :key="property.id" :value="property.id">
              {{ property.title }}
            </option>
          </select>
        </div>

        <div>
          <label for="deal_agent" class="label-base">Agent مسئول</label>
          <select id="deal_agent" v-model="form.agent" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="agent in agents" :key="agent.id" :value="agent.full_name">
              {{ agent.full_name }}
            </option>
          </select>
        </div>

        <div>
          <label for="deal_pipeline" class="label-base">Pipeline</label>
          <select id="deal_pipeline" v-model="form.pipeline" class="input-base" @change="onPipelineChange">
            <option v-for="pipeline in pipelines" :key="pipeline.id" :value="pipeline.id">
              {{ pipeline.name }}
            </option>
          </select>
        </div>

        <div>
          <label for="deal_stage" class="label-base">Stage *</label>
          <select id="deal_stage" v-model="form.stage" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="stage in stageOptions" :key="stage.id" :value="stage.id">
              {{ stage.name }}
            </option>
          </select>
          <p v-if="errors.stage" class="error-text">{{ errors.stage }}</p>
        </div>

        <div>
          <label for="deal_amount" class="label-base">مبلغ معامله *</label>
          <input id="deal_amount" v-model.number="form.amount" type="number" min="0" class="input-base" />
          <p v-if="errors.amount" class="error-text">{{ errors.amount }}</p>
        </div>

        <div>
          <label for="deal_probability" class="label-base">احتمال موفقیت (٪)</label>
          <input id="deal_probability" v-model.number="form.probability" type="number" min="0" max="100" class="input-base" />
          <p v-if="errors.probability" class="error-text">{{ errors.probability }}</p>
        </div>

        <div>
          <label for="deal_expected_close_date" class="label-base">تاریخ تخمینی بسته شدن</label>
          <input id="deal_expected_close_date" v-model="form.expected_close_date" type="date" class="input-base" />
        </div>

        <div>
          <label for="deal_source" class="label-base">منبع</label>
          <input id="deal_source" v-model="form.source" type="text" class="input-base" />
        </div>

        <div class="md:col-span-2">
          <label for="deal_notes" class="label-base">توضیحات</label>
          <textarea id="deal_notes" v-model="form.notes" rows="4" class="input-base"></textarea>
        </div>
      </div>
    </form>

    <template #footer>
      <div class="flex items-center justify-between gap-2">
        <button type="button" class="btn-secondary" :disabled="loading" @click="closeModal">
          انصراف
        </button>

        <button type="button" class="btn-primary" :disabled="loading" @click="submit">
          {{ loading ? 'در حال ذخیره...' : 'ذخیره' }}
        </button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Modal from '@/components/ui/Modal.vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  initial: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  pipelines: {
    type: Array,
    default: () => []
  },
  stages: {
    type: Array,
    default: () => []
  },
  clients: {
    type: Array,
    default: () => []
  },
  properties: {
    type: Array,
    default: () => []
  },
  agents: {
    type: Array,
    default: () => []
  },
  defaultPipeline: {
    type: Number,
    default: null
  },
  defaultStage: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['close', 'submit'])

const form = ref(buildEmptyForm())
const initialForm = ref(buildEmptyForm())
const errors = ref({})

const isDirty = computed(() => {
  return JSON.stringify(form.value) !== JSON.stringify(initialForm.value)
})

const stageOptions = computed(() => {
  return props.stages
    .filter((stage) => stage.pipeline === Number(form.value.pipeline))
    .sort((a, b) => a.sort_order - b.sort_order)
})

watch(
  () => props.open,
  (open) => {
    if (open) {
      resetForm()
    }
  }
)

function buildEmptyForm() {
  return {
    title: '',
    client_id: '',
    client_name: '',
    property_id: '',
    property_title: '',
    agent: '',
    pipeline: props.defaultPipeline || 1,
    stage: props.defaultStage || '',
    amount: null,
    probability: 50,
    expected_close_date: '',
    source: '',
    status: 'Open',
    notes: ''
  }
}

function resetForm() {
  if (props.initial) {
    form.value = {
      title: props.initial.title || '',
      client_id: props.initial.client_id || '',
      client_name: props.initial.client_name || '',
      property_id: props.initial.property_id || '',
      property_title: props.initial.property_title || '',
      agent: props.initial.agent || '',
      pipeline: props.initial.pipeline || props.defaultPipeline || 1,
      stage: props.initial.stage || '',
      amount: props.initial.amount ?? null,
      probability: props.initial.probability ?? 50,
      expected_close_date: props.initial.expected_close_date || '',
      source: props.initial.source || '',
      status: props.initial.status || 'Open',
      notes: props.initial.notes || ''
    }
  } else {
    form.value = buildEmptyForm()
  }

  initialForm.value = JSON.parse(JSON.stringify(form.value))
  errors.value = {}
}

function onPipelineChange() {
  form.value.stage = ''
}

function validate() {
  const nextErrors = {}

  if (!form.value.title.trim()) {
    nextErrors.title = 'عنوان معامله الزامی است.'
  }

  if (!form.value.client_id) {
    nextErrors.client_id = 'انتخاب مشتری الزامی است.'
  }

  if (!form.value.stage) {
    nextErrors.stage = 'انتخاب Stage الزامی است.'
  }

  if (form.value.amount === null || form.value.amount === '') {
    nextErrors.amount = 'مبلغ معامله الزامی است.'
  } else if (Number(form.value.amount) < 0) {
    nextErrors.amount = 'مبلغ معامله نمی‌تواند منفی باشد.'
  }

  if (form.value.probability !== null && form.value.probability !== '') {
    const probability = Number(form.value.probability)

    if (probability < 0 || probability > 100) {
      nextErrors.probability = 'احتمال موفقیت باید بین 0 تا 100 باشد.'
    }
  }

  errors.value = nextErrors
  return Object.keys(nextErrors).length === 0
}

function closeModal() {
  if (isDirty.value && !window.confirm('تغییرات ذخیره‌نشده دارید. آیا از بستن فرم مطمئن هستید؟')) {
    return
  }

  emit('close')
}

function submit() {
  if (!validate()) {
    return
  }

  const client = props.clients.find((item) => item.id === Number(form.value.client_id))
  const property = props.properties.find((item) => item.id === Number(form.value.property_id))

  const payload = {
    title: form.value.title.trim(),
    client_id: Number(form.value.client_id),
    client_name: client ? client.full_name : '',
    property_id: form.value.property_id ? Number(form.value.property_id) : null,
    property_title: property ? property.title : null,
    agent: form.value.agent,
    pipeline: Number(form.value.pipeline),
    stage: Number(form.value.stage),
    amount: Number(form.value.amount || 0),
    probability: Number(form.value.probability || 0),
    expected_close_date: form.value.expected_close_date,
    source: form.value.source,
    status: form.value.status,
    notes: form.value.notes
  }

  emit('submit', payload)
}
</script>
