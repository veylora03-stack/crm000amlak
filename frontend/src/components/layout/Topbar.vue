<template>
  <header
    class="fixed left-0 right-0 top-0 z-sticky flex h-14 items-center justify-between border-b border-app-border-light bg-app-panel-light/80 px-6 backdrop-blur-xl dark:border-app-border-dark dark:bg-app-panel-dark/80 lg:right-[240px]"
  >
    <div class="flex items-center gap-3">
      <button
        type="button"
        class="flex h-8 w-8 items-center justify-center rounded-md text-base-500 hover:bg-app-hover hover:text-base-800 dark:hover:text-base-200 lg:hidden"
        @click="ui.openSidebar"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <!-- Breadcrumbs -->
      <nav v-if="breadcrumbs.length > 0" class="hidden items-center gap-1.5 text-sm sm:flex">
        <template v-for="(crumb, idx) in breadcrumbs" :key="idx">
          <span v-if="idx > 0" class="text-base-400">/</span>
          <RouterLink
            v-if="crumb.to"
            :to="crumb.to"
            class="text-base-500 hover:text-base-900 dark:text-base-400 dark:hover:text-base-100"
          >
            {{ crumb.label }}
          </RouterLink>
          <span v-else class="font-medium text-base-900 dark:text-base-100">
            {{ crumb.label }}
          </span>
        </template>
      </nav>
    </div>

    <div class="flex items-center gap-1">
      <button
        type="button"
        class="flex h-8 w-8 items-center justify-center rounded-md text-base-500 hover:bg-app-hover hover:text-base-800 dark:hover:text-base-200"
        @click="ui.toggleTheme"
        :aria-label="ui.resolvedTheme === 'dark' ? 'روشن کن' : 'تیره کن'"
      >
        <svg v-if="ui.resolvedTheme === 'dark'" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </button>

      <NotificationDropdown />
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUiStore } from '@/stores/ui'
import NotificationDropdown from '@/components/notifications/NotificationDropdown.vue'

const ui = useUiStore()
const route = useRoute()

const breadcrumbs = computed(() => {
  const matched = route.matched || []
  const crumbs = []
  matched.forEach((r) => {
    if (r.meta?.title) {
      crumbs.push({
        label: r.meta.title,
        to: r.path.includes(':') ? undefined : r.path
      })
    }
  })
  return crumbs
})
</script>
