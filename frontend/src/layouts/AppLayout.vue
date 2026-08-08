<template>
  <div class="min-h-screen bg-background-light text-text-primary-light dark:bg-background-dark dark:text-text-primary-dark">
    <Sidebar />
    <Topbar />

    <main id="main-content" class="min-h-screen pt-16 lg:ps-[264px]">
      <div class="page-container">
        <slot />
      </div>
    </main>

    <ModalHost />
    <CommandPalette />
  </div>
</template>

<script setup>
import Sidebar from '@/components/layout/Sidebar.vue'
import Topbar from '@/components/layout/Topbar.vue'
import ModalHost from '@/components/layout/ModalHost.vue'
import CommandPalette from '@/components/search/CommandPalette.vue'
</script>
