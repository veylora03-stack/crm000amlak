<template>
  <section class="card p-6">
    <h2 class="mb-4 text-lg font-semibold">تنظیمات عمومی</h2>

    <form class="grid gap-4 md:grid-cols-2" @submit.prevent="save">
      <div>
        <label for="agency_name" class="label-base">نام آژانس *</label>
        <input id="agency_name" v-model="form.agency_name" type="text" class="input-base" />
        <p v-if="errors.agency_name" class="error-text">{{ errors.agency_name }}</p>
      </div>

      <div>
        <label for="currency" class="label-base">واحد پول پیش‌فرض</label>
        <select id="currency" v-model="form.currency" class="input-base">
          <option value="IRR">ریال</option>
          <option value="IRTOMAN">تومان</option>
        </select>
      </div>

      <div>
        <label for="date_format" class="label-base">فرمت تاریخ</label>
        <select id="date_format" v-model="form.date_format" class="input-base">
          <option value="jalali">شمسی</option>
          <option value="gregorian">میلادی</option>
        </select>
      </div>

      <div>
        <label for="language" class="label-base">زبان پیش‌فرض</label>
        <select id="language" v-model="form.language" class="input-base">
          <option value="fa">فارسی</option>
        </select>
      </div>

      <div>
        <label for="direction" class="label-base">جهت پیش‌فرض</label>
        <select id="direction" v-model="form.direction" class="input-base">
          <option value="rtl">راست‌به‌چپ</option>
        </select>
      </div>

      <div class="flex items-end md:col-span-2">
        <button type="submit" class="btn-primary" :disabled="saving">
          {{ saving ? 'در حال ذخیره...' : 'ذخیره تنظیمات' }}
        </button>
      </div>
    </form>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useUiStore } from '@/stores/ui'

const settingsStore = useSettingsStore()
const ui = useUiStore()

const form = ref({
  agency_name: '',
  currency: 'IRR',
  date_format: 'jalali',
  language: 'fa',
  direction: 'rtl'
})

const errors = ref({})
const saving = ref(false)

onMounted(() => {
  form.value = {
    ...form.value,
    ...settingsStore.settings
  }
})

async function save() {
  errors.value = {}

  if (!form.value.agency_name.trim()) {
    errors.value.agency_name = 'نام آژانس الزامی است.'
    return
  }

  saving.value = true

  const success = await settingsStore.updateSettings({
    agency_name: form.value.agency_name.trim(),
    currency: form.value.currency,
    date_format: form.value.date_format,
    language: form.value.language,
    direction: form.value.direction
  })

  saving.value = false

  if (success) {
    ui.pushToast({
      type: 'success',
      title: 'تنظیمات ذخیره شد',
      message: 'تنظیمات عمومی با موفقیت ذخیره شد.'
    })
  } else {
    ui.pushToast({
      type: 'error',
      title: 'ذخیره تنظیمات ناموفق بود',
      message: settingsStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}
</script>
