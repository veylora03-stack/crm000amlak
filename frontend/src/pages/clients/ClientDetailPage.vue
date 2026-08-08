<template>
  <AppLayout>
    <div class="page-container">
      <!-- Header -->
      <header class="mb-6">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div class="flex items-start gap-4">
            <div class="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-brand-500 to-accent-500 text-2xl font-bold text-white">
              {{ getInitials(client?.full_name) }}
            </div>
            <div>
              <h1 class="text-2xl font-bold tracking-tight">{{ client?.full_name || 'مشتری' }}</h1>
              <p class="mt-1 text-sm text-base-500">{{ client?.email || 'بدون ایمیل' }}</p>
              <div class="mt-2 flex items-center gap-2">
                <span :class="['badge badge-dot', statusBadge(client?.status)]">
                  {{ statusLabel(client?.status) }}
                </span>
                <span class="text-xs text-base-500">•</span>
                <span class="text-xs text-base-500">{{ customerTypeLabel(client?.customer_type) }}</span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button class="btn-secondary" @click="openEditModal">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              ویرایش
            </button>
            <button class="btn-brand">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              تماس
            </button>
          </div>
        </div>
      </header>

      <!-- Stats Cards -->
      <section class="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div class="card p-5">
          <p class="text-xs font-semibold uppercase tracking-wider text-base-500">معاملات فعال</p>
          <p class="mt-2 text-3xl font-bold tabular-nums" dir="ltr">{{ stats.activeDeals }}</p>
          <p class="mt-1 text-xs text-base-500">ارزش: {{ formatCurrency(stats.activeDealsValue) }}</p>
        </div>
        <div class="card p-5">
          <p class="text-xs font-semibold uppercase tracking-wider text-base-500">معاملات موفق</p>
          <p class="mt-2 text-3xl font-bold tabular-nums text-success-600" dir="ltr">{{ stats.wonDeals }}</p>
          <p class="mt-1 text-xs text-base-500">ارزش: {{ formatCurrency(stats.wonDealsValue) }}</p>
        </div>
        <div class="card p-5">
          <p class="text-xs font-semibold uppercase tracking-wider text-base-500">آخرین تماس</p>
          <p class="mt-2 text-lg font-semibold">{{ formatDate(stats.lastContact) }}</p>
          <p class="mt-1 text-xs text-base-500">{{ formatRelative(stats.lastContact) }}</p>
        </div>
        <div class="card p-5">
          <p class="text-xs font-semibold uppercase tracking-wider text-base-500">امتیاز مشتری</p>
          <p class="mt-2 text-3xl font-bold tabular-nums text-brand-600" dir="ltr">{{ stats.score }}/100</p>
          <div class="mt-2 h-2 overflow-hidden rounded-full bg-base-200">
            <div class="h-full rounded-full bg-gradient-to-r from-brand-500 to-accent-500" :style="{ width: stats.score + '%' }"></div>
          </div>
        </div>
      </section>

      <!-- Tabs -->
      <div class="card overflow-hidden">
        <div class="border-b border-app-border">
          <nav class="flex gap-6 px-6">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="[
                'relative py-4 text-sm font-semibold transition-colors',
                activeTab === tab.id
                  ? 'text-brand-600 after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-brand-600'
                  : 'text-base-500 hover:text-base-700'
              ]"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
              <span v-if="tab.count" class="ml-1.5 rounded-full bg-base-100 px-1.5 py-0.5 text-[10px] font-bold">
                {{ tab.count }}
              </span>
            </button>
          </nav>
        </div>

        <div class="p-6">
          <!-- Overview Tab -->
          <div v-if="activeTab === 'overview'" class="space-y-6">
            <div class="grid gap-6 lg:grid-cols-2">
              <div>
                <h3 class="mb-3 text-sm font-bold">اطلاعات تماس</h3>
                <dl class="space-y-3">
                  <div class="flex items-start gap-3">
                    <svg class="h-4 w-4 mt-0.5 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    <div>
                      <dt class="text-xs text-base-500">موبایل</dt>
                      <dd class="font-mono text-sm" dir="ltr">{{ client?.phone || '—' }}</dd>
                    </div>
                  </div>
                  <div class="flex items-start gap-3">
                    <svg class="h-4 w-4 mt-0.5 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    <div>
                      <dt class="text-xs text-base-500">ایمیل</dt>
                      <dd class="text-sm">{{ client?.email || '—' }}</dd>
                    </div>
                  </div>
                  <div class="flex items-start gap-3">
                    <svg class="h-4 w-4 mt-0.5 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <div>
                      <dt class="text-xs text-base-500">آدرس</dt>
                      <dd class="text-sm">{{ client?.address || '—' }}</dd>
                    </div>
                  </div>
                </dl>
              </div>
              <div>
                <h3 class="mb-3 text-sm font-bold">اطلاعات تجاری</h3>
                <dl class="space-y-3">
                  <div>
                    <dt class="text-xs text-base-500">منبع لید</dt>
                    <dd class="text-sm">{{ client?.source || '—' }}</dd>
                  </div>
                  <div>
                    <dt class="text-xs text-base-500">مسئول</dt>
                    <dd class="text-sm">{{ client?.assigned_agent || '—' }}</dd>
                  </div>
                  <div>
                    <dt class="text-xs text-base-500">تاریخ ایجاد</dt>
                    <dd class="text-sm">{{ formatDate(client?.created_at) }}</dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>

          <!-- Timeline Tab -->
          <div v-else-if="activeTab === 'timeline'">
            <ClientTimeline :client-id="clientId" />
          </div>

          <!-- Deals Tab -->
          <div v-else-if="activeTab === 'deals'">
            <ClientDeals :client-id="clientId" />
          </div>

          <!-- Notes Tab -->
          <div v-else-if="activeTab === 'notes'">
            <ClientNotes :client-id="clientId" />
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useClientsStore } from '@/stores/clients'
import { useJalaaliDate } from '@/composables/useJalaaliDate'
import AppLayout from '@/layouts/AppLayout.vue'
import ClientTimeline from '@/components/clients/ClientTimeline.vue'
import ClientDeals from '@/components/clients/ClientDeals.vue'
import ClientNotes from '@/components/clients/ClientNotes.vue'

