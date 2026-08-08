<template>
  <AuthLayout>
    <template #title>بازنشانی رمز عبور</template>
    <template #subtitle>رمز عبور جدید را وارد کنید.</template>

    <form novalidate @submit.prevent="submit">
      <div class="mb-4">
        <label for="password" class="label-base">رمز عبور جدید</label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          class="input-base"
          placeholder="رمز عبور جدید"
          autocomplete="new-password"
        />
        <p v-if="errors.password" class="error-text">{{ errors.password }}</p>
      </div>

      <div class="mb-6">
        <label for="passwordConfirm" class="label-base">تکرار رمز عبور جدید</label>
        <input
          id="passwordConfirm"
          v-model="form.passwordConfirm"
          type="password"
          class="input-base"
          placeholder="تکرار رمز عبور جدید"
          autocomplete="new-password"
        />
        <p v-if="errors.passwordConfirm" class="error-text">{{ errors.passwordConfirm }}</p>
      </div>

      <button type="submit" class="btn-primary w-full" :disabled="submitting">
        {{ submitting ? 'در حال ذخیره...' : 'ذخیره رمز جدید' }}
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
  </AuthLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { delay } from '@/utils/delay'
import { useUiStore } from '@/stores/ui'
import AuthLayout from '@/layouts/AuthLayout.vue'

const router = useRouter()
const ui = useUiStore()

const form = ref({
  password: '',
  passwordConfirm: ''
})

const errors = ref({})
const submitting = ref(false)

function validate() {
  const nextErrors = {}

  if (!form.value.password) {
    nextErrors.password = 'رمز عبور جدید الزامی است.'
  } else if (form.value.password.length < 8) {
    nextErrors.password = 'رمز عبور باید حداقل 8 کاراکتر باشد.'
  }

  if (!form.value.passwordConfirm) {
    nextErrors.passwordConfirm = 'تکرار رمز عبور الزامی است.'
  } else if (form.value.password !== form.value.passwordConfirm) {
    nextErrors.passwordConfirm = 'تکرار رمز عبور با رمز جدید یکسان نیست.'
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

  ui.pushToast({
    type: 'success',
    title: 'رمز عبور تغییر کرد',
    message: 'رمز عبور جدید به‌صورت Mock ذخیره شد.'
  })

  router.push('/login')
}
</script>
