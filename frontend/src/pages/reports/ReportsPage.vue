<template>
  <AppLayout>
    <PageHeader title="گزارش‌ها" description="گزارش‌گیری، فیلتر و خروجی Excel/CSV">
      <template #actions>
        <ExportButton
          :columns="visibleColumns"
          :rows="reportRows"
          :report-type="filters.report_type"
        />
      </template>
    </PageHeader>

    <ReportFilters
      v-model="filters"
      :report-types="reportTypes"
      :status-options="statusOptions"
      :responsible-options="responsibleOptions"
      :source-options="sourceOptions"
      :columns-options="reportColumns"
      :selected-columns="selectedColumns"
      @apply="applyReport"
      @reset="resetFilters"
      @toggle-column="toggleColumn"
    />

    <div class="mb-6">
      <ReportCharts
        :report-type="filters.report_type"
        :rows="reportRows"
        :loading="loading"
      />
    </div>

    <ReportTable
      :columns="visibleColumns"
      :rows="reportRows"
      :loading="loading"
      :error="error"
      @retry="applyReport"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { delay } from '@/utils/delay'
import { useClientsStore } from '@/stores/clients'
import { useDealsStore } from '@/stores/deals'
import { usePropertiesStore } from '@/stores/properties'
import { useTasksStore } from '@/stores/tasks'
import { useSettingsStore } from '@/stores/settings'
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import ReportFilters from '@/components/reports/ReportFilters.vue'
import ReportTable from '@/components/reports/ReportTable.vue'
import ReportCharts from '@/components/reports/ReportCharts.vue'
import ExportButton from '@/components/reports/ExportButton.vue'

const clientsStore = useClientsStore()
const dealsStore = useDealsStore()
const propertiesStore = usePropertiesStore()
const tasksStore = useTasksStore()
const settingsStore = useSettingsStore()

const loading = ref(true)
const error = ref('')
const reportRows = ref([])
const selectedColumns = ref([])

const filters = ref({
  report_type: 'leads',
  date_from: '',
  date_to: '',
  status: '',
  responsible: '',
  source: ''
})

const reportTypes = [
  { value: 'leads', label: 'گزارش لیدها' },
  { value: 'deals', label: 'گزارش Dealها' },
  { value: 'agents', label: 'گزارش عملکرد Agentها' },
  { value: 'funnel', label: 'گزارش Funnel' },
  { value: 'properties', label: 'گزارش املاک' },
  { value: 'interactions', label: 'گزارش تعامل‌ها' },
  { value: 'tasks', label: 'گزارش وظایف' }
]

const reportColumns = computed(() => {
  if (filters.value.report_type === 'leads') {
    return [
      { key: 'full_name', label: 'نام مشتری' },
      { key: 'phone', label: 'موبایل' },
      { key: 'source', label: 'منبع' },
      { key: 'status', label: 'وضعیت' },
      { key: 'customer_type', label: 'نوع مشتری' },
      { key: 'assigned_agent', label: 'مسئول' },
      { key: 'created_at', label: 'تاریخ ایجاد' }
    ]
  }

  if (filters.value.report_type === 'deals') {
    return [
      { key: 'title', label: 'عنوان معامله' },
      { key: 'client_name', label: 'مشتری' },
      { key: 'property_title', label: 'ملک' },
      { key: 'stage_name', label: 'Stage' },
      { key: 'amount', label: 'مبلغ' },
      { key: 'agent', label: 'Agent' },
      { key: 'status', label: 'وضعیت' },
      { key: 'expected_close_date', label: 'تاریخ تخمینی' }
    ]
  }

  if (filters.value.report_type === 'agents') {
    return [
      { key: 'agent', label: 'Agent' },
      { key: 'deals_count', label: 'تعداد Deal' },
      { key: 'won_count', label: 'برنده' },
      { key: 'lost_count', label: 'بازنده' },
      { key: 'total_amount', label: 'ارزش Dealها' },
      { key: 'win_rate', label: 'نرخ برد' }
    ]
  }

  if (filters.value.report_type === 'funnel') {
    return [
      { key: 'stage', label: 'Stage' },
      { key: 'deals_count', label: 'تعداد Deal' },
      { key: 'total_amount', label: 'ارزش Dealها' },
      { key: 'conversion', label: 'درصد از کل' }
    ]
  }

  if (filters.value.report_type === 'properties') {
    return [
      { key: 'code', label: 'کد ملک' },
      { key: 'title', label: 'عنوان' },
      { key: 'property_type', label: 'نوع ملک' },
      { key: 'listing_type', label: 'نوع آگهی' },
      { key: 'status', label: 'وضعیت' },
      { key: 'price', label: 'قیمت' },
      { key: 'city', label: 'شهر' },
      { key: 'assigned_agent', label: 'Agent' },
      { key: 'created_at', label: 'تاریخ ایجاد' }
    ]
  }

  if (filters.value.report_type === 'interactions') {
    return [
      { key: 'interaction_type', label: 'نوع تعامل' },
      { key: 'title', label: 'عنوان' },
      { key: 'client_name', label: 'مشتری' },
      { key: 'agent', label: 'Agent' },
      { key: 'occurred_at', label: 'تاریخ وقوع' },
      { key: 'needs_followup', label: 'نیاز به پیگیری' }
    ]
  }

  return [
    { key: 'title', label: 'عنوان وظیفه' },
    { key: 'assigned_user', label: 'مسئول' },
    { key: 'priority', label: 'اولویت' },
    { key: 'status', label: 'وضعیت' },
    { key: 'due_date', label: 'تاریخ سررسید' },
    { key: 'due_time', label: 'ساعت سررسید' },
    { key: 'completed_at', label: 'تاریخ انجام' }
  ]
})

