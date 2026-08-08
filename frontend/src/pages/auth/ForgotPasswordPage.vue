<template>
  <AuthLayout>
    <template #title>فراموشی رمز عبور</template>
    <template #subtitle>در حالت محلی، بازنشانی رمز عبور به‌صورت Mock انجام می‌شود.</template>

    <form v-if="!success" novalidate @submit.prevent="submit">
      <div class="mb-4">
        <label for="identifier" class="label-base">نام کاربری یا ایمیل</label>
        <input
          id="identifier"
          v-model="form.identifier"
          type="text"
          class="input-base"
          placeholder="نام کاربری یا ایمیل خود را وارد کنید"
        />
        <p v-if="errors.identifier" class="error-text">{{ errors.identifier }}</p>
      </div>

      <button type="submit" class="btn-primary w-full" :disabled="submitting">
        {{ submitting ? 'در حال ارسال...' : 'ارسال درخواست بازنشانی' }}
      </button>

      <div class="mt-4 text-center text-sm">
        <RouterLink
          to="/login"
          class="font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
        >
          بازگشت به ورود
        </RouterLink>
      </div>
    </form>

    <div v-else class="text-center">
      <div class="mb-4 rounded-md border border-success-500 bg-success-50 p-3 text-sm text-success-700 dark:bg-success-900/20 dark:text-success-400">
        درخواست بازنشانی به‌صورت Mock ثبت شد.
      </div>

      <RouterLink to="/reset-password" class="btn-primary inline-flex">
        رفتن به بازنشانی رمز عبور
      </RouterLink>

      <div class="mt-4 text-sm">
        <RouterLink
          to="/login"
          class="font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
        >
          بازگشت به ورود
        </RouterLink>
      </div>
    </div>
  </AuthLayout>
</template>

<script setup>
import { ref } from 'vue'
import { delay } from '@/utils/delay'
import AuthLayout from '@/layouts/AuthLayout.vue'

const form = ref({
  identifier: ''
})

const errors = ref({})
const submitting = ref(false)
const success = ref(false)

function validate() {
  const nextErrors = {}

  if (!form.value.identifier.trim()) {
    nextErrors.identifier = 'نام کاربری یا ایمیل الزامی است.'
  }

  errors.value = nextErrors
  return Object.keys(nextErrors).length === 0
}

async function submit() {
  if (!validate()) {
    return
  }

  submitting.value = true
  await delay(500)
  submitting.value = false
  success.value = true
}
</script>
