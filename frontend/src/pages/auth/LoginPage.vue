<template>
  <AuthLayout>
    <form novalidate @submit.prevent="submit" class="space-y-4">
      <div
        v-if="errorMessage"
        class="flex items-start gap-2.5 rounded-lg border border-danger-500/20 bg-danger-500/5 px-3.5 py-2.5 text-xs text-danger-700 dark:border-danger-500/30 dark:text-danger-300"
      >
        <svg class="mt-0.5 h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span>{{ errorMessage }}</span>
      </div>

      <div>
        <label for="identifier" class="label">نام کاربری</label>
        <input
          id="identifier"
          v-model="form.identifier"
          type="text"
          class="input"
          placeholder="admin"
          autocomplete="username"
          :class="{ 'input-error': errors.identifier }"
        />
        <p v-if="errors.identifier" class="error-text">{{ errors.identifier }}</p>
      </div>

      <div>
        <div class="mb-1.5 flex items-center justify-between">
          <label for="password" class="label mb-0">رمز عبور</label>
          <RouterLink
            to="/forgot-password"
            class="text-xs text-brand-600 hover:text-brand-700 dark:text-brand-400"
          >
            فراموشی رمز؟
          </RouterLink>
        </div>
        <div class="relative">
          <input
            id="password"
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            class="input pl-9"
            placeholder="••••••••"
            autocomplete="current-password"
            :class="{ 'input-error': errors.password }"
          />
          <button
            type="button"
            class="absolute left-2.5 top-1/2 -translate-y-1/2 text-base-400 hover:text-base-700 dark:hover:text-base-200"
            @click="showPassword = !showPassword"
          >
            <svg v-if="!showPassword" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
            </svg>
          </button>
        </div>
        <p v-if="errors.password" class="error-text">{{ errors.password }}</p>
      </div>

      <button
        type="submit"
        class="btn-primary w-full !py-2.5 font-semibold"
        :disabled="submitting || auth.loading"
      >
        <span v-if="submitting || auth.loading" class="inline-block h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
        <span v-else>ورود</span>
      </button>

      <div class="mt-4 rounded-lg bg-base-500/5 p-3 text-center">
        <p class="text-[11px] text-base-500">
          ورود سریع تست: <code class="rounded bg-base-500/10 px-1.5 py-0.5 font-mono text-[11px] font-semibold">admin</code> / <code class="rounded bg-base-500/10 px-1.5 py-0.5 font-mono text-[11px] font-semibold">admin123456</code>
        </p>
      </div>
    </form>
  </AuthLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AuthLayout from '@/layouts/AuthLayout.vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const form = ref({ identifier: '', password: '' })
const errors = ref({})
const submitting = ref(false)
const showPassword = ref(false)

const errorMessage = computed(() => auth.error)

onMounted(() => {
  auth.clearError()
  if (auth.isAuthenticated) router.push('/dashboard')
})

function validate() {
  const next = {}
  if (!form.value.identifier.trim()) next.identifier = 'نام کاربری الزامی است.'
  if (!form.value.password) next.password = 'رمز عبور الزامی است.'
  errors.value = next
  return Object.keys(next).length === 0
}

async function submit() {
  if (!validate()) return
  submitting.value = true
  auth.clearError()
  const ok = await auth.login({
    identifier: form.value.identifier.trim(),
    password: form.value.password
  })
  submitting.value = false
  if (ok) {
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/dashboard'
    router.push(redirect)
  }
}
</script>
