<template>
  <AppLayout>
    <div class="page-container">
      <header class="mb-8">
        <div class="relative overflow-hidden rounded-3xl border border-app-border bg-gradient-to-br from-brand-500/5 via-accent-500/5 to-transparent p-6 sm:p-8 dark:border-app-border-dark">
          <div class="pointer-events-none absolute inset-0 overflow-hidden">
            <div class="absolute -top-32 -right-32 h-96 w-96 animate-pulse-subtle rounded-full bg-brand-500/20 blur-3xl"></div>
            <div class="absolute -bottom-32 -left-32 h-96 w-96 animate-pulse-subtle rounded-full bg-accent-500/15 blur-3xl" style="animation-delay: 1s"></div>
          </div>

          <div class="relative flex flex-wrap items-center justify-between gap-4">
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center gap-2 rounded-full bg-success-500/15 px-3 py-1 text-xs font-semibold text-success-700 dark:text-success-400">
                  <span class="relative flex h-2 w-2">
                    <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-success-400 opacity-75"></span>
                    <span class="relative inline-flex h-2 w-2 rounded-full bg-success-500"></span>
                  </span>
                  آنلاین
                </span>
                <span class="text-xs text-base-500 dark:text-base-400">{{ todayFormatted }}</span>
              </div>

              <h1 class="mt-3 text-2xl font-bold tracking-tight sm:text-3xl">
                سلام، <span class="gradient-text-premium">{{ auth.displayName }}</span> 👋
              </h1>
              <p class="mt-1.5 text-sm text-base-600 dark:text-base-300">
                امروز <span class="font-semibold">{{ formatNumber(tasksStore.todayTasks.length) }}</span> وظیفه و <span class="font-semibold">{{ formatNumber(tasksStore.overdueTasks.length) }}</span> مورد نیاز به پیگیری
              </p>
            </div>

            <div class="flex items-center gap-2">
              <button class="btn-secondary btn-sm sm:btn-md" @click="loadDashboard">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" :class="{ 'animate-spin': loading }">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span class="hidden sm:inline">به‌روزرسانی</span>
              </button>
              <button class="btn-brand btn-sm sm:btn-md">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <span class="hidden sm:inline">معامله جدید</span>
                <span class="sm:hidden">جدید</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <section class="mb-8">
        <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 class="text-xl font-bold tracking-tight sm:text-2xl">عملکرد کلیدی</h2>
            <p class="mt-1 text-sm text-base-500 dark:text-base-400">آمار لحظه‌ای کسب‌وکار شما</p>
          </div>
          <div class="flex items-center gap-0.5 rounded-xl border border-app-border bg-app-panel p-1 text-xs dark:border-app-border-dark">
            <button
              v-for="range in dateRanges"
              :key="range.value"
              :class="[
                'rounded-lg px-3 py-1.5 font-medium transition-all duration-200',
                selectedRange === range.value
                  ? 'bg-base-900 text-white shadow-md dark:bg-base-50 dark:text-base-900'
                  : 'text-base-600 hover:text-base-900 dark:text-base-400 dark:hover:text-base-100'
              ]"
              @click="selectedRange = range.value"
            >
              {{ range.label }}
            </button>
          </div>
        </div>

        <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="i in 4" :key="i" class="card p-5">
            <div class="skeleton h-3 w-24"></div>
            <div class="skeleton mt-3 h-8 w-32"></div>
            <div class="skeleton mt-2 h-3 w-20"></div>
          </div>
        </div>

        <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <UltraKpiCard
            v-for="kpi in primaryKpis"
            :key="kpi.title"
            v-bind="kpi"
          />
        </div>
      </section>

      <div class="grid gap-6 lg:grid-cols-3">
        <div class="card p-5 sm:p-6 lg:col-span-2">
          <div class="mb-5 flex flex-wrap items-start justify-between gap-3">
            <div>
              <h3 class="text-base font-bold tracking-tight sm:text-lg">روند معاملات</h3>
              <p class="mt-0.5 text-xs text-base-500 dark:text-base-400 sm:text-sm">ارزش معاملات در ۶ ماه اخیر</p>
            </div>
            <div class="flex items-center gap-3 text-xs">
              <div class="flex items-center gap-1.5">
                <span class="h-2 w-2 rounded-full bg-gradient-to-br from-brand-500 to-accent-500"></span>
                <span class="text-base-600 dark:text-base-400">معاملات</span>
              </div>
              <div class="flex items-center gap-1.5">
                <span class="h-2 w-2 rounded-full bg-success-500"></span>
                <span class="text-base-600 dark:text-base-400">موفق</span>
              </div>
            </div>
          </div>

          <div class="mb-5 grid grid-cols-3 gap-3 sm:gap-5">
            <div class="rounded-xl border border-app-border p-3 dark:border-app-border-dark sm:p-4">
              <p class="text-[10px] font-medium uppercase tracking-wider text-base-500 sm:text-xs">ارزش کل</p>
              <p class="mt-1.5 text-lg font-bold tracking-tight tabular-nums sm:text-2xl" dir="ltr">۱۸۵B</p>
              <span class="kpi-delta-up mt-1.5 inline-flex items-center gap-0.5 text-[10px] sm:text-xs">
                <svg class="h-2.5 w-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                </svg>
                ۱۲٪
              </span>
            </div>
            <div class="rounded-xl border border-app-border p-3 dark:border-app-border-dark sm:p-4">
              <p class="text-[10px] font-medium uppercase tracking-wider text-base-500 sm:text-xs">تعداد</p>
              <p class="mt-1.5 text-lg font-bold tracking-tight tabular-nums sm:text-2xl" dir="ltr">۲۴</p>
              <span class="kpi-delta-up mt-1.5 inline-flex items-center gap-0.5 text-[10px] sm:text-xs">
                <svg class="h-2.5 w-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                </svg>
                ۸٪
              </span>
            </div>
            <div class="rounded-xl border border-app-border p-3 dark:border-app-border-dark sm:p-4">
              <p class="text-[10px] font-medium uppercase tracking-wider text-base-500 sm:text-xs">میانگین</p>
              <p class="mt-1.5 text-lg font-bold tracking-tight tabular-nums sm:text-2xl" dir="ltr">۷.۷B</p>
              <span class="kpi-delta-up mt-1.5 inline-flex items-center gap-0.5 text-[10px] sm:text-xs">
                <svg class="h-2.5 w-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                </svg>
                ۴٪
              </span>
            </div>
          </div>

          <ChartCard
            title=""
            type="area"
            :height="280"
            :options="chartOptions"
            :series="chartSeries"
          />
        </div>

        <div class="card p-5 sm:p-6">
          <div class="mb-5 flex items-start justify-between gap-2">
            <div class="min-w-0">
              <h3 class="text-base font-bold tracking-tight sm:text-lg">وضعیت پایپ‌لاین</h3>
              <p class="mt-0.5 text-xs text-base-500 sm:text-sm">معاملات فعال</p>
            </div>
            <RouterLink to="/pipeline" class="flex-shrink-0 text-xs font-bold text-brand-600 hover:text-brand-700 dark:text-brand-400">
              مشاهده همه ←
            </RouterLink>
          </div>

          <div class="space-y-4">
            <div v-for="stage in pipelineStages" :key="stage.name">
              <div class="mb-1.5 flex items-center justify-between gap-2">
                <div class="flex min-w-0 items-center gap-2">
                  <div
                    class="h-2.5 w-2.5 flex-shrink-0 rounded-full"
                    :style="{ backgroundColor: stage.color, boxShadow: `0 0 0 3px ${stage.color}20` }"
                  ></div>
                  <span class="truncate text-xs font-semibold text-base-800 dark:text-base-200 sm:text-sm">{{ stage.name }}</span>
                </div>
                <div class="flex items-baseline gap-1">
                  <span class="text-base font-bold tabular-nums sm:text-lg" dir="ltr">{{ stage.count }}</span>
                  <span class="text-[10px] text-base-500">/{{ stage.total }}</span>
                </div>
              </div>
              <div class="relative h-1.5 overflow-hidden rounded-full bg-base-200 dark:bg-base-800">
                <div
                  class="absolute inset-y-0 rounded-full transition-all duration-700 ease-out"
                  :style="{
                    width: stage.percent + '%',
                    backgroundColor: stage.color,
                    boxShadow: `0 0 12px ${stage.color}60`
                  }"
                ></div>
              </div>
            </div>
          </div>

          <div class="divider my-5"></div>

          <div class="rounded-xl bg-gradient-to-br from-brand-500/10 to-accent-500/10 p-3 sm:p-4">
            <p class="text-[10px] font-medium uppercase tracking-wider text-base-600 sm:text-xs">ارزش کل پایپ‌لاین</p>
            <p class="mt-1.5 text-lg font-bold tracking-tight tabular-nums sm:text-2xl" dir="ltr">۲۴۵B</p>
          </div>
        </div>
      </div>

      <div class="mt-6 grid gap-6 lg:grid-cols-3">
        <div class="card p-5 sm:p-6 lg:col-span-2">
          <div class="mb-5 flex flex-wrap items-start justify-between gap-3">
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-base font-bold tracking-tight sm:text-lg">وظایف امروز</h3>
                <span class="rounded-full bg-base-900 px-2 py-0.5 text-[10px] font-bold text-white dark:bg-base-50 dark:text-base-900">
                  {{ tasksStore.todayTasks.length }}
                </span>
              </div>
              <p class="mt-0.5 text-xs text-base-500 sm:text-sm">برنامه‌ریزی شده برای امروز</p>
            </div>
            <RouterLink to="/tasks" class="btn-secondary btn-sm">
              همه ←
            </RouterLink>
          </div>

          <div v-if="tasksStore.todayTasks.length === 0 && tasksStore.overdueTasks.length === 0" class="flex flex-col items-center justify-center py-12 text-center">
            <div class="mb-3 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-brand-500/20 to-accent-500/20">
              <svg class="h-8 w-8 text-brand-600 dark:text-brand-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p class="text-base font-semibold">امروز کار خاصی ندارید! 🎉</p>
            <p class="mt-1 text-sm text-base-500">از وقتت استفاده کن</p>
          </div>

          <ul v-else class="space-y-2.5">
            <li
              v-for="task in [...tasksStore.overdueTasks, ...tasksStore.todayTasks].slice(0, 6)"
              :key="task.id"
              :class="[
                'group flex items-center gap-3 rounded-xl border p-3 transition-all duration-200 hover:-translate-y-0.5 sm:p-4',
                task.due_date < todayKey
                  ? 'border-danger-500/30 bg-danger-500/5'
                  : 'border-app-border hover:border-base-300 hover:shadow-md dark:border-app-border-dark dark:hover:border-base-700'
              ]"
            >
              <button
                type="button"
                class="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-md border-2 border-base-300 transition-all hover:border-brand-500 hover:scale-110 dark:border-base-600"
                @click="tasksStore.completeTask(task.id)"
              >
                <svg class="h-3 w-3 text-transparent transition-colors group-hover:text-brand-500" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
                </svg>
              </button>

              <div class="min-w-0 flex-1">
                <p class="truncate text-sm font-semibold text-base-900 dark:text-base-100">{{ task.title }}</p>
                <div class="mt-0.5 flex flex-wrap items-center gap-2 text-xs text-base-500">
                  <span v-if="task.due_time" class="flex items-center gap-1">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span dir="ltr">{{ task.due_time }}</span>
                  </span>
                  <span v-if="task.client_id" class="flex items-center gap-1">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    مشتری
                  </span>
                </div>
              </div>

              <span :class="['badge flex-shrink-0', priorityBadge(task.priority)]">{{ task.priority }}</span>
            </li>
          </ul>
        </div>

        <div class="card p-5 sm:p-6">
          <div class="mb-5">
            <h3 class="text-base font-bold tracking-tight sm:text-lg">فعالیت‌های اخیر</h3>
            <p class="mt-0.5 text-xs text-base-500 sm:text-sm">آخرین رویدادها</p>
          </div>

          <ol class="relative space-y-4 pr-4 before:absolute before:bottom-0 before:right-[7px] before:top-0 before:w-0.5 before:bg-gradient-to-b before:from-app-border before:to-transparent dark:before:from-app-border-dark">
            <li v-for="activity in recentActivities" :key="activity.id" class="relative">
              <span
                class="absolute -right-[13px] flex h-5 w-5 items-center justify-center rounded-full border-2 text-[10px]"
                :class="activity.emoji.includes('✅') ? 'border-success-500 bg-success-500/10' : 'border-app-panel bg-base-900 text-white dark:border-app-panel-dark dark:bg-base-50 dark:text-base-900'"
              >
                {{ activity.emoji }}
              </span>
              <p class="text-xs leading-relaxed font-medium sm:text-sm">{{ activity.title }}</p>
              <p class="mt-0.5 text-[11px] text-base-500 sm:text-xs">
                {{ activity.user }} · {{ activity.time }}
              </p>
            </li>
          </ol>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { delay } from '@/utils/delay'
