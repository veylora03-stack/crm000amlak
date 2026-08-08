<template>
  <div class="flex flex-wrap items-center gap-3">
    <label for="pipeline-select" class="label-base mb-0">پایپ‌لاین</label>

    <select
      id="pipeline-select"
      class="input-base w-auto"
      :value="modelValue"
      @change="$emit('update:modelValue', Number($event.target.value))"
    >
      <option
        v-for="pipeline in pipelines"
        :key="pipeline.id"
        :value="pipeline.id"
      >
        {{ pipeline.name }}
      </option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Number,
    default: null
  },
  pipelines: {
    type: Array,
    default: () => []
  }
})

defineEmits(['update:modelValue'])
</script>
