<template>
  <div
    v-if="ui.sidebarOpen"
    class="fixed inset-0 z-sidebar-mobile bg-black/50 backdrop-blur-sm lg:hidden"
    @click="ui.closeSidebar"
  ></div>

  <aside
    :class="[
      'fixed inset-y-0 right-0 z-sidebar-mobile flex w-[240px] flex-col border-l border-app-border-light bg-app-panel-light transition-transform duration-200 dark:border-app-border-dark dark:bg-app-panel-dark',
      'lg:z-sidebar lg:w-[240px] lg:translate-x-0',
      ui.sidebarOpen ? 'translate-x-0' : 'translate-x-full'
    ]"
  >
    <!-- Logo -->
    <div class="flex h-14 items-center gap-2.5 border-b border-app-border-light px-4 dark:border-app-border-dark">
      <div class="flex h-7 w-7 items-center justify-center rounded-md bg-gradient-to-br from-brand-500 to-brand-700 text-white shadow-sm">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </div>
      <div class="flex-1">
        <p class="text-sm font-bold tracking-tight">املاک CRM</p>
        <p class="text-[10px] text-base-500 dark:text-base-400">Professional</p>
      </div>
      <button
        type="button"
        class="flex h-6 w-6 items-center justify-center rounded-md text-base-500 hover:bg-app-hover hover:text-base-800 dark:hover:text-base-200 lg:hidden"
        @click="ui.closeSidebar"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Search trigger -->
    <div class="px-3 pt-3">
      <button
        type="button"
        class="flex w-full items-center gap-2 rounded-md border border-app-border-light bg-app-subtle-light px-2.5 py-1.5 text-xs text-base-500 hover:border-base-300 hover:text-base-700 dark:border-app-border-dark dark:bg-app-subtle-dark dark:hover:border-base-700 dark:hover:text-base-300"
        @click="ui.openCommandPalette"
      >
        <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <span class="flex-1 text-right">جستجو...</span>
        <kbd class="rounded border border-app-border-light bg-app-panel-light px-1 py-0.5 text-[10px] font-mono dark:border-app-border-dark dark:bg-app-panel-dark">⌘K</kbd>
      </button>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto px-3 py-3">
      <div class="mb-4">
        <p class="mb-1.5 px-2 text-[10px] font-semibold uppercase tracking-wider text-base-500 dark:text-base-400">
          اصلی
        </p>
        <ul class="space-y-0.5">
          <li v-for="item in mainMenu" :key="item.to">
            <RouterLink
              :to="item.to"
              :class="[
                'group flex items-center gap-2.5 rounded-md px-2 py-1.5 text-sm transition-colors duration-100',
                isActive(item)
                  ? 'bg-base-900 text-white dark:bg-base-50 dark:text-base-900'
                  : 'text-base-700 hover:bg-app-hover hover:text-base-900 dark:text-base-300 dark:hover:text-base-100'
              ]"
              @click="ui.closeSidebar"
            >
              <span class="flex h-4 w-4 items-center justify-center" v-html="item.icon" aria-hidden="true"></span>
              <span class="flex-1">{{ item.title }}</span>
              <span
                v-if="item.badge"
                class="rounded-full bg-brand-500/15 px-1.5 py-0.5 text-[10px] font-bold text-brand-700 dark:text-brand-300"
              >
                {{ item.badge }}
              </span>
            </RouterLink>
          </li>
        </ul>
      </div>

      <div class="mb-4">
        <p class="mb-1.5 px-2 text-[10px] font-semibold uppercase tracking-wider text-base-500 dark:text-base-400">
          مدیریت
        </p>
        <ul class="space-y-0.5">
          <li v-for="item in managementMenu" :key="item.to">
            <RouterLink
              :to="item.to"
              :class="[
                'group flex items-center gap-2.5 rounded-md px-2 py-1.5 text-sm transition-colors duration-100',
                isActive(item)
                  ? 'bg-base-900 text-white dark:bg-base-50 dark:text-base-900'
                  : 'text-base-700 hover:bg-app-hover hover:text-base-900 dark:text-base-300 dark:hover:text-base-100'
              ]"
              @click="ui.closeSidebar"
            >
              <span class="flex h-4 w-4 items-center justify-center" v-html="item.icon" aria-hidden="true"></span>
              <span class="flex-1">{{ item.title }}</span>
            </RouterLink>
          </li>
        </ul>
      </div>

      <div v-if="auth.isAdmin">
        <p class="mb-1.5 px-2 text-[10px] font-semibold uppercase tracking-wider text-base-500 dark:text-base-400">
          سیستم
        </p>
        <ul class="space-y-0.5">
          <li v-for="item in systemMenu" :key="item.to">
            <RouterLink
              :to="item.to"
              :class="[
                'group flex items-center gap-2.5 rounded-md px-2 py-1.5 text-sm transition-colors duration-100',
                isActive(item)
                  ? 'bg-base-900 text-white dark:bg-base-50 dark:text-base-900'
                  : 'text-base-700 hover:bg-app-hover hover:text-base-900 dark:text-base-300 dark:hover:text-base-100'
              ]"
              @click="ui.closeSidebar"
            >
              <span class="flex h-4 w-4 items-center justify-center" v-html="item.icon" aria-hidden="true"></span>
              <span class="flex-1">{{ item.title }}</span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </nav>

    <!-- User card -->
    <div class="border-t border-app-border-light p-3 dark:border-app-border-dark">
      <div class="flex items-center gap-2.5 rounded-md px-1.5 py-1.5 hover:bg-app-hover">
        <div class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-accent-400 to-brand-500 text-xs font-bold text-white">
          {{ auth.displayName.slice(0, 1) }}
        </div>
        <div class="min-w-0 flex-1">
          <p class="truncate text-sm font-semibold">{{ auth.displayName }}</p>
          <p class="truncate text-[10px] text-base-500 dark:text-base-400">{{ auth.role }}</p>
        </div>
        <button
          type="button"
          class="flex h-6 w-6 items-center justify-center rounded text-base-400 hover:text-base-700 dark:hover:text-base-200"
          @click="logout"
          aria-label="خروج"
        >
          <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUiStore } from '@/stores/ui'
