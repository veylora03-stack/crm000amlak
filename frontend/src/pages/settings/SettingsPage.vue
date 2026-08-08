<template>
  <AppLayout>
    <PageHeader title="تنظیمات" description="مدیریت تنظیمات سیستم، کاربران و مقادیر پایه" />

    <div v-if="!auth.isAdmin" class="card flex flex-col items-center justify-center gap-3 p-10 text-center">
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        شما به بخش تنظیمات دسترسی ندارید.
      </p>
      <RouterLink to="/dashboard" class="btn-primary">
        بازگشت به داشبورد
      </RouterLink>
    </div>

    <template v-else>
      <section class="card mb-6 p-4">
        <div class="flex flex-wrap gap-2">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            type="button"
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium',
              activeTab === tab.key
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
            ]"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>
      </section>

      <GeneralSettings v-if="activeTab === 'general'" />

      <UsersManagement v-if="activeTab === 'users'" />

      <PipelinesManagement v-if="activeTab === 'pipelines'" />

      <StagesManagement v-if="activeTab === 'stages'" />

      <SettingsLookupManager
        v-if="activeTab === 'property-types'"
        category="propertyTypes"
        title="مدیریت انواع ملک"
        description="انواع ملک قابل استفاده در فرم‌ها و فیلترها را مدیریت کنید."
      />

      <SettingsLookupManager
        v-if="activeTab === 'lead-sources'"
        category="leadSources"
        title="مدیریت منابع لید"
        description="منابع ورودی مشتری‌ها و Dealها را مدیریت کنید."
      />

      <SettingsLookupManager
        v-if="activeTab === 'amenities'"
        category="amenities"
        title="مدیریت امکانات رفاهی"
        description="امکانات رفاهی قابل ثبت برای املاک را مدیریت کنید."
      />
    </template>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useSettingsStore } from '@/stores/settings'
import { useDealsStore } from '@/stores/deals'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import GeneralSettings from '@/components/settings/GeneralSettings.vue'
import UsersManagement from '@/components/settings/UsersManagement.vue'
import PipelinesManagement from '@/components/settings/PipelinesManagement.vue'
import StagesManagement from '@/components/settings/StagesManagement.vue'
import SettingsLookupManager from '@/components/settings/SettingsLookupManager.vue'

const auth = useAuthStore()
const settingsStore = useSettingsStore()
const dealsStore = useDealsStore()

const activeTab = ref('general')

const tabs = [
  { key: 'general', label: 'تنظیمات عمومی' },
  { key: 'users', label: 'کاربران' },
  { key: 'pipelines', label: 'Pipelineها' },
  { key: 'stages', label: 'Stageها' },
  { key: 'property-types', label: 'انواع ملک' },
  { key: 'lead-sources', label: 'منابع لید' },
  { key: 'amenities', label: 'امکانات رفاهی' }
]

onMounted(async () => {
  await Promise.all([
    settingsStore.fetchUsers(),
    dealsStore.fetchPipelines(),
    dealsStore.fetchStages(),
    dealsStore.fetchDeals()
  ])
})
</script>
