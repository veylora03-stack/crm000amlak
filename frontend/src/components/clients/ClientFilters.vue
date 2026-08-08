<template>
  <section class="card mb-6 p-4">
    <form class="grid gap-4 md:grid-cols-2 xl:grid-cols-5" @submit.prevent="$emit('apply')">
      <div>
        <label for="client-search" class="label-base">جستجو</label>
        <input
          id="client-search"
          :value="modelValue.search"
          type="text"
          class="input-base"
          placeholder="نام، موبایل یا ایمیل"
          @input="setField('search', $event.target.value)"
        />
      </div>

      <div>
        <label for="client-status" class="label-base">وضعیت لید</label>
        <select
          id="client-status"
          :value="modelValue.status"
          class="input-base"
          @change="setField('status', $event.target.value)"
        >
          <option value="">همه وضعیت‌ها</option>
          <option v-for="status in statuses" :key="status.id" :value="status.title">
            {{ status.title }}
          </option>
        </select>
      </div>

      <div>
        <label for="customer-type" class="label-base">نوع مشتری</label>
        <select
          id="customer-type"
          :value="modelValue.customer_type"
          class="input-base"
          @change="setField('customer_type', $event.target.value)"
        >
          <option value="">همه انواع</option>
          <option v-for="type in customerTypes" :key="type.id" :value="type.title">
            {{ type.title }}
          </option>
        </select>
      </div>

      <div>
        <label for="client-source" class="label-base">منبع لید</label>
        <select
          id="client-source"
          :value="modelValue.source"
          class="input-base"
          @change="setField('source', $event.target.value)"
        >
          <option value="">همه منابع</option>
          <option v-for="source in sources" :key="source.id" :value="source.title">
            {{ source.title }}
          </option>
        </select>
      </div>

      <div>
        <label for="assigned-agent" class="label-base">مسئول پیگیری</label>
        <select
          id="assigned-agent"
          :value="modelValue.assigned_agent"
          class="input-base"
          @change="setField('assigned_agent', $event.target.value)"
        >
          <option value="">همه مسئولان</option>
          <option v-for="agent in agents" :key="agent.id" :value="agent.full_name">
            {{ agent.full_name }}
          </option>
        </select>
      </div>

      <div class="flex flex-wrap items-center gap-2 xl:col-span-5">
        <button type="submit" class="btn-primary">
          اعمال فیلترها
        </button>

        <button type="button" class="btn-secondary" @click="$emit('reset')">
          حذف فیلترها
        </button>
      </div>
    </form>
  </section>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
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

const emit = defineEmits(['update:modelValue', 'apply', 'reset'])

function setField(field, value) {
  emit('update:modelValue', {
    ...props.modelValue,
    [field]: value
  })
}
</script>