import { useAuthStore } from '@/stores/auth'

const ui = useUiStore()
const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const icon = (d) => `<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`

const mainMenu = [
  { to: '/dashboard', title: 'داشبورد',     icon: icon('<rect x="3" y="3" width="7" height="9"></rect><rect x="14" y="3" width="7" height="5"></rect><rect x="14" y="12" width="7" height="9"></rect><rect x="3" y="16" width="7" height="5"></rect>') },
  { to: '/pipeline',  title: 'پایپ‌لاین',   icon: icon('<line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line>') },
  { to: '/clients',   title: 'مشتریان',     icon: icon('<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 00-3-3.87"></path><path d="M16 3.13a4 4 0 010 7.75"></path>') },
  { to: '/properties',title: 'املاک',       icon: icon('<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline>') },
  { to: '/deals',     title: 'معاملات',     icon: icon('<line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>') },
  { to: '/tasks',     title: 'وظایف',       icon: icon('<path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>') }
]

const managementMenu = [
  { to: '/reports',       title: 'گزارش‌ها',      icon: icon('<line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>') },
  { to: '/notifications', title: 'نوتیفیکیشن',    icon: icon('<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>') },
  { to: '/profile',       title: 'پروفایل',       icon: icon('<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle>') }
]

const systemMenu = [
  { to: '/users',    title: 'کاربران',  icon: icon('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle>') },
  { to: '/settings', title: 'تنظیمات',  icon: icon('<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>') }
]

function isActive(item) {
  if (route.path === item.to) return true
  return route.path.startsWith(item.to + '/')
}

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
