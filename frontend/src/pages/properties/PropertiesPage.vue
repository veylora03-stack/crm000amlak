<template>
  <AppLayout>
    <div class="page-container">
      <!-- Hero Header -->
      <header class="page-header">
        <div class="relative overflow-hidden rounded-2xl border border-app-border bg-gradient-to-br from-accent-500/5 via-brand-500/5 to-transparent p-6 dark:border-app-border-dark">
          <div class="pointer-events-none absolute -top-24 -left-24 h-64 w-64 rounded-full bg-accent-500/15 blur-3xl" aria-hidden="true"></div>
          <div class="relative flex flex-wrap items-center justify-between gap-4">
            <div>
              <h1 class="text-2xl font-bold tracking-tight sm:text-3xl">
                <span class="gradient-text-premium">املاک</span>
              </h1>
              <p class="mt-1 text-sm text-base-500 dark:text-base-400">
                مدیریت <span class="font-semibold tabular-nums">{{ formatNumber(propertiesStore.total) }}</span> ملک در سیستم
              </p>
            </div>
            <div class="flex items-center gap-2">
              <button class="btn-secondary">
                <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span class="hidden sm:inline">خروجی</span>
              </button>
              <button class="btn-secondary">
                <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                <span class="hidden sm:inline">ورود</span>
              </button>
              <button class="btn-brand" @click="openCreateModal">
                <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <span>ملک جدید</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Quick Stats -->
      <section class="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div class="card p-4">
          <p class="text-[11px] font-semibold uppercase tracking-wider text-base-500">کل املاک</p>
          <p class="mt-1.5 text-2xl font-bold tabular-nums" dir="ltr">{{ formatNumber(propertiesStore.total) }}</p>
        </div>
        <div class="card p-4">
          <p class="text-[11px] font-semibold uppercase tracking-wider text-base-500">منتشر شده</p>
          <p class="mt-1.5 text-2xl font-bold tabular-nums text-success-600 dark:text-success-400" dir="ltr">۳۸</p>
        </div>
        <div class="card p-4">
          <p class="text-[11px] font-semibold uppercase tracking-wider text-base-500">فروخته شده</p>
          <p class="mt-1.5 text-2xl font-bold tabular-nums text-brand-600 dark:text-brand-400" dir="ltr">۱۲</p>
        </div>
        <div class="card p-4">
          <p class="text-[11px] font-semibold uppercase tracking-wider text-base-500">ارزش کل</p>
          <p class="mt-1.5 text-2xl font-bold tabular-nums" dir="ltr">۱۸۵B</p>
        </div>
      </section>

      <!-- Search & Filter Bar -->
      <div class="card mb-4 p-2">
        <div class="flex flex-wrap items-center gap-2">
          <!-- Search -->
          <div class="relative min-w-[200px] flex-1">
            <svg class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              class="input !border-0 !bg-transparent !pr-9 focus:!ring-0"
              placeholder="جستجو در کد، عنوان، آدرس..."
              @input="onSearch"
            />
          </div>

          <div class="h-6 w-px bg-app-border dark:bg-app-border-dark"></div>

          <!-- View Toggle -->
          <div class="flex items-center gap-0.5 rounded-lg border border-app-border bg-app-panel p-0.5 dark:border-app-border-dark">
            <button
              :class="['rounded-md px-2.5 py-1 transition-all', viewMode === 'grid' ? 'bg-base-900 text-white dark:bg-base-50 dark:text-base-900' : 'text-base-500 hover:text-base-800 dark:hover:text-base-200']"
              @click="viewMode = 'grid'"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </button>
            <button
              :class="['rounded-md px-2.5 py-1 transition-all', viewMode === 'list' ? 'bg-base-900 text-white dark:bg-base-50 dark:text-base-900' : 'text-base-500 hover:text-base-800 dark:hover:text-base-200']"
              @click="viewMode = 'list'"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
            </button>
          </div>

          <button class="btn-ghost" @click="toggleFilters">
            <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            فیلترها
            <span v-if="activeFilterCount > 0" class="rounded-full bg-brand-600 px-1.5 text-[10px] font-bold text-white">
              {{ activeFilterCount }}
            </span>
          </button>
        </div>

        <!-- Quick Filter Chips -->
        <div class="mt-3 flex flex-wrap gap-2">
          <button
            v-for="chip in quickChips"
            :key="chip.value"
            :class="[
              'inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium transition-all',
              selectedChip === chip.value
                ? 'bg-base-900 text-white shadow-sm dark:bg-base-50 dark:text-base-900'
                : 'bg-base-100 text-base-700 hover:bg-base-200 dark:bg-base-800 dark:text-base-300 dark:hover:bg-base-700'
            ]"
            @click="selectChip(chip.value)"
          >
            <span>{{ chip.icon }}</span>
            {{ chip.label }}
          </button>
        </div>
      </div>

      <!-- Active Filters -->
      <div v-if="hasActiveFilters" class="mb-4 flex flex-wrap items-center gap-2">
        <span class="text-xs text-base-500">فیلترهای فعال:</span>
        <button
          v-for="pill in activeFilterPills"
          :key="pill.key"
          class="group inline-flex items-center gap-1 rounded-full bg-base-100 px-2.5 py-1 text-xs font-medium text-base-700 transition-colors hover:bg-base-200 dark:bg-base-800 dark:text-base-200 dark:hover:bg-base-700"
          @click="removeFilter(pill.key)"
        >
          {{ pill.label }}
          <svg class="h-3 w-3 opacity-60 group-hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <button class="text-xs font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400" @click="clearAllFilters">
          پاک کردن همه
        </button>
      </div>

      <!-- Properties Grid -->
      <div v-if="propertiesStore.loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <div v-for="i in 8" :key="i" class="card overflow-hidden">
          <div class="skeleton aspect-video"></div>
          <div class="p-4 space-y-2">
            <div class="skeleton h-3 w-16"></div>
            <div class="skeleton h-5 w-full"></div>
            <div class="skeleton h-4 w-2/3"></div>
          </div>
        </div>
      </div>

      <div v-else-if="propertiesStore.error" class="flex flex-col items-center justify-center gap-3 py-16 text-center">
        <div class="flex h-16 w-16 items-center justify-center rounded-full bg-danger-500/10">
          <svg class="h-8 w-8 text-danger-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <p class="font-semibold">{{ propertiesStore.error }}</p>
        <button class="btn-secondary" @click="applyFilters">تلاش مجدد</button>
      </div>

      <div v-else-if="propertiesStore.items.length === 0" class="flex flex-col items-center justify-center gap-3 py-20 text-center">
        <div class="flex h-20 w-20 items-center justify-center rounded-full bg-base-100 dark:bg-base-800">
          <svg class="h-10 w-10 text-base-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
        </div>
        <p class="text-lg font-semibold">هنوز ملکی ثبت نشده</p>
        <p class="max-w-sm text-sm text-base-500">اولین ملک خود را اضافه کنید و شروع به مدیریت املاک کنید</p>
        <button class="btn-brand mt-2" @click="openCreateModal">
          <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          افزودن اولین ملک
        </button>
      </div>

      <div v-else-if="viewMode === 'grid'" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <article
          v-for="property in propertiesStore.items"
          :key="property.id"
          class="group relative overflow-hidden rounded-2xl border border-app-border bg-app-panel transition-all duration-300 hover:-translate-y-1 hover:border-base-300 hover:shadow-xl dark:border-app-border-dark dark:hover:border-base-700"
          @click="goToDetail(property)"
        >
          <!-- Image -->
          <div class="relative aspect-video overflow-hidden bg-base-100 dark:bg-base-800">
            <img
              v-if="property.primary_image"
              :src="property.primary_image.image"
              :alt="property.title"
              class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            />
            <div v-else class="flex h-full w-full items-center justify-center">
              <svg class="h-12 w-12 text-base-300 dark:text-base-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>

            <!-- Status Badge -->
            <div class="absolute right-2 top-2">
              <span :class="['badge rounded-lg px-2 py-1 text-[10px] font-bold backdrop-blur-sm', statusBadge(property.status)]">
                {{ statusLabel(property.status) }}
              </span>
            </div>

            <!-- Type Badge -->
            <div class="absolute left-2 top-2">
              <span class="rounded-lg bg-black/50 px-2 py-1 text-[10px] font-bold text-white backdrop-blur-sm">
                {{ property.property_type }}
              </span>
            </div>

            <!-- Favorite Button -->
            <button
              type="button"
              class="absolute bottom-2 left-2 flex h-8 w-8 items-center justify-center rounded-full bg-white/90 text-base-700 shadow-sm transition-all hover:bg-white hover:text-danger-600 dark:bg-base-900/90 dark:text-base-200 dark:hover:bg-base-900"
              @click.stop="toggleFavorite(property)"
            >
              <svg class="h-4 w-4" :fill="property.is_favorite ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24" :class="{ 'text-danger-500': property.is_favorite }">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </button>
          </div>

          <!-- Content -->
          <div class="p-4">
            <div class="mb-2 flex items-center gap-2">
              <span class="font-mono text-[10px] text-base-500 dark:text-base-400" dir="ltr">{{ property.code }}</span>
              <span class="h-1 w-1 rounded-full bg-base-300 dark:bg-base-600"></span>
              <span class="text-[10px] text-base-500">{{ property.city }}</span>
            </div>

            <h3 class="line-clamp-1 text-sm font-bold text-base-900 dark:text-base-50">
              {{ property.title }}
            </h3>

            <p class="mt-1 line-clamp-1 text-xs text-base-500">
              {{ property.district }} - {{ property.address || 'آدرس نامشخص' }}
            </p>

            <div class="divider my-3"></div>

            <!-- Features -->
            <div class="mb-3 flex items-center gap-3 text-xs text-base-600 dark:text-base-400">
              <div class="flex items-center gap-1">
                <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span class="tabular-nums" dir="ltr">{{ property.building_area || 0 }}m²</span>
              </div>
              <div class="flex items-center gap-1">
                <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                <span class="tabular-nums" dir="ltr">{{ property.bedrooms || 0 }}</span>
              </div>
              <div class="flex items-center gap-1">
                <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
                </svg>
                <span class="tabular-nums" dir="ltr">{{ property.bathrooms || 0 }}</span>
              </div>
            </div>

            <!-- Price -->
            <div class="flex items-baseline justify-between">
              <div>
                <p class="text-[10px] text-base-500">{{ property.listing_type === 'فروش' ? 'قیمت' : 'ودیعه' }}</p>
                <p class="text-base font-bold tracking-tight text-brand-600 dark:text-brand-400 tabular-nums" dir="ltr">
                  {{ formatPriceShort(property.listing_type === 'فروش' ? property.price : property.deposit_amount) }}
                </p>
              </div>
              <button
                type="button"
                class="rounded-lg p-2 text-base-400 transition-colors hover:bg-base-100 hover:text-brand-600 dark:hover:bg-base-800"
                @click.stop="openMenu($event, property)"
              >
                <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                  <circle cx="12" cy="5" r="1.5" />
                  <circle cx="12" cy="12" r="1.5" />
                  <circle cx="12" cy="19" r="1.5" />
                </svg>
              </button>
            </div>
          </div>
        </article>
      </div>

      <!-- List View -->
      <div v-else class="card overflow-hidden">
        <table class="data-table">
          <thead>
            <tr>
              <th class="w-10"><input type="checkbox" class="h-3.5 w-3.5 rounded border-base-300" /></th>
              <th>ملک</th>
              <th>کد</th>
              <th>نوع</th>
              <th>متراژ</th>
              <th>قیمت</th>
              <th>وضعیت</th>
              <th>مسئول</th>
              <th class="text-left">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="property in propertiesStore.items"
              :key="property.id"
              class="cursor-pointer"
              @click="goToDetail(property)"
            >
              <td><input type="checkbox" class="h-3.5 w-3.5 rounded border-base-300" @click.stop /></td>
              <td>
                <div class="flex items-center gap-3">
                  <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-base-100 text-base-400 dark:bg-base-800">
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                    </svg>
                  </div>
                  <div class="min-w-0">
                    <p class="truncate font-semibold">{{ property.title }}</p>
                    <p class="truncate text-xs text-base-500">{{ property.city }} - {{ property.district }}</p>
                  </div>
                </div>
              </td>
              <td class="font-mono text-xs" dir="ltr">{{ property.code }}</td>
              <td class="text-xs">{{ property.property_type }}</td>
              <td class="tabular-nums text-xs" dir="ltr">{{ property.building_area }}m²</td>
              <td class="font-semibold tabular-nums text-brand-600 dark:text-brand-400 text-xs" dir="ltr">
                {{ formatPriceShort(property.price) }}
              </td>
              <td>
                <span :class="['badge badge-dot', statusBadge(property.status)]">{{ statusLabel(property.status) }}</span>
              </td>
              <td class="text-xs">{{ property.assigned_agent || '—' }}</td>
              <td class="text-left">
                <div class="flex items-center justify-end gap-1" @click.stop>
                  <button class="btn-icon btn-ghost" @click.stop="openEditModal(property)">
                    <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button class="btn-icon btn-ghost hover:!text-danger-600" @click.stop="confirmDelete(property)">
                    <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="border-t border-app-border p-4 dark:border-app-border-dark">
          <Pagination
            :page="propertiesStore.page"
            :page-size="propertiesStore.pageSize"
            :total="propertiesStore.total"
            :loading="propertiesStore.loading"
            @change="changePage"
          />
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from '@/utils/debounce'
import { formatNumber } from '@/utils/format'
import { usePropertiesStore } from '@/stores/properties'
import { useUiStore } from '@/stores/ui'
import AppLayout from '@/layouts/AppLayout.vue'
import Pagination from '@/components/ui/Pagination.vue'