const visibleColumns = computed(() => {
  return reportColumns.value.filter((column) => selectedColumns.value.includes(column.key))
})

const statusOptions = computed(() => {
  if (filters.value.report_type === 'leads') {
    return settingsStore.lookups.clientStatuses.map((item) => item.title)
  }

  if (filters.value.report_type === 'deals') {
    return ['Open', 'Won', 'Lost']
  }

  if (filters.value.report_type === 'properties') {
    return settingsStore.lookups.propertyStatuses.map((item) => item.title)
  }

  if (filters.value.report_type === 'tasks') {
    return settingsStore.lookups.taskStatuses.map((item) => item.title)
  }

  return []
})

const responsibleOptions = computed(() => {
  return settingsStore.users.map((user) => user.full_name)
})

const sourceOptions = computed(() => {
  if (filters.value.report_type === 'leads' || filters.value.report_type === 'deals') {
    return settingsStore.lookups.leadSources.map((item) => item.title)
  }

  return []
})

onMounted(async () => {
  try {
    await Promise.all([
      settingsStore.fetchUsers(),
      clientsStore.fetchClients(),
      dealsStore.fetchPipelines(),
      dealsStore.fetchStages(),
      dealsStore.fetchDeals(),
      propertiesStore.fetchProperties(),
      tasksStore.fetchTasks()
    ])

    selectedColumns.value = reportColumns.value.map((column) => column.key)
    await applyReport()
  } catch (e) {
    error.value = 'دریافت اطلاعات گزارش با مشکل مواجه شد.'
  } finally {
    loading.value = false
  }
})

watch(
  () => filters.value.report_type,
  () => {
    selectedColumns.value = reportColumns.value.map((column) => column.key)
  }
)

function toggleColumn(columnKey) {
  if (selectedColumns.value.includes(columnKey)) {
    if (selectedColumns.value.length > 1) {
      selectedColumns.value = selectedColumns.value.filter((key) => key !== columnKey)
    }
  } else {
    selectedColumns.value = [...selectedColumns.value, columnKey]
  }
}

function resetFilters() {
  filters.value = {
    report_type: filters.value.report_type,
    date_from: '',
    date_to: '',
    status: '',
    responsible: '',
    source: ''
  }

  applyReport()
}

async function applyReport() {
  loading.value = true
  error.value = ''

  try {
    await delay(400)

    const rows = buildRows()
    reportRows.value = filterRows(rows)
  } catch (e) {
    error.value = 'دریافت گزارش با مشکل مواجه شد.'
    reportRows.value = []
  } finally {
    loading.value = false
  }
}

