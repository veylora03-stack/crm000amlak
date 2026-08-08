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
          v-model="searchQuery"
          type="text"
          placeholder="جستجوی سریع... (Ctrl+K)"
          class="input-base"
          aria-label="جستجوی سراسری"
          @input="onSearchInput"
          @keyup.esc="ui.closeCommandPalette"
        />
      </div>

      <div class="max-h-96 overflow-y-auto p-3">
        <SearchResults
          :loading="loading"
          :has-searched="hasSearched"
          :has-results="hasResults"
          :client-results="clientResults"
          :property-results="propertyResults"
          :deal-results="dealResults"
          :task-results="taskResults"
          @select="onSelectResult"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from '@/utils/debounce'
import { useUiStore } from '@/stores/ui'
import { useGlobalSearch } from '@/composables/useGlobalSearch'
import SearchResults from '@/components/search/SearchResults.vue'

const ui = useUiStore()
const router = useRouter()

const {
  loading,
  hasSearched,
  clientResults,
  propertyResults,
  dealResults,
  taskResults,
  hasResults,
  search,
  clearSearch
} = useGlobalSearch()

const searchQuery = ref('')
const searchInput = ref(null)

const debouncedSearch = debounce((value) => {
  search(value)
}, 300)

function onSearchInput() {
  debouncedSearch(searchQuery.value)
}

function onSelectResult(result) {
  ui.closeCommandPalette()

  if (result.type === 'client') {
    router.push(`/clients/${result.item.id}`)
  } else if (result.type === 'property') {
    router.push(`/properties/${result.item.id}`)
  } else if (result.type === 'deal') {
    router.push('/deals')
  } else if (result.type === 'task') {
    router.push('/tasks')
  }
}

watch(
  () => ui.commandPaletteOpen,
  async (open) => {
    if (open) {
      searchQuery.value = ''
      clearSearch()
      await nextTick()
      searchInput.value?.focus()
    }
  }
)
</script>