const router = useRouter()
const propertiesStore = usePropertiesStore()
const ui = useUiStore()

const searchQuery = ref('')
const viewMode = ref('grid')
const selectedChip = ref('all')

const quickChips = [
  { value: 'all', label: 'همه', icon: '📊' },
  { value: 'published', label: 'منتشر شده', icon: '✅' },
  { value: 'draft', label: 'پیش‌نویس', icon: '📝' },
  { value: 'sold', label: 'فروخته شده', icon: '💰' },
  { value: 'rented', label: 'اجاره داده', icon: '🔑' },
  { value: 'apartment', label: 'آپارتمان', icon: '🏢' },
  { value: 'villa', label: 'ویلا', icon: '🏡' }
]

const hasActiveFilters = computed(() => Object.values(propertiesStore.filters).some(v => v))
const activeFilterCount = computed(() => Object.values(propertiesStore.filters).filter(v => v).length)

const activeFilterPills = computed(() => {
  const pills = []
  const f = propertiesStore.filters
  if (f.status) pills.push({ key: 'status', label: `وضعیت: ${f.status}` })
  if (f.property_type) pills.push({ key: 'property_type', label: `نوع: ${f.property_type}` })
  if (f.city) pills.push({ key: 'city', label: `شهر: ${f.city}` })
  return pills
})

