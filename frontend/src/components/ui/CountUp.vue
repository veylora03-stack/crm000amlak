<template>
  <span class="inline-block" dir="ltr">
    <span v-if="prefix">{{ prefix }}</span>
    <span class="tabular-nums">{{ displayValue }}</span>
    <span v-if="suffix">{{ suffix }}</span>
  </span>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  endVal: { type: Number, required: true },
  duration: { type: Number, default: 1.5 },
  separator: { type: String, default: ',' },
  prefix: { type: String, default: '' },
  suffix: { type: String, default: '' }
})

const displayValue = ref('0')
let animationFrame = null
let startTime = null

function easeOutQuart(t) {
  return 1 - Math.pow(1 - t, 4)
}

function animate(timestamp) {
  if (!startTime) startTime = timestamp
  const elapsed = timestamp - startTime
  const progress = Math.min(elapsed / (props.duration * 1000), 1)

  const currentVal = Math.floor(easeOutQuart(progress) * props.endVal)
  displayValue.value = currentVal.toLocaleString('en-US').replace(/,/g, props.separator)

  if (progress < 1) {
    animationFrame = requestAnimationFrame(animate)
  }
}

onMounted(() => {
  animationFrame = requestAnimationFrame(animate)
})

watch(() => props.endVal, () => {
  if (animationFrame) cancelAnimationFrame(animationFrame)
  startTime = null
  animationFrame = requestAnimationFrame(animate)
})
</script>
