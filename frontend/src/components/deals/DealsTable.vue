<template>
  <section class="card p-4">
    <div v-if="loading" class="space-y-3">
      <div
        v-for="index in 6"
        :key="index"
        class="h-12 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div
      v-else-if="error"
      class="flex flex-col items-center justify-center gap-3 py-12 text-center"
    >
      <p class="text-danger-600 dark:text-danger-400">
        دریافت لیست معاملات با مشکل مواجه شد.
      </p>
      <button type="button" class="btn-primary" @click="$emit('retry')">
        تلاش مجدد
      </button>
    </div>

    <div
      v-else-if="items.length === 0"
      class="flex flex-col items-center justify-center gap-3 py-12 text-center"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        هنوز معامله‌ای ثبت نشده است.
      </p>
      <button type="button" class="btn-primary" @click="$emit('add')">
        ایجاد Deal
      </button>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full min-w-[980px] border-collapse text-sm">
        <thead>
          <tr class="border-b border-border-light text-right text-text-secondary-light dark:border-border-dark dark:text-text-secondary-dark">
            <th class="p-3 font-semibold">عنوان</th>
            <th class="p-3 font-semibold">مشتری</th>
            <th class="p-3 font-semibold">ملک</th>
            <th class="p-3 font-semibold">Stage</th>
            <th class="p-3 font-semibold">مبلغ</th>
            <th class="p-3 font-semibold">Agent</th>
            <th class="p-3 font-semibold">وضعیت</th>
            <th class="p-3 font-semibold">تاریخ تخمینی</th>
            <th class="p-3 font-semibold">اقدامات</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="deal in items"
            :key="deal.id"
            class="cursor-pointer border-b border-border-light transition duration-normal ease-out hover:bg-secondary-100 dark:border-border-dark dark:hover:bg-secondary-800"
            @click="$emit('row-click', deal)"
          >
            <td class="p-3 font-medium">{{ deal.title }}</td>
            <td class="p-3">{{ deal.client_name || '-' }}</td>
            <td class="p-3">{{ deal.property_title || '-' }}</td>
            <td class="p-3">{{ stageName(deal.stage) }}</td>
            <td class="p-3">{{ formatCurrency(deal.amount) }}</td>
            <td class="p-3">{{ deal.agent || '-' }}</td>
            <td class="p-3">
              <span :class="['rounded-full px-2 py-1 text-xs font-medium', statusClass(deal.status)]">
                {{ deal.status }}
              </span>
            </td>
            <td class="p-3">{{ formatDate(deal.expected_close_date) }}</td>
            <td class="p-3">
              <div class="flex items-center gap-2">
                <button
                  type="button"
                  class="btn-secondary"
                  @click.stop="$emit('edit', deal)"
                >
                  ویرایش
                </button>

                <button
                  type="button"
                  class="btn-danger"
                  @click.stop="$emit('delete', deal)"
                >
                  حذف
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { formatDate, formatCurrency } from '@/utils/format'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  stages: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

defineEmits(['row-click', 'edit', 'delete', 'add', 'retry'])

function stageName(stageId) {
  const stage = props.stages.find((item) => item.id === Number(stageId))

  return stage ? stage.name : '-'
}

function statusClass(status) {
  if (status === 'Won') {
    return 'bg-success-50 text-success-700 dark:bg-success-900/20 dark:text-success-400'
  }

  if (status === 'Lost') {
    return 'bg-danger-50 text-danger-700 dark:bg-danger-900/20 dark:text-danger-400'
  }

  return 'bg-info-50 text-info-700 dark:bg-info-900/20 dark:text-info-400'
}
</script>