onMounted(() => {
  propertiesStore.fetchProperties()
})

const debouncedSearch = debounce(() => applyFilters(), 300)

function onSearch() {
  debouncedSearch()
}

function applyFilters() {
  propertiesStore.setFilter('search', searchQuery.value)
  propertiesStore.fetchProperties()
}

function selectChip(value) {
  selectedChip.value = value
  
  // Reset filters first
  propertiesStore.resetFilters()
  
  // Apply chip filter
  if (value === 'published') propertiesStore.setFilter('publish_status', 'Published')
  else if (value === 'draft') propertiesStore.setFilter('status', 'Draft')
  else if (value === 'sold') propertiesStore.setFilter('status', 'Sold')
  else if (value === 'rented') propertiesStore.setFilter('status', 'Rented')
  else if (value === 'apartment') propertiesStore.setFilter('property_type', 'آپارتمان')
  else if (value === 'villa') propertiesStore.setFilter('property_type', 'ویلا')
  
  propertiesStore.fetchProperties()
}

function removeFilter(key) {
  propertiesStore.setFilter(key, '')
  propertiesStore.fetchProperties()
}

function clearAllFilters() {
  propertiesStore.resetFilters()
  selectedChip.value = 'all'
  searchQuery.value = ''
  propertiesStore.fetchProperties()
}