import { formatNumber, formatCurrency } from '@/utils/format'
import { useTasksStore } from '@/stores/tasks'
import { useNotificationsStore } from '@/stores/notifications'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'
import UltraKpiCard from '@/components/dashboard/UltraKpiCard.vue'
import ChartCard from '@/components/dashboard/ChartCard.vue'

const tasksStore = useTasksStore()
const notificationsStore = useNotificationsStore()
const auth = useAuthStore()

const loading = ref(true)
const selectedRange = ref('week')

const dateRanges = [
  { label: 'امروز', value: 'today' },
  { label: 'هفته', value: 'week' },
  { label: 'ماه', value: 'month' },
  { label: 'سال', value: 'year' }
]

const today = new Date()
const todayKey = today.toISOString().slice(0, 10)
const todayFormatted = new Intl.DateTimeFormat('fa-IR', {
  weekday: 'long',
  day: 'numeric',
  month: 'long'
}).format(today)

const primaryKpis = [
  {
    title: 'معاملات فعال',
    value: '24',
    icon: '💼',
    change: '+12%',
    changeTone: 'success',
    to: '/deals',
    sparklineData: [12, 18, 15, 22, 19, 24, 28],
    sparklineColor: 'theme("colors.chart.emerald")',
    progress: 75
  },
  {
    title: 'مشتریان جدید',
    value: '18',
    icon: '👥',
    change: '+8%',
    changeTone: 'success',
    to: '/clients',
    badge: 'جدید',
    badgeVariant: 'badge-success',
    sparklineData: [8, 12, 10, 15, 13, 18, 20],
    sparklineColor: 'theme("colors.chart.cyan")'
  },
  {
    title: 'ارزش پایپ‌لاین',
    value: '245000000000',
    icon: '💰',
    change: '+24%',
    changeTone: 'success',
    to: '/pipeline',
    suffix: ' T',
    sparklineData: [180, 195, 210, 225, 240, 245, 260],
    sparklineColor: 'theme("colors.chart.amber")'
  },
  {
    title: 'املاک فعال',
    value: '42',
    icon: '🏠',
    change: '-3%',
    changeTone: 'danger',
    to: '/properties',
    sparklineData: [48, 46, 45, 44, 43, 42, 41],
    sparklineColor: 'theme("colors.chart.red")'
  }
]