function buildRows() {
  if (filters.value.report_type === 'leads') {
    return clientsStore.items
      .filter((client) => !client.is_deleted)
      .map((client) => {
        return {
          full_name: client.full_name,
          phone: client.phone,
          source: client.source || '-',
          status: client.status || '-',
          customer_type: client.customer_type || '-',
          assigned_agent: client.assigned_agent || '-',
          created_at: client.created_at?.slice(0, 10) || '-'
        }
      })
  }

  if (filters.value.report_type === 'deals') {
    return dealsStore.deals.map((deal) => {
      const stage = dealsStore.stages.find((item) => item.id === deal.stage)

      return {
        title: deal.title,
        client_name: deal.client_name || '-',
        property_title: deal.property_title || '-',
        stage_name: stage ? stage.name : '-',
        amount: deal.amount,
        agent: deal.agent || '-',
        status: deal.status || '-',
        expected_close_date: deal.expected_close_date || '-'
      }
    })
  }

  if (filters.value.report_type === 'agents') {
    const agents = {}

    dealsStore.deals.forEach((deal) => {
      const agentName = deal.agent || 'نامشخص'

      if (!agents[agentName]) {
        agents[agentName] = {
          agent: agentName,
          deals_count: 0,
          won_count: 0,
          lost_count: 0,
          total_amount: 0
        }
      }

      agents[agentName].deals_count += 1
      agents[agentName].total_amount += Number(deal.amount || 0)

      if (deal.status === 'Won') {
        agents[agentName].won_count += 1
      }

      if (deal.status === 'Lost') {
        agents[agentName].lost_count += 1
      }
    })

    return Object.values(agents).map((agent) => {
      const closed = agent.won_count + agent.lost_count
      const winRate = closed > 0 ? Math.round((agent.won_count / closed) * 100) : 0

      return {
        ...agent,
        win_rate: winRate + '٪'
      }
    })
  }

  if (filters.value.report_type === 'funnel') {
    const stages = [...dealsStore.stages]
      .filter((stage) => stage.pipeline === dealsStore.selectedPipelineId)
      .sort((a, b) => a.sort_order - b.sort_order)

    const totalDeals = dealsStore.deals.length || 1

    return stages.map((stage) => {
      const stageDeals = dealsStore.deals.filter((deal) => deal.stage === stage.id)
      const totalAmount = stageDeals.reduce((sum, deal) => sum + Number(deal.amount || 0), 0)

      return {
        stage: stage.name,
        deals_count: stageDeals.length,
        total_amount: totalAmount,
        conversion: Math.round((stageDeals.length / totalDeals) * 100) + '٪'
      }
    })
  }

  if (filters.value.report_type === 'properties') {
    return propertiesStore.items
      .filter((property) => !property.is_deleted)
      .map((property) => {
        return {
          code: property.code,
          title: property.title,
          property_type: property.property_type || '-',
          listing_type: property.listing_type || '-',
          status: property.status || '-',
          price: property.price,
          city: property.city || '-',
          assigned_agent: property.assigned_agent || '-',
          created_at: property.created_at?.slice(0, 10) || '-'
        }
      })
  }

  if (filters.value.report_type === 'interactions') {
    return [
      {
        interaction_type: 'تماس تلفنی',
        title: 'تماس اولیه با علی رضایی',
        client_name: 'علی رضایی',
        agent: 'مدیر سیستم',
        occurred_at: '2026-07-06',
        needs_followup: 'بله'
      },
      {
        interaction_type: 'بازدید ملک',
        title: 'بازدید آپارتمان سعادت‌آباد',
        client_name: 'علی رضایی',
        agent: 'مدیر سیستم',
        occurred_at: '2026-07-08',
        needs_followup: 'بله'
      },
      {
        interaction_type: 'یادداشت',
        title: 'ثبت ترجیحات مشتری',
        client_name: 'مریم احمدی',
        agent: 'مدیر سیستم',
        occurred_at: '2026-07-09',
        needs_followup: 'خیر'
      }
    ]
  }

  return tasksStore.items.map((task) => {
    return {
      title: task.title,
      assigned_user: task.assigned_user || '-',
      priority: task.priority || '-',
      status: task.status || '-',
      due_date: task.due_date || '-',
      due_time: task.due_time || '-',
      completed_at: task.completed_at ? task.completed_at.slice(0, 10) : '-'
    }
  })
}

function filterRows(rows) {
  let result = [...rows]

  if (filters.value.status) {
    result = result.filter((row) => row.status === filters.value.status)
  }

  if (filters.value.responsible) {
    result = result.filter((row) => {
      return (
        row.assigned_agent === filters.value.responsible ||
        row.agent === filters.value.responsible ||
        row.assigned_user === filters.value.responsible
      )
    })
  }

  if (filters.value.source) {
    result = result.filter((row) => row.source === filters.value.source)
  }

  if (filters.value.date_from) {
    result = result.filter((row) => {
      const rowDate = row.created_at || row.expected_close_date || row.occurred_at || row.due_date

      if (!rowDate || rowDate === '-') {
        return true
      }

      return rowDate >= filters.value.date_from
    })
  }

  if (filters.value.date_to) {
    result = result.filter((row) => {
      const rowDate = row.created_at || row.expected_close_date || row.occurred_at || row.due_date

      if (!rowDate || rowDate === '-') {
        return true
      }

      return rowDate <= filters.value.date_to
    })
  }

  return result
}
</script>
