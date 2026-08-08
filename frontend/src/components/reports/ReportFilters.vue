<template>
  <section class="card mb-6 p-4">
    <form class="grid gap-4 md:grid-cols-2 xl:grid-cols-4" @submit.prevent="$emit('apply')">
      <div>
        <label for="report-type" class="label-base">نوع گزارش</label>
        <select
          id="report-type"
          :value="modelValue.report_type"
          class="input-base"
          @change="setField('report_type', $event.target.value)"
        >
          <option v-for="report in reportTypes" :key="report.value" :value="report.value">
            {{ report.label }}
          </option>
        </select>
      </div>

      <div>
        <label for="report-date-from" class="label-base">از تاریخ</label>
        <input
          id="report-date-from"
          :value="modelValue.date_from"
          type="date"
          class="input-base"
          @input="setField('date_from', $event.target.value)"
        />
      </div>

      <div>
        <label for="report-date-to" class="label-base">تا تاریخ</label>
        <input
          id="report-date-to"
          :value="modelValue.date_to"
          type="date"
          class="input-base"
          @input="setField('date_to', $event.target.value)"
        />
      </div>

      <div>
        <label for="report-status" class="label-base">وضعیت</label>
        <select
          id="report-status"
          :value="modelValue.status"
          class="input-base"
          :disabled="statusOptions.length === 0"
          @change="setField('status', $event.target.value)"
        >
          <option value="">همه وضعیت‌ها</option>
          <option v-for="status in statusOptions" :key="status" :value="status">
            {{ status }}
          </option>
        </select>
      </div>

      <div>
        <label for="report-responsible" class="label-base">مسئول</label>
        <select
          id="report-responsible"
          :value="modelValue.responsible"
          class="input-base"
          :disabled="responsibleOptions.length === 0"
          @change="setField('responsible', $event.target.value)"
        >
          <option value="">همه مسئولان</option>
          <option v-for="person in responsibleOptions" :key="person" :value="person">
            {{ person }}
          </option>
        </select>
      </div>

      <div>
        <label for="report-source" class="label-base">منبع</label>
        <select
          id="report-source"
          :value="modelValue.source"
          class="input-base"
          :disabled="sourceOptions.length === 0"
          @change="setField('source', $event.target.value)"
        >
          <option value="">همه منابع</option>
          <option v-for="source in sourceOptions" :key="source" :value="source">
            {{ source }}
          </option>
        </select>
      </div>

      <div class="md:col-span-2 xl:col-span-4">
        <p class="label-base">انتخاب ستون‌ها</p>

        <div class="flex flex-wrap gap-3">
          <label
            v-for="column in columnsOptions"
            :key="column.key"
            class="flex items-center gap-2 rounded-md border border-border-light px-3 py-2 text-sm dark:border-border-dark"
          >
            <input
              type="checkbox"
              :checked="selectedColumns.includes(column.key)"
              class="h-4 w-4"
              @change="$emit('toggle-column', column.key)"
            />
            {{ column.label }}
          </label>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-2 md:col-span-2 xl:col-span-4">
        <button type="submit" class="btn-primary">
          نمایش گزارش
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
  reportTypes: {
    type: Array,
    required: true
  },
  statusOptions: {
    type: Array,
    default: () => []
  },
  responsibleOptions: {
    type: Array,
    default: () => []
  },
  sourceOptions: {
    type: Array,
    default: () => []
  },
  columnsOptions: {
    type: Array,
    default: () => []
  },
  selectedColumns: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'apply', 'reset', 'toggle-column'])

function setField(field, value) {
  emit('update:modelValue', {
    ...props.modelValue,
    [field]: value
  })
}
</script>
