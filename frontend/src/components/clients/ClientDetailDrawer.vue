<template>
  <Drawer :open="open" title="جزئیات مشتری" @close="$emit('close')">
    <div v-if="client" class="space-y-4 text-sm">
      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">نام</span>
        <span class="font-medium">{{ client.full_name }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">موبایل</span>
        <span class="font-medium" dir="ltr">{{ client.phone }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">وضعیت</span>
        <span class="font-medium">{{ client.status }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">نوع مشتری</span>
        <span class="font-medium">{{ client.customer_type }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">مسئول فعلی</span>
        <span class="font-medium">{{ client.assigned_agent || '-' }}</span>
      </div>

      <div>
        <label for="assign-agent" class="label-base">تخصیص Agent</label>
        <select id="assign-agent" v-model="selectedAgent" class="input-base">
          <option value="">بدون مسئول</option>
          <option v-for="agent in agents" :key="agent.id" :value="agent.full_name">
            {{ agent.full_name }}
          </option>
        </select>
      </div>
    </div>

    <template #footer>
      <div class="flex items-center justify-between gap-2">
        <button type="button" class="btn-secondary" @click="$emit('edit')">
          ویرایش مشتری
        </button>

        <button type="button" class="btn-primary" @click="$emit('assign', selectedAgent)">
          ذخیره تخصیص
        </button>
      </div>
    </template>
  </Drawer>
</template>

<script setup>
import { ref, watch } from 'vue'
import Drawer from '@/components/ui/Drawer.vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  client: {
    type: Object,
    default: null
  },
  agents: {
    type: Array,
    default: () => []
  }
})

defineEmits(['close', 'assign', 'edit'])

const selectedAgent = ref('')

watch(
  () => props.open,
  (open) => {
    if (open && props.client) {
      selectedAgent.value = props.client.assigned_agent || ''
    }
  }
)
</script>
