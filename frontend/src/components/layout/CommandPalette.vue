<template>
  <div
    v-if="ui.commandPaletteOpen"
    class="fixed inset-0 z-command-palette bg-black/50 p-4"
    @click.self="ui.closeCommandPalette"
  >
    <div class="mx-auto mt-20 w-full max-w-command-palette rounded-lg border border-border-light bg-surface-light shadow-xl dark:border-border-dark dark:bg-surface-dark">
      <div class="border-b border-border-light p-3 dark:border-border-dark">
        <input
          ref="searchInput"
          v-model="query"
          type="text"
          placeholder="جستجوی سریع..."
          class="input-base"
          aria-label="جستجوی سریع"
          @keyup.esc="ui.closeCommandPalette"
        />
      </div>

      <div class="p-4 text-sm text-text-secondary-light dark:text-text-secondary-dark">
        <p v-if="!query">
          برای جستجو در مشتریان، املاک، معاملات و وظایف تایپ کنید.
        </p>
        <p v-else>
          نتیجه‌ای یافت نشد.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const query = ref('')
const searchInput = ref(null)

watch(
  () => ui.commandPaletteOpen,
  async (open) => {
    if (open) {
      query.value = ''
      await nextTick()
      searchInput.value?.focus()
    }
  }
)

function handleKeydown(event) {
  if (event.ctrlKey && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    ui.toggleCommandPalette()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>