const route = useRoute()
const clientsStore = useClientsStore()
const { formatDate, formatRelative } = useJalaaliDate()

const clientId = computed(() => route.params.id)
const client = computed(() => clientsStore.currentItem)
const activeTab = ref('overview')

const tabs = computed(() => [
  { id: 'overview', label: 'نمای کلی' },
  { id: 'timeline', label: 'تایم‌لاین', count: 12 },
  { id: 'deals', label: 'معاملات', count: stats.value.activeDeals + stats.value.wonDeals },
  { id: 'notes', label: 'یادداشت‌ها', count: 5 }
])

const stats = computed(() => ({
  activeDeals: 3,
  activeDealsValue: 2500000000,
  wonDeals: 2,
  wonDealsValue: 1800000000,
  lastContact: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
  score: 85
}))

onMounted(async () => {
  await clientsStore.fetchItem(clientId.value)
})

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

function formatCurrency(amount) {
  if (!amount) return '—'
  if (amount >= 1e9) return (amount / 1e9).toFixed(1) + 'B'
  if (amount >= 1e6) return (amount / 1e6).toFixed(1) + 'M'
  return amount.toLocaleString()
}

function statusBadge(status) {
  const map = {
    'New': 'badge-brand',
    'Contacted': 'badge-warning',
    'Qualified': 'badge-success',
    'Negotiating': 'badge-warning',
    'Won': 'badge-success',
    'Lost': 'badge-danger'
  }
  return map[status] || 'badge-neutral'
}

function statusLabel(status) {
  const map = {
    'New': 'جدید',
    'Contacted': 'تماس گرفته',
    'Qualified': 'واجد شرایط',
    'Negotiating': 'در حال مذاکره',
    'Won': 'برنده',
    'Lost': 'باخته'
  }
  return map[status] || status
}

function customerTypeLabel(type) {
  const map = {
    'Buyer': 'خریدار',
    'Seller': 'فروشنده',
    'Both': 'خریدار و فروشنده'
  }
  return map[type] || type
}

function openEditModal() {
  // TODO: Open edit modal
}
</script>
