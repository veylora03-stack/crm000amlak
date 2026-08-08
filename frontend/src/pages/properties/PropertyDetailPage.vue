<template>
  <AppLayout>
    <PageHeader
      :title="pageTitle"
      :description="pageDescription"
      :breadcrumbs="breadcrumbs"
    >
      <template #actions>
        <button type="button" class="btn-secondary" @click="copyCode">
          کپی کد ملک
        </button>

        <button
          type="button"
          class="btn-secondary"
          :disabled="savingStatus"
          @click="publishProperty"
        >
          انتشار
        </button>

        <button
          type="button"
          class="btn-danger"
          :disabled="savingStatus"
          @click="archiveProperty"
        >
          آرشیو
        </button>

        <button type="button" class="btn-primary" @click="openEditModal">
          ویرایش ملک
        </button>
      </template>
    </PageHeader>

    <div v-if="pageLoading" class="space-y-6">
      <div class="card h-40 animate-pulse bg-surface-muted-light dark:bg-surface-muted-dark"></div>
      <div class="card h-96 animate-pulse bg-surface-muted-light dark:bg-surface-muted-dark"></div>
    </div>

    <div
      v-else-if="!property && propertiesStore.error"
      class="card flex flex-col items-center justify-center gap-3 p-10 text-center"
    >
      <p class="text-danger-600 dark:text-danger-400">
        دریافت اطلاعات ملک با مشکل مواجه شد.
      </p>
      <button type="button" class="btn-primary" @click="loadProperty">
        تلاش مجدد
      </button>
    </div>

    <div
      v-else-if="!property"
      class="card flex flex-col items-center justify-center gap-3 p-10 text-center"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        ملک مورد نظر یافت نشد.
      </p>
      <RouterLink to="/properties" class="btn-primary">
        بازگشت به لیست املاک
      </RouterLink>
    </div>

    <template v-else>
      <section class="card mb-6 p-4">
        <div class="flex flex-wrap gap-2">
          <button
            type="button"
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium',
              activeTab === 'details'
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
            ]"
            @click="activeTab = 'details'"
          >
            جزئیات ملک
          </button>

          <button
            type="button"
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium',
              activeTab === 'gallery'
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
            ]"
            @click="activeTab = 'gallery'"
          >
            گالری و تصاویر
          </button>

          <button
            type="button"
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium',
              activeTab === 'map'
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
            ]"
            @click="activeTab = 'map'"
          >
            نقشه
          </button>

          <button
            type="button"
            :class="[
              'rounded-md px-4 py-2 text-sm font-medium',
              activeTab === 'matches'
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-text-secondary-light hover:bg-secondary-200 dark:bg-secondary-800 dark:text-text-secondary-dark dark:hover:bg-secondary-700'
            ]"
            @click="activeTab = 'matches'"
          >
            Smart Match
          </button>
        </div>
      </section>

      <section v-if="activeTab === 'details'" class="card p-6">
        <h2 class="mb-4 text-lg font-semibold">اطلاعات اصلی ملک</h2>

        <dl class="grid gap-4 text-sm md:grid-cols-2 xl:grid-cols-3">
          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">کد ملک</dt>
            <dd class="font-medium" dir="ltr">{{ property.code }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">نوع ملک</dt>
            <dd class="font-medium">{{ property.property_type || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">نوع آگهی</dt>
            <dd class="font-medium">{{ property.listing_type || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">وضعیت ملک</dt>
            <dd class="font-medium">{{ property.status || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">قیمت</dt>
            <dd class="font-medium">{{ formatCurrency(property.price) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">مبلغ رهن</dt>
            <dd class="font-medium">{{ formatCurrency(property.deposit_amount) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">مبلغ اجاره</dt>
            <dd class="font-medium">{{ formatCurrency(property.rent_amount) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">متراژ زمین</dt>
            <dd class="font-medium">{{ formatNumber(property.land_area) }} متر مربع</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">متراژ بنا</dt>
            <dd class="font-medium">{{ formatNumber(property.building_area) }} متر مربع</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">اتاق خواب</dt>
            <dd class="font-medium">{{ formatNumber(property.bedrooms) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">حمام</dt>
            <dd class="font-medium">{{ formatNumber(property.bathrooms) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">پارکینگ</dt>
            <dd class="font-medium">{{ formatNumber(property.parking_count) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">طبقه</dt>
            <dd class="font-medium">{{ property.floor_number ?? '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">تعداد طبقات</dt>
            <dd class="font-medium">{{ property.total_floors ?? '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">سال ساخت</dt>
            <dd class="font-medium">{{ property.year_built || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">Agent مسئول</dt>
            <dd class="font-medium">{{ property.assigned_agent || '-' }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">تاریخ ایجاد</dt>
            <dd class="font-medium">{{ formatDate(property.created_at) }}</dd>
          </div>

          <div class="flex items-center justify-between gap-3 rounded-md border border-border-light p-3 dark:border-border-dark">
            <dt class="text-text-secondary-light dark:text-text-secondary-dark">تاریخ به‌روزرسانی</dt>
            <dd class="font-medium">{{ formatDate(property.updated_at) }}</dd>
          </div>
        </dl>

        <div class="mt-6 rounded-md border border-border-light p-4 dark:border-border-dark">
          <h3 class="mb-2 font-medium">آدرس</h3>
          <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark">
            {{ property.address || 'آدرس ثبت نشده است.' }}
          </p>
          <p class="mt-2 text-sm text-text-secondary-light dark:text-text-secondary-dark">
            {{ [property.province, property.city, property.district, property.neighborhood].filter(Boolean).join('، ') || '-' }}
          </p>
        </div>

        <div class="mt-6 rounded-md border border-border-light p-4 dark:border-border-dark">
          <h3 class="mb-2 font-medium">امکانات رفاهی</h3>

          <div v-if="property.amenities?.length" class="flex flex-wrap gap-2">
            <span
              v-for="amenity in property.amenities"
              :key="amenity"
              class="rounded-full bg-secondary-100 px-3 py-1 text-xs text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300"
            >
              {{ amenity }}
            </span>
          </div>

          <p v-else class="text-sm text-text-secondary-light dark:text-text-secondary-dark">
            امکانات رفاهی ثبت نشده است.
          </p>
        </div>

        <div class="mt-6 rounded-md border border-border-light p-4 dark:border-border-dark">
          <h3 class="mb-2 font-medium">توضیحات</h3>
          <p class="text-sm leading-6 text-text-secondary-light dark:text-text-secondary-dark">
            {{ property.description || 'توضیحاتی ثبت نشده است.' }}
          </p>
        </div>
      </section>

      <section v-if="activeTab === 'gallery'" class="space-y-6">
        <PropertyGallery :images="images" />
        <PropertyImagesManager
          :images="images"
          @add="addImages"
          @set-primary="setPrimaryImage"
          @delete="deleteImage"
          @move="moveImage"
        />
      </section>

      <section v-if="activeTab === 'map'" class="card p-4">
        <PropertyMap
          :latitude="property.latitude"
          :longitude="property.longitude"
        />
      </section>

      <section v-if="activeTab === 'matches'" class="card p-4">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-semibold">Smart Match با مشتریان</h2>
          <button type="button" class="btn-secondary" @click="loadMatches">
            به‌روزرسانی
          </button>
        </div>

        <PropertyMatchList
          :matches="propertiesStore.matches"
          :loading="matchesLoading"
          @view-client="goToClient"
        />
      </section>
    </template>

    <PropertyFormModal
      :open="showEditModal"
      :initial="property"
      :loading="savingEdit"
      :property-types="settingsStore.lookups.propertyTypes"
      :listing-types="settingsStore.lookups.listingTypes"
      :statuses="settingsStore.lookups.propertyStatuses"
      :agents="settingsStore.users"
      @close="closeEditModal"
      @submit="saveProperty"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { useSettingsStore } from '@/stores/settings'
import { useUiStore } from '@/stores/ui'
import { formatDate, formatCurrency, formatNumber } from '@/utils/format'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import PropertyFormModal from '@/components/properties/PropertyFormModal.vue'
import PropertyGallery from '@/components/properties/PropertyGallery.vue'
import PropertyImagesManager from '@/components/properties/PropertyImagesManager.vue'
import PropertyMap from '@/components/properties/PropertyMap.vue'
import PropertyMatchList from '@/components/properties/PropertyMatchList.vue'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()
const settingsStore = useSettingsStore()
const ui = useUiStore()

const pageLoading = ref(true)
const matchesLoading = ref(false)
const activeTab = ref('details')
const showEditModal = ref(false)
const savingEdit = ref(false)
const savingStatus = ref(false)

const property = computed(() => propertiesStore.currentItem)
const images = computed(() => propertiesStore.images)

const pageTitle = computed(() => {
  return property.value ? property.value.title : 'جزئیات ملک'
})

const pageDescription = computed(() => {
  if (!property.value) {
    return ''
  }

  return [
    property.value.property_type,
    property.value.listing_type,
    property.value.status
  ].filter(Boolean).join(' — ')
})

const breadcrumbs = computed(() => {
  const items = [
    {
      label: 'املاک',
      to: '/properties'
    }
  ]

  if (property.value) {
    items.push({
      label: property.value.title
    })
  }

  return items
})

onMounted(() => {
  loadProperty()
})

async function loadProperty() {
  pageLoading.value = true

  try {
    await Promise.all([
      settingsStore.fetchUsers(),
      propertiesStore.fetchProperty(route.params.id),
      loadMatches(false)
    ])
  } catch (error) {
    propertiesStore.error = 'دریافت اطلاعات ملک با مشکل مواجه شد.'
  } finally {
    pageLoading.value = false
  }
}

async function loadMatches(showLoading = true) {
  if (showLoading) {
    matchesLoading.value = true
  }

  try {
    await propertiesStore.fetchMatches(route.params.id)
  } finally {
    matchesLoading.value = false
  }
}

function openEditModal() {
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
}

async function saveProperty(payload) {
  if (!property.value) {
    return
  }

  savingEdit.value = true

  const result = await propertiesStore.updateProperty(property.value.id, payload)

  savingEdit.value = false

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'ملک به‌روزرسانی شد',
      message: 'اطلاعات ملک با موفقیت ذخیره شد.'
    })

    closeEditModal()
  } else {
    ui.pushToast({
      type: 'error',
      title: 'به‌روزرسانی ملک ناموفق بود',
      message: propertiesStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

async function copyCode() {
  if (!property.value?.code) {
    return
  }

  try {
    await navigator.clipboard.writeText(property.value.code)

    ui.pushToast({
      type: 'success',
      title: 'کد ملک کپی شد',
      message: `کد ${property.value.code} در کلیپ‌بورد کپی شد.`
    })
  } catch (error) {
    ui.pushToast({
      type: 'error',
      title: 'کپی انجام نشد',
      message: 'مرورگر اجازه کپی در کلیپ‌بورد را نداد.'
    })
  }
}

async function publishProperty() {
  await changePropertyStatus('Published', 'ملک منتشر شد.')
}

async function archiveProperty() {
  await changePropertyStatus('Archived', 'ملک آرشیو شد.')
}

async function changePropertyStatus(status, message) {
  if (!property.value) {
    return
  }

  savingStatus.value = true

  const result = await propertiesStore.updateProperty(property.value.id, {
    status
  })

  savingStatus.value = false

  if (result) {
    ui.pushToast({
      type: 'success',
      title: 'وضعیت ملک به‌روزرسانی شد',
      message
    })
  } else {
    ui.pushToast({
      type: 'error',
      title: 'تغییر وضعیت ناموفق بود',
      message: propertiesStore.error || 'لطفاً دوباره تلاش کنید.'
    })
  }
}

function addImages(files) {
  const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
  const maxSize = 10 * 1024 * 1024

  Array.from(files).forEach((file, index) => {
    if (!validTypes.includes(file.type)) {
      ui.pushToast({
        type: 'error',
        title: 'فرمت فایل مجاز نیست',
        message: `فایل ${file.name} مجاز نیست.`
      })

      return
    }

    if (file.size > maxSize) {
      ui.pushToast({
        type: 'error',
        title: 'حجم فایل زیاد است',
        message: `فایل ${file.name} بیشتر از 10 مگابایت است.`
      })

      return
    }

    const image = {
      id: Date.now() + index,
      url: URL.createObjectURL(file),
      alt_text: file.name,
      is_primary: propertiesStore.images.length === 0,
      sort_order: propertiesStore.images.length + 1
    }

    propertiesStore.images.push(image)
  })

  if (propertiesStore.currentItem) {
    propertiesStore.currentItem.images = propertiesStore.images
  }

  ui.pushToast({
    type: 'success',
    title: 'تصاویر اضافه شدند',
    message: 'تصاویر به‌صورت موقت در حالت Mock اضافه شدند.'
  })
}

function setPrimaryImage(imageId) {
  propertiesStore.images = propertiesStore.images.map((image) => {
    return {
      ...image,
      is_primary: image.id === imageId
    }
  })

  ui.pushToast({
    type: 'success',
    title: 'تصویر اصلی انتخاب شد',
    message: 'تصویر اصلی ملک به‌روزرسانی شد.'
  })
}

function deleteImage(imageId) {
  const image = propertiesStore.images.find((item) => item.id === imageId)

  if (image && image.url.startsWith('blob:')) {
    URL.revokeObjectURL(image.url)
  }

  propertiesStore.images = propertiesStore.images.filter((item) => item.id !== imageId)

  if (image?.is_primary && propertiesStore.images.length > 0) {
    propertiesStore.images[0].is_primary = true
  }

  ui.pushToast({
    type: 'success',
    title: 'تصویر حذف شد',
    message: 'تصویر انتخاب‌شده حذف شد.'
  })
}

function moveImage(imageId, direction) {
  const index = propertiesStore.images.findIndex((item) => item.id === imageId)
  const targetIndex = index + direction

  if (index === -1 || targetIndex < 0 || targetIndex >= propertiesStore.images.length) {
    return
  }

  const items = [...propertiesStore.images]
  const [movedItem] = items.splice(index, 1)
  items.splice(targetIndex, 0, movedItem)

  propertiesStore.images = items.map((item, itemIndex) => {
    return {
      ...item,
      sort_order: itemIndex + 1
    }
  })
}

function goToClient(clientId) {
  router.push(`/clients/${clientId}`)
}
</script>
