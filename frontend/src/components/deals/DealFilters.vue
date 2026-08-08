<template>
  <section class="card mb-6 p-4">
    <form class="grid gap-4 md:grid-cols-2 xl:grid-cols-4" @submit.prevent="$emit('apply')">
      <div>
        <label for="deal-search" class="label-base">جستجو</label>
        <input
          id="deal-search"
          :value="modelValue.search"
          type="text"
          class="input-base"
          placeholder="عنوان، مشتری یا ملک"
          @input="setField('search', $event.target.value)"
        />
      </div>

      <div>
        <label for="deal-stage" class="label-base">Stage</label>
        <select
          id="deal-stage"
          :value="modelValue.stage"
          class="input-base"
          @change="setField('stage', $event.target.value)"
        >
          <option value="">همه Stageها</option>
          <option v-for="stage in stages" :key="stage.id" :value="stage.id">
            {{ stage.name }}
          </option>
        </select>
      </div>

      <div>
        <label for="deal-agent" class="label-base">Agent مسئول</label>
        <select
          id="deal-agent"
          :value="modelValue.agent"
          class="input-base"
          @change="setField('agent', $event.target.value)"
        >
          <option value="">همه Agentها</option>
          <option v-for="agent in agents" :key="agent.id" :value="agent.full_name">
            {{ agent.full_name }}
          </option>
        </select>
      </div>

      <div>
        <label for="deal-status" class="label-base">وضعیت</label>
        <select
          id="deal-status"
          :value="modelValue.status"
          class="input-base"
          @change="setField('status', $event.target.value)"
        >
          <option value="">همه وضعیت‌ها</option>
          <option value="Open">Open</option>
          <option value="Won">Won</option>
          <option value="Lost">Lost</option>
        </select>
      </div>

      <div class="flex flex-wrap items-center gap-2 xl:col-span-4">
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
  stages: {
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
