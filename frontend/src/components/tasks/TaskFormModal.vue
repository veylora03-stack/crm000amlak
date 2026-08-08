<template>
  <Modal
    :open="open"
    :title="initial ? 'ویرایش وظیفه' : 'افزودن وظیفه'"
    size="lg"
    :closable="!loading"
    @close="closeModal"
  >
    <form novalidate @submit.prevent="submit">
      <div class="grid gap-4 md:grid-cols-2">
        <div class="md:col-span-2">
          <label for="task_title" class="label-base">عنوان وظیفه *</label>
          <input id="task_title" v-model="form.title" type="text" class="input-base" />
          <p v-if="errors.title" class="error-text">{{ errors.title }}</p>
        </div>

        <div class="md:col-span-2">
          <label for="task_description" class="label-base">توضیحات</label>
          <textarea id="task_description" v-model="form.description" rows="3" class="input-base"></textarea>
        </div>

        <div>
          <label for="task_assigned_user" class="label-base">مسئول *</label>
          <select id="task_assigned_user" v-model="form.assigned_user" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="agent in agents" :key="agent.id" :value="agent.full_name">
              {{ agent.full_name }}
            </option>
          </select>
          <p v-if="errors.assigned_user" class="error-text">{{ errors.assigned_user }}</p>
        </div>

        <div>
          <label for="task_priority" class="label-base">اولویت</label>
          <select id="task_priority" v-model="form.priority" class="input-base">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Urgent">Urgent</option>
          </select>
        </div>

        <div>
          <label for="task_status" class="label-base">وضعیت</label>
          <select id="task_status" v-model="form.status" class="input-base">
            <option value="Todo">Todo</option>
            <option value="In Progress">In Progress</option>
            <option value="Done">Done</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </div>

        <div>
          <label for="task_due_date" class="label-base">تاریخ سررسید *</label>
          <input id="task_due_date" v-model="form.due_date" type="date" class="input-base" />
          <p v-if="errors.due_date" class="error-text">{{ errors.due_date }}</p>
        </div>

        <div>
          <label for="task_due_time" class="label-base">ساعت سررسید</label>
          <input id="task_due_time" v-model="form.due_time" type="time" class="input-base" />
        </div>

        <div>
          <label for="task_client" class="label-base">مشتری مرتبط</label>
          <select id="task_client" v-model="form.client_id" class="input-base">
            <option value="">بدون مشتری</option>
            <option v-for="client in clients" :key="client.id" :value="client.id">
              {{ client.full_name }}
            </option>
          </select>
        </div>

        <div>
          <label for="task_deal" class="label-base">Deal مرتبط</label>
          <select id="task_deal" v-model="form.deal_id" class="input-base">
            <option value="">بدون Deal</option>
            <option v-for="deal in deals" :key="deal.id" :value="deal.id">
              {{ deal.title }}
            </option>
          </select>
        </div>

        <div>
          <label for="task_property" class="label-base">ملک مرتبط</label>
          <select id="task_property" v-model="form.property_id" class="input-base">
            <option value="">بدون ملک</option>
            <option v-for="property in properties" :key="property.id" :value="property.id">
              {{ property.title }}
            </option>
          </select>
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
  agents: {
    type: Array,
    default: () => []
  },
  clients: {
    type: Array,
    default: () => []
  },
  deals: {
    type: Array,
    default: () => []
  },
  properties: {
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

function todayValue() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function buildEmptyForm() {
  return {
    title: '',
    description: '',
    assigned_user: '',
    client_id: '',
    deal_id: '',
    property_id: '',
    priority: 'Medium',
    status: 'Todo',
    due_date: todayValue(),
    due_time: ''
  }
}

function resetForm() {
  if (props.initial) {
    form.value = {
      title: props.initial.title || '',
      description: props.initial.description || '',
      assigned_user: props.initial.assigned_user || '',
      client_id: props.initial.client_id || '',
      deal_id: props.initial.deal_id || '',
      property_id: props.initial.property_id || '',
      priority: props.initial.priority || 'Medium',
      status: props.initial.status || 'Todo',
      due_date: props.initial.due_date || todayValue(),
      due_time: props.initial.due_time || ''
    }
  } else {
    form.value = buildEmptyForm()
  }

  initialForm.value = JSON.parse(JSON.stringify(form.value))
  errors.value = {}
}

function validate() {
  const nextErrors = {}

  if (!form.value.title.trim()) {
    nextErrors.title = 'عنوان وظیفه الزامی است.'
  }

  if (!form.value.assigned_user) {
    nextErrors.assigned_user = 'مسئول وظیفه الزامی است.'
  }

  if (!form.value.due_date) {
    nextErrors.due_date = 'تاریخ سررسید الزامی است.'
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
    title: form.value.title.trim(),
    description: form.value.description,
    assigned_user: form.value.assigned_user,
    client_id: form.value.client_id || null,
    deal_id: form.value.deal_id || null,
    property_id: form.value.property_id || null,
    priority: form.value.priority,
    status: form.value.status,
    due_date: form.value.due_date,
    due_time: form.value.due_time
  }

  emit('submit', payload)
}
</script>
