<template>
  <section class="card mb-6 p-4">
    <form class="grid gap-4 md:grid-cols-2 xl:grid-cols-5" @submit.prevent="$emit('apply')">
      <div>
        <label for="property-search" class="label-base">جستجو</label>
        <input
          id="property-search"
          :value="modelValue.search"
          type="text"
          class="input-base"
          placeholder="کد، عنوان، آدرس یا شهر"
          @input="setField('search', $event.target.value)"
        />
      </div>

      <div>
        <label for="property-type" class="label-base">نوع ملک</label>
        <select
          id="property-type"
          :value="modelValue.property_type"
          class="input-base"
          @change="setField('property_type', $event.target.value)"
        >
          <option value="">همه انواع</option>
          <option v-for="type in propertyTypes" :key="type.id" :value="type.title">
            {{ type.title }}
          </option>
        </select>
      </div>

      <div>
        <label for="listing-type" class="label-base">نوع آگهی</label>
        <select
          id="listing-type"
          :value="modelValue.listing_type"
          class="input-base"
          @change="setField('listing_type', $event.target.value)"
        >
          <option value="">همه آگهی‌ها</option>
          <option v-for="listing in listingTypes" :key="listing.id" :value="listing.title">
            {{ listing.title }}
          </option>
        </select>
      </div>

      <div>
        <label for="property-status" class="label-base">وضعیت ملک</label>
        <select
          id="property-status"
          :value="modelValue.status"
          class="input-base"
          @change="setField('status', $event.target.value)"
        >
          <option value="">همه وضعیت‌ها</option>
          <option v-for="status in statuses" :key="status.id" :value="status.title">
            {{ status.title }}
          </option>
        </select>
      </div>

      <div>
        <label for="property-city" class="label-base">شهر</label>
        <input
          id="property-city"
          :value="modelValue.city"
          type="text"
          class="input-base"
          placeholder="مثلاً تهران"
          @input="setField('city', $event.target.value)"
        />
      </div>

      <div class="flex flex-wrap items-center gap-2 xl:col-span-5">
        <button type="submit" class="btn-primary">
          اعمال فیلترها
        </button>

        <button type="button" class="btn-secondary" @click="$emit('reset')">
          حذف فیلترها
        </button>
      </div>
    </form>
  </section>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
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
  }
})

const emit = defineEmits(['update:modelValue', 'apply', 'reset'])

function setField(field, value) {
  emit('update:modelValue', {
    ...props.modelValue,
    [field]: value
  })
}
</script>
