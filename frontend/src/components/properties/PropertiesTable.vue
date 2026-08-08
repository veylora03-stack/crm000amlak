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
        دریافت لیست املاک با مشکل مواجه شد.
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
        هنوز ملکی ثبت نشده است.
      </p>
      <button type="button" class="btn-primary" @click="$emit('add')">
        افزودن ملک
      </button>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full min-w-[980px] border-collapse text-sm">
        <thead>
          <tr class="border-b border-border-light text-right text-text-secondary-light dark:border-border-dark dark:text-text-secondary-dark">
            <th class="p-3 font-semibold">کد</th>
            <th class="p-3 font-semibold">عنوان</th>
            <th class="p-3 font-semibold">نوع</th>
            <th class="p-3 font-semibold">آگهی</th>
            <th class="p-3 font-semibold">وضعیت</th>
            <th class="p-3 font-semibold">قیمت</th>
            <th class="p-3 font-semibold">شهر</th>
            <th class="p-3 font-semibold">مسئول</th>
            <th class="p-3 font-semibold">تاریخ ایجاد</th>
            <th class="p-3 font-semibold">اقدامات</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="property in items"
            :key="property.id"
            class="cursor-pointer border-b border-border-light transition duration-normal ease-out hover:bg-secondary-100 dark:border-border-dark dark:hover:bg-secondary-800"
            @click="$emit('row-click', property)"
          >
            <td class="p-3 font-medium" dir="ltr">{{ property.code }}</td>
            <td class="p-3 font-medium">{{ property.title }}</td>
            <td class="p-3">{{ property.property_type }}</td>
            <td class="p-3">{{ property.listing_type }}</td>
            <td class="p-3">
              <span :class="['rounded-full px-2 py-1 text-xs font-medium', statusClass(property.status)]">
                {{ property.status }}
              </span>
            </td>
            <td class="p-3">{{ formatCurrency(property.price) }}</td>
            <td class="p-3">{{ property.city }}</td>
            <td class="p-3">{{ property.assigned_agent || '-' }}</td>
            <td class="p-3">{{ formatDate(property.created_at) }}</td>
            <td class="p-3">
              <div class="flex items-center gap-2">
                <button
                  type="button"
                  class="btn-secondary"
                  @click.stop="$emit('edit', property)"
                >
                  ویرایش
                </button>

                <button
                  type="button"
                  class="btn-danger"
                  @click.stop="$emit('delete', property)"
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

defineProps({
  items: {
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

function statusClass(status) {
  if (status === 'Published') {
    return 'bg-info-50 text-info-700 dark:bg-info-900/20 dark:text-info-400'
  }

  if (status === 'Sold') {
    return 'bg-success-50 text-success-700 dark:bg-success-900/20 dark:text-success-400'
  }

  if (status === 'Rented') {
    return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300'
  }

  if (status === 'Reserved') {
    return 'bg-warning-50 text-warning-700 dark:bg-warning-900/20 dark:text-warning-400'
  }

  if (status === 'Expired') {
    return 'bg-danger-50 text-danger-700 dark:bg-danger-900/20 dark:text-danger-400'
  }

  return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300'
}
</script>
