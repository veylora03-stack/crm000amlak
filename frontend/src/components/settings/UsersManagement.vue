<template>
  <section class="card p-6">
    <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
      <h2 class="text-lg font-semibold">مدیریت کاربران</h2>

      <button type="button" class="btn-primary" @click="openCreateModal">
        ایجاد کاربر
      </button>
    </div>

    <div v-if="settingsStore.loading" class="space-y-3">
      <div
        v-for="index in 4"
        :key="index"
        class="h-12 animate-pulse rounded-md bg-surface-muted-light dark:bg-surface-muted-dark"
      ></div>
    </div>

    <div v-else-if="settingsStore.users.length === 0" class="py-10 text-center text-sm text-text-secondary-light dark:text-text-secondary-dark">
      کاربری یافت نشد.
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full min-w-[860px] border-collapse text-sm">
        <thead>
          <tr class="border-b border-border-light text-right text-text-secondary-light dark:border-border-dark dark:text-text-secondary-dark">
            <th class="p-3 font-semibold">نام</th>
            <th class="p-3 font-semibold">نام کاربری</th>
            <th class="p-3 font-semibold">ایمیل</th>
            <th class="p-3 font-semibold">نقش</th>
            <th class="p-3 font-semibold">وضعیت</th>
            <th class="p-3 font-semibold">آخرین ورود</th>
            <th class="p-3 font-semibold">اقدامات</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="user in settingsStore.users"
            :key="user.id"
            class="border-b border-border-light dark:border-border-dark"
          >
            <td class="p-3 font-medium">{{ user.full_name }}</td>
            <td class="p-3" dir="ltr">{{ user.username }}</td>
            <td class="p-3" dir="ltr">{{ user.email || '-' }}</td>
            <td class="p-3">{{ user.role }}</td>
            <td class="p-3">
              <span
                :class="[
                  'rounded-full px-2 py-1 text-xs font-medium',
                  user.is_active
                    ? 'bg-success-50 text-success-700 dark:bg-success-900/20 dark:text-success-400'
                    : 'bg-danger-50 text-danger-700 dark:bg-danger-900/20 dark:text-danger-400'
                ]"
              >
                {{ user.is_active ? 'فعال' : 'غیرفعال' }}
              </span>
            </td>
            <td class="p-3">{{ user.last_login || '-' }}</td>
            <td class="p-3">
              <div class="flex flex-wrap items-center gap-2">
                <button type="button" class="btn-secondary" @click="openEditModal(user)">
                  ویرایش
                </button>

                <button type="button" class="btn-secondary" @click="toggleActive(user)">
                  {{ user.is_active ? 'غیرفعال' : 'فعال' }}
                </button>

                <button type="button" class="btn-secondary" @click="resetPassword(user)">
                  ریست رمز عبور
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Modal
      :open="showModal"
      :title="editingUser ? 'ویرایش کاربر' : 'ایجاد کاربر'"
      size="md"
      @close="closeModal"
    >
      <form novalidate @submit.prevent="saveUser">
        <div class="grid gap-4 md:grid-cols-2">
          <div>
            <label for="user_full_name" class="label-base">نام و نام خانوادگی *</label>
            <input id="user_full_name" v-model="form.full_name" type="text" class="input-base" />
            <p v-if="errors.full_name" class="error-text">{{ errors.full_name }}</p>
          </div>

          <div>
            <label for="user_username" class="label-base">نام کاربری *</label>
            <input id="user_username" v-model="form.username" type="text" class="input-base" dir="ltr" />
            <p v-if="errors.username" class="error-text">{{ errors.username }}</p>
          </div>

          <div>
            <label for="user_email" class="label-base">ایمیل</label>
            <input id="user_email" v-model="form.email" type="email" class="input-base" dir="ltr" />
            <p v-if="errors.email" class="error-text">{{ errors.email }}</p>
          </div>

          <div>
            <label for="user_role" class="label-base">نقش *</label>
            <select id="user_role" v-model="form.role" class="input-base">
              <option value="">انتخاب کنید</option>
              <option v-for="role in roles" :key="role" :value="role">
                {{ role }}
              </option>
            </select>
            <p v-if="errors.role" class="error-text">{{ errors.role }}</p>
          </div>

          <div class="md:col-span-2">
            <label class="flex items-center gap-2 text-sm">
              <input id="user_is_active" v-model="form.is_active" type="checkbox" class="h-4 w-4" />
              کاربر فعال باشد
            </label>
          </div>
        </div>
      </form>

      <template #footer>
        <div class="flex items-center justify-between gap-2">
          <button type="button" class="btn-secondary" @click="closeModal">
            انصراف
          </button>

          <button type="button" class="btn-primary" :disabled="saving" @click="saveUser">
            {{ saving ? 'در حال ذخیره...' : 'ذخیره' }}
          </button>
        </div>
      </template>
    </Modal>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useUiStore } from '@/stores/ui'
