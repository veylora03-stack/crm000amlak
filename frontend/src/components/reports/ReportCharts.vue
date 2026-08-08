<template>
  <ChartCard
    :title="chartTitle"
    :type="chartType"
    :loading="loading"
    :error="false"
    :empty="rows.length === 0"
    :options="chartOptions"
    :series="chartSeries"
  />
</template>

<script setup>
import { computed } from 'vue'
import ChartCard from '@/components/dashboard/ChartCard.vue'

const props = defineProps({
  reportType: {
    type: String,
    required: true
  },
  rows: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const chartTitle = computed(() => {
  if (props.reportType === 'leads') {
    return 'لیدها بر اساس منبع'
  }

  if (props.reportType === 'deals') {
    return 'Dealها بر اساس Stage'
  }

  if (props.reportType === 'agents') {
    return 'عملکرد Agentها'
  }

  if (props.reportType === 'funnel') {
    return 'Funnel فروش'
  }

  if (props.reportType === 'properties') {
    return 'وضعیت املاک'
  }

  if (props.reportType === 'tasks') {
    return 'وضعیت وظایف'
  }

  return 'تعامل‌ها بر اساس نوع'
})

const chartType = computed(() => {
  if (props.reportType === 'deals' || props.reportType === 'agents' || props.reportType === 'tasks') {
    return 'bar'
  }

  if (props.reportType === 'funnel') {
    return 'bar'
  }

  return 'donut'
})

const chartOptions = computed(() => {
  const base = {
    chart: {
      fontFamily: 'Vazirmatn, Tahoma, sans-serif',
      toolbar: {
        show: false
      },
      background: 'transparent'
    },
    dataLabels: {
      enabled: false
    },
    colors: ['#2563eb', '#16a34a', 'theme("colors.chart.amber")', '#dc2626', '#7c3aed', '#0891b2', '#db2777']
  }

  if (chartType.value === 'bar') {
    return {
      ...base,
      plotOptions: {
        bar: {
          borderRadius: 4,
          columnWidth: '45%',
          horizontal: props.reportType === 'funnel'
        }
      },
      xaxis: {
        categories: categories.value
      }
    }
  }

  return {
    ...base,
    labels: categories.value,
    legend: {
      position: 'bottom'
    }
  }
})

const categories = computed(() => {
  if (props.reportType === 'leads') {
    return groupLabels('source')
  }

  if (props.reportType === 'deals') {
    return groupLabels('stage_name')
  }

  if (props.reportType === 'agents') {
    return groupLabels('agent')
  }

  if (props.reportType === 'funnel') {
    return groupLabels('stage')
  }

  if (props.reportType === 'properties') {
    return groupLabels('status')
  }

  if (props.reportType === 'tasks') {
    return groupLabels('status')
  }

  return groupLabels('interaction_type')
})

const chartSeries = computed(() => {
  const counts = groupCounts()

  if (chartType.value === 'bar') {
    return [
      {
        name: 'تعداد',
        data: counts
      }
    ]
  }

  return counts
})

function groupLabels(field) {
  const values = props.rows.map((row) => row[field] || 'نامشخص')

  return [...new Set(values)]
}

function groupCounts() {
  const labels = categories.value
  const field = fieldForReport()

  return labels.map((label) => {
    return props.rows.filter((row) => {
      return (row[field] || 'نامشخص') === label
    }).length
  })
}

function fieldForReport() {
  if (props.reportType === 'leads') {
    return 'source'
  }

  if (props.reportType === 'deals') {
    return 'stage_name'
  }

  if (props.reportType === 'agents') {
    return 'agent'
  }

  if (props.reportType === 'funnel') {
    return 'stage'
  }

  if (props.reportType === 'properties') {
    return 'status'
  }

  if (props.reportType === 'tasks') {
    return 'status'
  }

  return 'interaction_type'
}
</script>