function changePage(page) {
  propertiesStore.setPage(page)
  propertiesStore.fetchProperties()
}

function openCreateModal() {
  ui.pushToast({ type: 'info', title: 'Modal ملک جدید در حال توسعه است' })
}

function openEditModal(property) {
  ui.pushToast({ type: 'info', title: `ویرایش ${property.title}` })
}

function confirmDelete(property) {
  ui.pushToast({ type: 'warning', title: `تایید حذف ${property.title}` })
}

function goToDetail(property) {
  router.push(`/properties/${property.id}`)
}

function toggleFavorite(property) {
  property.is_favorite = !property.is_favorite
  ui.pushToast({ type: 'success', title: property.is_favorite ? 'به علاقه‌مندی‌ها اضافه شد' : 'از علاقه‌مندی‌ها حذف شد' })
}

function openMenu(event, property) {
  event.stopPropagation()
  ui.pushToast({ type: 'info', title: `منو برای ${property.title}` })
}

function statusBadge(status) {
  const map = {
    'Published': 'badge-success',
    'Draft': 'badge-neutral',
    'Sold': 'badge-brand',
    'Rented': 'badge-warning',
    'Reserved': 'badge-warning',
    'Expired': 'badge-danger',
    'Archived': 'badge-neutral'
  }
  return map[status] || 'badge-neutral'
}

function statusLabel(status) {
  const map = {
    'Published': 'منتشر شده',
    'Draft': 'پیش‌نویس',
    'Sold': 'فروخته شده',
    'Rented': 'اجاره داده',
    'Reserved': 'رزرو شده',
    'Expired': 'منقضی',
    'Archived': 'آرشیو'
  }
  return map[status] || status
}

function formatPriceShort(price) {
  if (!price) return 'توافقی'
  if (price >= 1000000000000) return (price / 1000000000000).toFixed(1) + 'T'
  if (price >= 1000000000) return (price / 1000000000).toFixed(1) + 'B'
  if (price >= 1000000) return (price / 1000000).toFixed(1) + 'M'
  return formatNumber(price)
}
</script>

<style scoped>
.gradient-text-premium {
  background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 50%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