import Modal from '@/components/ui/Modal.vue'

const settingsStore = useSettingsStore()
const ui = useUiStore()

const roles = ['Admin', 'Manager', 'Agent', 'Client']

const showModal = ref(false)
const editingUser = ref(null)
const saving = ref(false)

const form = ref({
  full_name: '',
  username: '',
  email: '',
  role: '',
  is_active: true
})

const errors = ref({})

function openCreateModal() {
  editingUser.value = null
  form.value = {
    full_name: '',
    username: '',
    email: '',
    role: '',
    is_active: true
  }
  errors.value = {}
  showModal.value = true
}

function openEditModal(user) {
  editingUser.value = user
  form.value = {
    full_name: user.full_name || '',
    username: user.username || '',
    email: user.email || '',
    role: user.role || '',
    is_active: Boolean(user.is_active)
  }
  errors.value = {}
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingUser.value = null
}

function validate() {
  const nextErrors = {}

  if (!form.value.full_name.trim()) {
    nextErrors.full_name = 'نام و نام خانوادگی الزامی است.'
  }

  if (!form.value.username.trim()) {
    nextErrors.username = 'نام کاربری الزامی است.'
  }

  if (form.value.email.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email.trim())) {
    nextErrors.email = 'ایمیل معتبر نیست.'
  }

  if (!form.value.role) {
    nextErrors.role = 'نقش کاربر الزامی است.'
  }

  errors.value = nextErrors
  return Object.keys(nextErrors).length === 0
}

async function saveUser() {
  if (!validate()) {
    return
  }

  saving.value = true

  const payload = {
    full_name: form.value.full_name.trim(),
    username: form.value.username.trim(),
    email: form.value.email.trim(),
    role: form.value.role,
    is_active: form.value.is_active
  }

  let result = null

  if (editingUser.value) {
    result = await settingsStore.updateUser(editingUser.value.id, payload)
  } else {
    result = await settingsStore.createUser(payload)
  }

  saving.value = false

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'کاربر ذخیره شد',
      message: 'اطلاعات کاربر با موفقیت ذخیره شد.'
    })

    closeModal()
  } else {
    ui.pushToast({
      type: 'error',
      title: 'ذخیره کاربر ناموفق بود',
      message: settingsStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

async function toggleActive(user) {
  const result = await settingsStore.toggleUserActive(user.id)

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'وضعیت کاربر به‌روزرسانی شد',
      message: user.is_active ? 'کاربر غیرفعال شد.' : 'کاربر فعال شد.'
    })
  } else {
    ui.pushToast({
      type: 'error',
      title: 'تغییر وضعیت کاربر ناموفق بود',
      message: settingsStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

function resetPassword(user) {
  ui.pushToast({
    type: 'success',
    title: 'رمز عبور ریست شد',
    message: `رمز عبور کاربر «${user.full_name}» به‌صورت Mock ریست شد.`
  })
}
</script>