const pipelineStages = [
  { name: 'لید جدید', color: 'theme("colors.chart.indigo")', count: 8, total: 24, percent: 33, value: 82000000000 },
  { name: 'تماس اولیه', color: 'theme("colors.chart.violet")', count: 6, total: 24, percent: 25, value: 65000000000 },
  { name: 'نیازسنجی', color: 'theme("colors.chart.emerald")', count: 5, total: 24, percent: 21, value: 58000000000 },
  { name: 'بازدید', color: 'theme("colors.chart.amber")', count: 3, total: 24, percent: 13, value: 28000000000 },
  { name: 'مذاکره', color: 'theme("colors.chart.red")', count: 2, total: 24, percent: 8, value: 12000000000 }
]

const recentActivities = [
  { id: 1, emoji: '📞', title: 'تماس با علی رضایی ثبت شد', user: 'مدیر سیستم', time: '۵ دقیقه پیش' },
  { id: 2, emoji: '💼', title: 'معامله «آپارتمان سعادت‌آباد» منتقل شد', user: 'مدیر سیستم', time: '۲۰ دقیقه پیش' },
  { id: 3, emoji: '🏠', title: 'ملک «ویلای لواسان» ایجاد شد', user: 'مدیر سیستم', time: '۱ ساعت پیش' },
  { id: 4, emoji: '✅', title: 'وظیفه «پیگیری قرارداد» تکمیل شد', user: 'کارشناس فروش', time: '۲ ساعت پیش' }
]

