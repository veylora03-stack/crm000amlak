<template>
  <Modal
    :open="open"
    :title="initial ? 'ویرایش مشتری' : 'افزودن مشتری'"
    size="lg"
    :closable="!loading"
    @close="closeModal"
  >
    <form novalidate @submit.prevent="submit">
      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label for="full_name" class="label-base">نام کامل *</label>
          <input
            id="full_name"
            v-model="form.full_name"
            type="text"
            class="input-base"
          />
          <p v-if="errors.full_name" class="error-text">{{ errors.full_name }}</p>
        </div>

        <div>
          <label for="phone" class="label-base">موبایل *</label>
          <input
            id="phone"
            v-model="form.phone"
            type="text"
            class="input-base"
            dir="ltr"
          />
          <p v-if="errors.phone" class="error-text">{{ errors.phone }}</p>
        </div>

        <div>
          <label for="email" class="label-base">ایمیل</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="input-base"
            dir="ltr"
          />
          <p v-if="errors.email" class="error-text">{{ errors.email }}</p>
        </div>

        <div>
          <label for="source" class="label-base">منبع لید</label>
          <select id="source" v-model="form.source" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="source in sources" :key="source.id" :value="source.title">
              {{ source.title }}
            </option>
          </select>
        </div>

        <div>
          <label for="status" class="label-base">وضعیت لید</label>
          <select id="status" v-model="form.status" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="status in statuses" :key="status.id" :value="status.title">
              {{ status.title }}
            </option>
          </select>
        </div>

        <div>
          <label for="customer_type" class="label-base">نوع مشتری</label>
          <select id="customer_type" v-model="form.customer_type" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="type in customerTypes" :key="type.id" :value="type.title">
              {{ type.title }}
            </option>
          </select>
        </div>

        <div>
          <label for="budget_min" class="label-base">بودجه حداقل</label>
          <input
            id="budget_min"
            v-model.number="form.budget_min"
            type="number"
            min="0"
            class="input-base"
          />
          <p v-if="errors.budget_min" class="error-text">{{ errors.budget_min }}</p>
        </div>

        <div>
          <label for="budget_max" class="label-base">بودجه حداکثر</label>
          <input
            id="budget_max"
            v-model.number="form.budget_max"
            type="number"
            min="0"
            class="input-base"
          />
          <p v-if="errors.budget_max" class="error-text">{{ errors.budget_max }}</p>
        </div>

        <div>
          <label for="preferred_areas_text" class="label-base">مناطق مورد نظر</label>
          <input
            id="preferred_areas_text"
            v-model="form.preferred_areas_text"
            type="text"
            class="input-base"
            placeholder="با کاما جدا کنید"
          />
        </div>

        <div>
          <label for="preferred_property_types_text" class="label-base">نوع ملک مورد نظر</label>
          <input
            id="preferred_property_types_text"
            v-model="form.preferred_property_types_text"
            type="text"
            class="input-base"
            placeholder="با کاما جدا کنید"
          />
        </div>

        <div>
          <label for="assigned_agent" class="label-base">مسئول پیگیری</label>
          <select id="assigned_agent" v-model="form.assigned_agent" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="agent in agents" :key="agent.id" :value="agent.full_name">
              {{ agent.full_name }}
            </option>
          </select>
        </div>

        <div class="md:col-span-2">
          <label for="notes" class="label-base">توضیحات</label>
          <textarea
            id="notes"
            v-model="form.notes"
            rows="4"
            class="input-base"
          ></textarea>
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
import { ref, watch, computed } from 'vue'
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
  statuses: {
    type: Array,
    default: () => []
  },
  customerTypes: {
    type: Array,
    default: () => []
  },
  sources: {
    type: Array,
    default: () => []
  },
  agents: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'submit'])

const form = ref(buildEmptyForm())
const initialForm = ref(buildEmptyForm())
const errors = ref({})

const isDirty = computed(() => {
  return JSON.stringify(form.value) !== JSON.stringify(initialForm.value)
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
    full_name: '',
    phone: '',
    email: '',
    source: '',
    status: 'New',
    customer_type: '',
    budget_min: null,
    budget_max: null,
    preferred_areas_text: '',
    preferred_property_types_text: '',
    notes: '',
    assigned_agent: ''
  }
}

function resetForm() {
  if (props.initial) {
    form.value = {
      full_name: props.initial.full_name || '',
      phone: props.initial.phone || '',
      email: props.initial.email || '',
      source: props.initial.source || '',
      status: props.initial.status || 'New',
      customer_type: props.initial.customer_type || '',
      budget_min: props.initial.budget_min ?? null,
      budget_max: props.initial.budget_max ?? null,
      preferred_areas_text: Array.isArray(props.initial.preferred_areas)
        ? props.initial.preferred_areas.join('، ')
        : '',
      preferred_property_types_text: Array.isArray(props.initial.preferred_property_types)
        ? props.initial.preferred_property_types.join('، ')
        : '',
      notes: props.initial.notes || '',
      assigned_agent: props.initial.assigned_agent || ''
    }
  } else {
    form.value = buildEmptyForm()
  }

  initialForm.value = JSON.parse(JSON.stringify(form.value))
  errors.value = {}
}

function parseList(value) {
  return String(value || '')
    .split(/[,،]/)
    .map((item) => item.trim())
    .filter(Boolean)
}

function validate() {
  const nextErrors = {}

  if (!form.value.full_name.trim()) {
    nextErrors.full_name = 'نام کامل الزامی است.'
  }

  if (!form.value.phone.trim()) {
    nextErrors.phone = 'شماره موبایل الزامی است.'
  } else if (!/^09\d{9}$/.test(form.value.phone.trim())) {
    nextErrors.phone = 'شماره موبایل معتبر نیست.'
  }

  if (form.value.email.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email.trim())) {
    nextErrors.email = 'ایمیل معتبر نیست.'
  }

  if (form.value.budget_min !== null && form.value.budget_min !== '' && Number(form.value.budget_min) < 0) {
    nextErrors.budget_min = 'بودجه حداقل نمی‌تواند منفی باشد.'
  }

  if (form.value.budget_max !== null && form.value.budget_max !== '' && Number(form.value.budget_max) < 0) {
    nextErrors.budget_max = 'بودجه حداکثر نمی‌تواند منفی باشد.'
  }

  if (
    form.value.budget_min !== null &&
    form.value.budget_max !== null &&
    Number(form.value.budget_min) > Number(form.value.budget_max)
  ) {
    nextErrors.budget_max = 'بودجه حداکثر نمی‌تواند کمتر از بودجه حداقل باشد.'
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

  const payload = {
    full_name: form.value.full_name.trim(),
    phone: form.value.phone.trim(),
    email: form.value.email.trim(),
    source: form.value.source,
    status: form.value.status,
    customer_type: form.value.customer_type,
    budget_min: Number(form.value.budget_min || 0),
    budget_max: Number(form.value.budget_max || 0),
    preferred_areas: parseList(form.value.preferred_areas_text),
    preferred_property_types: parseList(form.value.preferred_property_types_text),
    notes: form.value.notes,
    assigned_agent: form.value.assigned_agent
  }

  emit('submit', payload)
}
</script>
