<template>
  <Modal
    :open="open"
    :title="initial ? 'ویرایش ملک' : 'افزودن ملک'"
    size="xl"
    :closable="!loading"
    @close="closeModal"
  >
    <form novalidate @submit.prevent="submit">
      <div class="mb-4 rounded-md bg-secondary-100 p-3 text-sm text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300">
        اطلاعات ملک
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div>
          <label for="code" class="label-base">کد ملک *</label>
          <input id="code" v-model="form.code" type="text" class="input-base" dir="ltr" />
          <p v-if="errors.code" class="error-text">{{ errors.code }}</p>
        </div>

        <div>
          <label for="title" class="label-base">عنوان *</label>
          <input id="title" v-model="form.title" type="text" class="input-base" />
          <p v-if="errors.title" class="error-text">{{ errors.title }}</p>
        </div>

        <div>
          <label for="property_type" class="label-base">نوع ملک</label>
          <select id="property_type" v-model="form.property_type" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="type in propertyTypes" :key="type.id" :value="type.title">
              {{ type.title }}
            </option>
          </select>
        </div>

        <div>
          <label for="listing_type" class="label-base">نوع آگهی</label>
          <select id="listing_type" v-model="form.listing_type" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="listing in listingTypes" :key="listing.id" :value="listing.title">
              {{ listing.title }}
            </option>
          </select>
        </div>

        <div>
          <label for="status" class="label-base">وضعیت ملک</label>
          <select id="status" v-model="form.status" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="status in statuses" :key="status.id" :value="status.title">
              {{ status.title }}
            </option>
          </select>
        </div>

        <div>
          <label for="assigned_agent" class="label-base">Agent مسئول</label>
          <select id="assigned_agent" v-model="form.assigned_agent" class="input-base">
            <option value="">انتخاب کنید</option>
            <option v-for="agent in agents" :key="agent.id" :value="agent.full_name">
              {{ agent.full_name }}
            </option>
          </select>
        </div>
      </div>

      <div class="mb-4 mt-6 rounded-md bg-secondary-100 p-3 text-sm text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300">
        قیمت و متراژ
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div>
          <label for="price" class="label-base">قیمت</label>
          <input id="price" v-model.number="form.price" type="number" min="0" class="input-base" />
          <p v-if="errors.price" class="error-text">{{ errors.price }}</p>
        </div>

        <div>
          <label for="deposit_amount" class="label-base">مبلغ رهن</label>
          <input id="deposit_amount" v-model.number="form.deposit_amount" type="number" min="0" class="input-base" />
          <p v-if="errors.deposit_amount" class="error-text">{{ errors.deposit_amount }}</p>
        </div>

        <div>
          <label for="rent_amount" class="label-base">مبلغ اجاره</label>
          <input id="rent_amount" v-model.number="form.rent_amount" type="number" min="0" class="input-base" />
          <p v-if="errors.rent_amount" class="error-text">{{ errors.rent_amount }}</p>
        </div>

        <div>
          <label for="land_area" class="label-base">متراژ زمین</label>
          <input id="land_area" v-model.number="form.land_area" type="number" min="0" class="input-base" />
          <p v-if="errors.land_area" class="error-text">{{ errors.land_area }}</p>
        </div>

        <div>
          <label for="building_area" class="label-base">متراژ بنا</label>
          <input id="building_area" v-model.number="form.building_area" type="number" min="0" class="input-base" />
          <p v-if="errors.building_area" class="error-text">{{ errors.building_area }}</p>
        </div>

        <div>
          <label for="bedrooms" class="label-base">تعداد اتاق خواب</label>
          <input id="bedrooms" v-model.number="form.bedrooms" type="number" min="0" class="input-base" />
        </div>

        <div>
          <label for="bathrooms" class="label-base">تعداد حمام</label>
          <input id="bathrooms" v-model.number="form.bathrooms" type="number" min="0" class="input-base" />
        </div>

        <div>
          <label for="parking_count" class="label-base">تعداد پارکینگ</label>
          <input id="parking_count" v-model.number="form.parking_count" type="number" min="0" class="input-base" />
        </div>
      </div>

      <div class="mb-4 mt-6 rounded-md bg-secondary-100 p-3 text-sm text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300">
        جزئیات ساختمان
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div>
          <label for="floor_number" class="label-base">طبقه</label>
          <input id="floor_number" v-model.number="form.floor_number" type="number" class="input-base" />
        </div>

        <div>
          <label for="total_floors" class="label-base">تعداد طبقات</label>
          <input id="total_floors" v-model.number="form.total_floors" type="number" min="0" class="input-base" />
        </div>

        <div>
          <label for="year_built" class="label-base">سال ساخت</label>
          <input id="year_built" v-model.number="form.year_built" type="number" class="input-base" />
        </div>
      </div>

      <div class="mb-4 mt-6 rounded-md bg-secondary-100 p-3 text-sm text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300">
        موقعیت مکانی
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div>
          <label for="province" class="label-base">استان</label>
          <input id="province" v-model="form.province" type="text" class="input-base" />
        </div>

        <div>
          <label for="city" class="label-base">شهر</label>
          <input id="city" v-model="form.city" type="text" class="input-base" />
        </div>

        <div>
          <label for="district" class="label-base">منطقه</label>
          <input id="district" v-model="form.district" type="text" class="input-base" />
        </div>

        <div>
          <label for="neighborhood" class="label-base">محله</label>
          <input id="neighborhood" v-model="form.neighborhood" type="text" class="input-base" />
        </div>

        <div>
          <label for="latitude" class="label-base">Latitude</label>
          <input id="latitude" v-model.number="form.latitude" type="number" step="any" class="input-base" dir="ltr" />
        </div>

        <div>
          <label for="longitude" class="label-base">Longitude</label>
          <input id="longitude" v-model.number="form.longitude" type="number" step="any" class="input-base" dir="ltr" />
        </div>

        <div class="md:col-span-2 xl:col-span-3">
          <label for="address" class="label-base">آدرس</label>
          <input id="address" v-model="form.address" type="text" class="input-base" />
        </div>
      </div>

      <div class="mb-4 mt-6 rounded-md bg-secondary-100 p-3 text-sm text-secondary-700 dark:bg-secondary-800 dark:text-secondary-300">
        امکانات و توضیحات
      </div>

      <div class="grid gap-4">
        <div>
          <label for="amenities_text" class="label-base">امکانات رفاهی</label>
          <input
            id="amenities_text"
            v-model="form.amenities_text"
            type="text"
            class="input-base"
            placeholder="با کاما جدا کنید: آسانسور، پارکینگ، انباری"
          />
        </div>

        <div>
          <label for="description" class="label-base">توضیحات</label>
          <textarea id="description" v-model="form.description" rows="4" class="input-base"></textarea>
        </div>
      </div>
    </form>

    <template #footer>
      <div class="flex items-center justify-between gap-2">
        <button type="button" class="btn-secondary" :disabled="loading" @click="closeModal">
          انصراف
        </button>

        <button type="button" class="btn-primary" :disabled="loading" @click="submit">
          {{ loading ? 'در حال ذخیره...' : 'ذخیره' }}
        </button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import Modal from '@/components/ui/Modal.vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  initial: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  propertyTypes: {
    type: Array,
    default: () => []
  },
  listingTypes: {
    type: Array,
    default: () => []
  },
  statuses: {
    type: Array,
    default: () => []
  },
  agents: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'submit'])

