<template>
  <div v-if="open" class="fixed inset-0 z-drawer">
    <div class="absolute inset-0 bg-black/50" @click="onOverlayClick"></div>

    <aside
      :class="[
        'absolute inset-y-0 flex w-full max-w-drawer flex-col border-border-light bg-surface-light shadow-xl dark:border-border-dark dark:bg-surface-dark',
        side === 'left' ? 'left-0 border-r' : 'right-0 border-l'
      ]"
      role="dialog"
      aria-modal="true"
      :aria-label="title"
    >
      <div class="flex h-16 items-center justify-between border-b border-border-light px-4 dark:border-border-dark">
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

      <div class="flex-1 overflow-y-auto p-4">
        <slot />
      </div>

      <div
        v-if="$slots.footer"
        class="border-t border-border-light p-4 dark:border-border-dark"
      >
        <slot name="footer" />
      </div>
    </aside>
  </div>
</template>

<script setup>
import { watch, onUnmounted } from 'vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  side: {
    type: String,
    default: 'left'
  },
  closable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

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
