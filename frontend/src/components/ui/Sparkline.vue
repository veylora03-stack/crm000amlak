<template>
  <svg
    :viewBox="`0 0 ${width} ${height}`"
    :width="width"
    :height="height"
    class="sparkline"
    preserveAspectRatio="none"
  >
    <defs>
      <linearGradient :id="gradientId" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" :stop-color="color" stop-opacity="0.3" />
        <stop offset="100%" :stop-color="color" stop-opacity="0" />
      </linearGradient>
    </defs>

    <path
      v-if="showArea"
      :d="areaPath"
      :fill="`url(#${gradientId})`"
    />

    <path
      :d="linePath"
      fill="none"
      :stroke="color"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true,
    validator: (val) => val.length > 1
  },
  width: { type: Number, default: 80 },
  height: { type: Number, default: 32 },
  color: { type: String, default: '#10b981' },
  showArea: { type: Boolean, default: true }
})

const gradientId = computed(() => `spark-${Math.random().toString(36).substr(2, 9)}`)

const points = computed(() => {
  const data = props.data
  const max = Math.max(...data)
  const min = Math.min(...data)
  const range = max - min || 1

  return data.map((value, index) => {
    const x = (index / (data.length - 1)) * props.width
    const y = props.height - ((value - min) / range) * (props.height - 4) - 2
    return { x, y }
  })
})

const linePath = computed(() => {
  if (points.value.length < 2) return ''

  let path = `M ${points.value[0].x} ${points.value[0].y}`

  for (let i = 1; i < points.value.length; i++) {
    const prev = points.value[i - 1]
    const curr = points.value[i]
    const cpx = (prev.x + curr.x) / 2
    path += ` Q ${cpx} ${prev.y}, ${(prev.x + curr.x) / 2} ${(prev.y + curr.y) / 2}`
    path += ` T ${curr.x} ${curr.y}`
  }

  return path
})

const areaPath = computed(() => {
  if (points.value.length < 2) return ''

  let path = `M ${points.value[0].x} ${props.height}`
  path += ` L ${points.value[0].x} ${points.value[0].y}`

  for (let i = 1; i < points.value.length; i++) {
    const prev = points.value[i - 1]
    const curr = points.value[i]
    const cpx = (prev.x + curr.x) / 2
    path += ` Q ${cpx} ${prev.y}, ${(prev.x + curr.x) / 2} ${(prev.y + curr.y) / 2}`
    path += ` T ${curr.x} ${curr.y}`
  }

  path += ` L ${points.value[points.value.length - 1].x} ${props.height}`
  path += ' Z'

  return path
})
</script>

<style scoped>
.sparkline {
  overflow: visible;
}
</style>