const form = ref(buildEmptyForm())
const initialForm = ref(buildEmptyForm())
const errors = ref({})

const isDirty = computed(() => {
  return JSON.stringify(form.value) !== JSON.stringify(initialForm.value)
})

watch(
  () => props.open,
  (open) => {
    if (open) {
      resetForm()
    }
  }
)

function buildEmptyForm() {
  return {
    code: '',
    title: '',
    slug: '',
    property_type: '',
    listing_type: '',
    status: 'Draft',
    price: null,
    deposit_amount: null,
    rent_amount: null,
    land_area: null,
    building_area: null,
    bedrooms: null,
    bathrooms: null,
    parking_count: null,
    floor_number: null,
    total_floors: null,
    year_built: null,
    address: '',
    province: '',
    city: '',
    district: '',
    neighborhood: '',
    latitude: null,
    longitude: null,
    description: '',
    amenities_text: '',
    assigned_agent: ''
  }
}

function resetForm() {
  if (props.initial) {
    form.value = {
      code: props.initial.code || '',
      title: props.initial.title || '',
      slug: props.initial.slug || '',
      property_type: props.initial.property_type || '',
      listing_type: props.initial.listing_type || '',
      status: props.initial.status || 'Draft',
      price: props.initial.price ?? null,
      deposit_amount: props.initial.deposit_amount ?? null,
      rent_amount: props.initial.rent_amount ?? null,
      land_area: props.initial.land_area ?? null,
      building_area: props.initial.building_area ?? null,
      bedrooms: props.initial.bedrooms ?? null,
      bathrooms: props.initial.bathrooms ?? null,
      parking_count: props.initial.parking_count ?? null,
      floor_number: props.initial.floor_number ?? null,
      total_floors: props.initial.total_floors ?? null,
      year_built: props.initial.year_built ?? null,
      address: props.initial.address || '',
      province: props.initial.province || '',
      city: props.initial.city || '',
      district: props.initial.district || '',
      neighborhood: props.initial.neighborhood || '',
      latitude: props.initial.latitude ?? null,
      longitude: props.initial.longitude ?? null,
      description: props.initial.description || '',
      amenities_text: Array.isArray(props.initial.amenities)
        ? props.initial.amenities.join('، ')
        : '',
      assigned_agent: props.initial.assigned_agent || ''
    }
  } else {
    form.value = buildEmptyForm()
  }

  initialForm.value = JSON.parse(JSON.stringify(form.value))
  errors.value = {}
}

