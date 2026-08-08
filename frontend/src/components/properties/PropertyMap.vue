<template>
  <section>
    <div
      v-if="!hasCoordinates"
      class="flex flex-col items-center justify-center gap-3 rounded-md border border-dashed border-border-light py-14 text-center dark:border-border-dark"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        موقعیت مکانی برای این ملک ثبت نشده است.
      </p>
    </div>

    <div v-else class="h-96 overflow-hidden rounded-md border border-border-light dark:border-border-dark">
      <LMap
        :zoom="14"
        :center="center"
        :use-global-leaflet="false"
      >
        <LTileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="© OpenStreetMap contributors"
        />

        <LCircleMarker
          :lat-lng="center"
          :radius="10"
          color="#2563eb"
          fill-color="#2563eb"
          :fill-opacity="0.8"
        />
      </LMap>
    </div>

    <p v-if="hasCoordinates" class="mt-2 text-xs text-text-secondary-light dark:text-text-secondary-dark">
      Latitude: <span dir="ltr">{{ latitude }}</span> — Longitude: <span dir="ltr">{{ longitude }}</span>
    </p>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { LMap, LTileLayer, LCircleMarker } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  latitude: {
    type: Number,
    default: null
  },
  longitude: {
    type: Number,
    default: null
  }
})

const hasCoordinates = computed(() => {
  return props.latitude !== null && props.longitude !== null
})

const center = computed(() => {
  return [props.latitude || 35.7219, props.longitude || 51.3347]
})
</script>
