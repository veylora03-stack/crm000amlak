<template>
  <section class="card mb-6 p-4">
    <form class="grid gap-4 md:grid-cols-3" @submit.prevent="$emit('apply')">
      <div>
        <label for="task-assigned-user" class="label-base">مسئول</label>
        <select
          id="task-assigned-user"
          :value="modelValue.assigned_user"
          class="input-base"
          @change="setField('assigned_user', $event.target.value)"
        >
          <option value="">همه مسئولان</option>
          <option v-for="agent in agents" :key="agent.id" :value="agent.full_name">
            {{ agent.full_name }}
          </option>
        </select>
      </div>

      <div>
        <label for="task-priority" class="label-base">اولویت</label>
        <select
          id="task-priority"
          :value="modelValue.priority"
          class="input-base"
          @change="setField('priority', $event.target.value)"
        >
          <option value="">همه اولویت‌ها</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
          <option value="Urgent">Urgent</option>
        </select>
      </div>

      <div>
        <label for="task-status" class="label-base">وضعیت</label>
        <select
          id="task-status"
          :value="modelValue.status"
          class="input-base"
          @change="setField('status', $event.target.value)"
        >
          <option value="">همه وضعیت‌ها</option>
          <option value="Todo">Todo</option>
          <option value="In Progress">In Progress</option>
          <option value="Done">Done</option>
          <option value="Cancelled">Cancelled</option>
        </select>
      </div>

      <div class="flex flex-wrap items-center gap-2 md:col-span-3">
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
