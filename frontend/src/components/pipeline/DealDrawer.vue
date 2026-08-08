<template>
  <Drawer :open="open" title="جزئیات Deal" @close="$emit('close')">
    <div v-if="deal" class="space-y-4 text-sm">
      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">عنوان</span>
        <span class="font-medium">{{ deal.title }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">مشتری</span>
        <span class="font-medium">{{ deal.client_name || '-' }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">ملک</span>
        <span class="font-medium">{{ deal.property_title || '-' }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">Agent</span>
        <span class="font-medium">{{ deal.agent || '-' }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">مبلغ</span>
        <span class="font-medium">{{ formatCurrency(deal.amount) }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">احتمال موفقیت</span>
        <span class="font-medium">{{ deal.probability }}٪</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">تاریخ تخمینی بسته شدن</span>
        <span class="font-medium">{{ formatDate(deal.expected_close_date) }}</span>
      </div>

      <div class="flex items-center justify-between gap-2">
        <span class="text-text-secondary-light dark:text-text-secondary-dark">وضعیت</span>
        <span class="font-medium">{{ deal.status }}</span>
      </div>

      <div v-if="deal.notes" class="rounded-md border border-border-light p-3 dark:border-border-dark">
        <p class="mb-1 font-medium">توضیحات</p>
        <p class="text-text-secondary-light dark:text-text-secondary-dark">{{ deal.notes }}</p>
      </div>

      <div>
        <label for="move-stage" class="label-base">انتقال به Stage</label>
        <select id="move-stage" v-model="selectedStage" class="input-base">
          <option value="">انتخاب کنید</option>
          <option v-for="stage in stages" :key="stage.id" :value="stage.id">
            {{ stage.name }}
          </option>
        </select>
      </div>
    </div>

    <template #footer>
      <div class="flex flex-wrap items-center justify-between gap-2">
        <button type="button" class="btn-secondary" @click="$emit('edit', deal)">
          ویرایش
        </button>

        <button
          type="button"
          class="btn-primary"
          :disabled="!selectedStage"
          @click="$emit('move', Number(selectedStage))"
        >
          انتقال
        </button>

        <button type="button" class="btn-danger" @click="$emit('delete', deal)">
          حذف
        </button>
      </div>
    </template>
  </Drawer>
</template>

<script setup>
import { ref, watch } from 'vue'
import Drawer from '@/components/ui/Drawer.vue'
import { formatDate, formatCurrency } from '@/utils/format'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  deal: {
    type: Object,
    default: null
  },
  stages: {
    type: Array,
    default: () => []
  }
})

defineEmits(['close', 'edit', 'delete', 'move'])

const selectedStage = ref('')

watch(
  () => props.open,
  (open) => {
    if (open && props.deal) {
      selectedStage.value = props.deal.stage
    }
  }
)
</script>
