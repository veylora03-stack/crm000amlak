<template>
  <ErrorBoundary>
    <ToastHost />
    <ModalHost />
    <CommandPalette />
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </ErrorBoundary>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUiStore } from '@/stores/ui'
import ErrorBoundary from '@/components/ui/ErrorBoundary.vue'
import ToastHost from '@/components/layout/ToastHost.vue'
import ModalHost from '@/components/layout/ModalHost.vue'
import CommandPalette from '@/components/layout/CommandPalette.vue'

const ui = useUiStore()
const { locale } = useI18n()

onMounted(() => {
  ui.initTheme()
  updateDir(locale.value)
})

// Watch for locale changes and update dir attribute
watch(locale, (newLocale) => {
  updateDir(newLocale)
})

function updateDir(loc) {
  const dir = loc === 'fa' ? 'rtl' : 'ltr'
  document.documentElement.setAttribute('dir', dir)
  document.documentElement.setAttribute('lang', loc)
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* RTL-specific adjustments */
[dir="rtl"] .ltr-icon {
  transform: scaleX(-1);
}
</style>