function parseList(value) {
  return String(value || '')
    .split(/[,،]/)
    .map((item) => item.trim())
    .filter(Boolean)
}

function validate() {
  const nextErrors = {}

  if (!form.value.code.trim()) {
    nextErrors.code = 'کد ملک الزامی است.'
  }

  if (!form.value.title.trim()) {
    nextErrors.title = 'عنوان ملک الزامی است.'
  }

  if (form.value.price !== null && form.value.price !== '' && Number(form.value.price) < 0) {
    nextErrors.price = 'قیمت نمی‌تواند منفی باشد.'
  }

  if (form.value.deposit_amount !== null && form.value.deposit_amount !== '' && Number(form.value.deposit_amount) < 0) {
    nextErrors.deposit_amount = 'مبلغ رهن نمی‌تواند منفی باشد.'
  }

  if (form.value.rent_amount !== null && form.value.rent_amount !== '' && Number(form.value.rent_amount) < 0) {
    nextErrors.rent_amount = 'مبلغ اجاره نمی‌تواند منفی باشد.'
  }

  if (form.value.land_area !== null && form.value.land_area !== '' && Number(form.value.land_area) < 0) {
    nextErrors.land_area = 'متراژ زمین نمی‌تواند منفی باشد.'
  }

  if (form.value.building_area !== null && form.value.building_area !== '' && Number(form.value.building_area) < 0) {
    nextErrors.building_area = 'متراژ بنا نمی‌تواند منفی باشد.'
  }

  errors.value = nextErrors
  return Object.keys(nextErrors).length === 0
}

function closeModal() {
  if (isDirty.value && !window.confirm('تغییرات ذخیره‌نشده دارید. آیا از بستن فرم مطمئن هستید؟')) {
    return
  }

  emit('close')
}

function submit() {
  if (!validate()) {
    return
  }

  const payload = {
    code: form.value.code.trim(),
    title: form.value.title.trim(),
    slug: form.value.slug.trim(),
    property_type: form.value.property_type,
    listing_type: form.value.listing_type,
    status: form.value.status,
    price: Number(form.value.price || 0),
    deposit_amount: Number(form.value.deposit_amount || 0),
    rent_amount: Number(form.value.rent_amount || 0),
    land_area: Number(form.value.land_area || 0),
    building_area: Number(form.value.building_area || 0),
    bedrooms: Number(form.value.bedrooms || 0),
    bathrooms: Number(form.value.bathrooms || 0),
    parking_count: Number(form.value.parking_count || 0),
    floor_number: form.value.floor_number,
    total_floors: form.value.total_floors,
    year_built: form.value.year_built,
    address: form.value.address,
    province: form.value.province,
    city: form.value.city,
    district: form.value.district,
    neighborhood: form.value.neighborhood,
    latitude: form.value.latitude,
    longitude: form.value.longitude,
    description: form.value.description,
    amenities: parseList(form.value.amenities_text),
    assigned_agent: form.value.assigned_agent
  }

  emit('submit', payload)
}
</script>
