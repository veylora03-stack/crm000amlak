<template>
  <section class="card p-6">
    <h2 class="mb-2 text-lg font-semibold">{{ title }}</h2>
    <p class="mb-4 text-sm text-text-secondary-light dark:text-text-secondary-dark">
      {{ description }}
    </p>

    <form class="grid gap-4 md:grid-cols-3" @submit.prevent="addItem">
      <div class="md:col-span-2">
        <label for="lookup-item" class="label-base">عنوان جدید *</label>
        <input id="lookup-item" v-model="newItemTitle" type="text" class="input-base" />
        <p v-if="error" class="error-text">{{ error }}</p>
      </div>

      <div class="flex items-end">
        <button type="submit" class="btn-primary">
          افزودن
        </button>
      </div>
    </form>

    <div v-if="items.length === 0" class="mt-6 py-8 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark">
      موردی ثبت نشده است.
    </div>

    <ul v-else class="mt-6 space-y-3">
      <li
        v-for="item in items"
        :key="item.id"
        class="flex flex-wrap items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark"
      >
        <input v-model="item.title" type="text" class="input-base md:max-w-sm" />

        <div class="flex items-center gap-3">
          <label class="flex items-center gap-2 text-sm">
            <input v-model="item.is_active" type="checkbox" class="h-4 w-4" />
            فعال
          </label>

          <button
            type="button"
            class="btn-danger"
            :disabled="!item.is_active"
            @click="deactivateItem(item)"
          >
            غیرفعال‌سازی
          </button>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useUiStore } from '@/stores/ui'

const props = defineProps({
  category: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  }
})

const settingsStore = useSettingsStore()
const ui = useUiStore()

const newItemTitle = ref('')
const error = ref('')

const items = computed(() => {
  return settingsStore.lookups[props.category] || []
})

function addItem() {
  if (!newItemTitle.value.trim()) {
    error.value = 'عنوان الزامی است.'
    return
  }

  error.value = ''

  settingsStore.addLookupItem(props.category, newItemTitle.value.trim())

  newItemTitle.value = ''

  ui.pushToast({
    type: 'success',
    title: 'مورد جدید اضافه شد',
    message: 'مورد جدید با موفقیت اضافه شد.'
  })
}

function deactivateItem(item) {
  settingsStore.deactivateLookupItem(props.category, item.id)

  ui.pushToast({
    type: 'success',
    title: 'مورد غیرفعال شد',
    message: 'مورد انتخاب‌شده غیرفعال شد.'
  })
}
</script>
