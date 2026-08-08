<template>
  <AppLayout>
    <PageHeader title="پروفایل" description="مشاهده اطلاعات کاربری و تغییر رمز عبور" />

    <div class="grid gap-6 lg:grid-cols-2">
      <section class="card p-6">
        <h2 class="mb-4 text-lg font-semibold">اطلاعات شخصی</h2>

        <dl class="space-y-3 text-sm">
          <div class="flex items-center justify-between gap-4">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">نام و نام خانوادگی</dt>
            <dd class="font-medium">{{ auth.user?.full_name || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-4">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">نام کاربری</dt>
            <dd class="font-medium">{{ auth.user?.username || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-4">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">ایمیل</dt>
            <dd class="font-medium">{{ auth.user?.email || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-4">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">نقش</dt>
            <dd class="font-medium">{{ auth.role || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-4">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">آخرین ورود</dt>
            <dd class="font-medium">{{ auth.user?.last_login || '-' }}</dd>
          </div>
        </dl>
      </section>

      <section class="card p-6">
        <h2 class="mb-4 text-lg font-semibold">تغییر رمز عبور</h2>

        <form novalidate @submit.prevent="submitChangePassword">
          <div class="mb-4">
            <label for="currentPassword" class="label-base">رمز عبور فعلی</label>
            <input
              id="currentPassword"
              v-model="passwordForm.currentPassword"
              type="password"
              class="input-base"
              autocomplete="current-password"
            />
            <p v-if="passwordErrors.currentPassword" class="error-text">{{ passwordErrors.currentPassword }}</p>
          </div>

          <div class="mb-4">
            <label for="newPassword" class="label-base">رمز عبور جدید</label>
            <input
              id="newPassword"
              v-model="passwordForm.newPassword"
              type="password"
              class="input-base"
              autocomplete="new-password"
            />
            <p v-if="passwordErrors.newPassword" class="error-text">{{ passwordErrors.newPassword }}</p>
          </div>

          <div class="mb-6">
            <label for="newPasswordConfirm" class="label-base">تکرار رمز عبور جدید</label>
            <input
              id="newPasswordConfirm"
              v-model="passwordForm.newPasswordConfirm"
              type="password"
              class="input-base"
              autocomplete="new-password"
            />
            <p v-if="passwordErrors.newPasswordConfirm" class="error-text">{{ passwordErrors.newPasswordConfirm }}</p>
          </div>

          <button type="submit" class="btn-primary" :disabled="changingPassword">
            {{ changingPassword ? 'در حال ذخیره...' : 'تغییر رمز عبور' }}
          </button>
        </form>
      </section>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { delay } from '@/utils/delay'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'

const auth = useAuthStore()
const ui = useUiStore()

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  newPasswordConfirm: ''
})

const passwordErrors = ref({})
const changingPassword = ref(false)

function validatePasswordForm() {
  const nextErrors = {}

  if (!passwordForm.value.currentPassword) {
    nextErrors.currentPassword = 'رمز عبور فعلی الزامی است.'
  }

  if (!passwordForm.value.newPassword) {
    nextErrors.newPassword = 'رمز عبور جدید الزامی است.'
  } else if (passwordForm.value.newPassword.length < 8) {
    nextErrors.newPassword = 'رمز عبور جدید باید حداقل 8 کاراکتر باشد.'
  }

  if (!passwordForm.value.newPasswordConfirm) {
    nextErrors.newPasswordConfirm = 'تکرار رمز عبور جدید الزامی است.'
  } else if (passwordForm.value.newPassword !== passwordForm.value.newPasswordConfirm) {
    nextErrors.newPasswordConfirm = 'تکرار رمز عبور جدید یکسان نیست.'
  }

  passwordErrors.value = nextErrors
  return Object.keys(nextErrors).length === 0
}

async function submitChangePassword() {
  if (!validatePasswordForm()) {
    return
  }

  changingPassword.value = true
  await delay(500)
  changingPassword.value = false

  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    newPasswordConfirm: ''
  }

  passwordErrors.value = {}

  ui.pushToast({
    type: 'success',
    title: 'رمز عبور تغییر کرد',
    message: 'تغییر رمز عبور در حالت Mock انجام شد.'
  })
}
</script>