const chartOptions = {
  chart: {
    fontFamily: 'Vazirmatn, sans-serif',
    toolbar: { show: false },
    zoom: { enabled: false },
    background: 'transparent'
  },
  colors: ['theme("colors.chart.emerald")'],
  stroke: { curve: 'smooth', width: 3, lineCap: 'round' },
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'light',
      type: 'vertical',
      opacityFrom: 0.4,
      opacityTo: 0.05,
      stops: [0, 90, 100]
    }
  },
  dataLabels: { enabled: false },
  grid: {
    borderColor: 'rgba(113, 113, 122, 0.1)',
    strokeDashArray: 4,
    xaxis: { lines: { show: false } },
    yaxis: { lines: { show: true } }
  },
  xaxis: {
    categories: ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور'],
    labels: { style: { colors: '#71717a', fontSize: '11px', fontWeight: 500 } },
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  yaxis: {
    labels: {
      style: { colors: '#71717a', fontSize: '11px', fontWeight: 500 },
      formatter: (v) => (v / 1000000000).toFixed(0) + 'B'
    }
  },
  tooltip: {
    theme: 'light',
    x: { show: true },
    y: { formatter: (v) => formatCurrency(v) }
  }
}

const chartSeries = [
  {
    name: 'ارزش معاملات',
    data: [9800000000, 12500000000, 15200000000, 13400000000, 17800000000, 21000000000]
  }
]

function priorityBadge(p) {
  if (p === 'Urgent') return 'badge-danger'
  if (p === 'High') return 'badge-warning'
  if (p === 'Medium') return 'badge-neutral'
  return 'badge-brand'
}

onMounted(async () => {
  await Promise.all([
    delay(600),
    tasksStore.fetchTasks().catch(() => {}),
    notificationsStore.fetchNotifications().catch(() => {})
  ])
  loading.value = false
})

async function loadDashboard() {
  loading.value = true
  await delay(500)
  loading.value = false
}
</script>

<style scoped>
.gradient-text-premium {
  background: linear-gradient(135deg, theme("colors.chart.emerald") 0%, theme("colors.chart.cyan") 50%, theme("colors.chart.violet") 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>


