<template>
  <div
    v-if="open"
    class="fixed inset-0 z-modal flex items-center justify-center p-4"
    role="dialog"
    aria-modal="true"
    :aria-label="title"
  >
    <div class="absolute inset-0 bg-black/50" @click="onOverlayClick"></div>

    <div :class="['card relative w-full p-0 shadow-xl', sizeClass]">
      <div class="flex items-center justify-between border-b border-border-light p-4 dark:border-border-dark">
        <h2 class="text-lg font-semibold text-text-primary-light dark:text-text-primary-dark">
          {{ title }}
        </h2>

        <button
          v-if="closable"
          type="button"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md text-text-secondary-light hover:bg-secondary-100 dark:text-text-secondary-dark dark:hover:bg-secondary-800"
          aria-label="بستن"
          @click="$emit('close')"
        >
          ×
        </button>
      </div>

      <div class="max-h-[70vh] overflow-y-auto p-4">
        <slot />
      </div>

      <div
        v-if="$slots.footer"
        class="border-t border-border-light p-4 dark:border-border-dark"
      >
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch, onUnmounted } from 'vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md'
  },
  closable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const sizeClass = computed(() => {
  if (props.size === 'sm') {
    return 'max-w-modal-sm'
  }

  if (props.size === 'lg') {
    return 'max-w-modal-lg'
  }

  if (props.size === 'xl') {
    return 'max-w-modal-xl'
  }

  return 'max-w-modal-md'
})

function onOverlayClick() {
  if (props.closable) {
    emit('close')
  }
}

function onKeydown(event) {
  if (event.key === 'Escape' && props.open && props.closable) {
    emit('close')
  }
}

watch(
  () => props.open,
  (open) => {
    if (open) {
      document.addEventListener('keydown', onKeydown)
    } else {
      document.removeEventListener('keydown', onKeydown)
    }
  },
  { immediate: true }
)

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
})
</script>
