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
import { onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import ErrorBoundary from '@/components/ui/ErrorBoundary.vue'
import ToastHost from '@/components/layout/ToastHost.vue'
import ModalHost from '@/components/layout/ModalHost.vue'
import CommandPalette from '@/components/layout/CommandPalette.vue'

const ui = useUiStore()

onMounted(() => {
  ui.initTheme()
})
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
</style>
