<template>
  <div class="flex flex-wrap items-center gap-2">
    <button
      type="button"
      class="btn-secondary"
      :disabled="rows.length === 0"
      @click="exportCsv"
    >
      خروجی CSV
    </button>

    <button
      type="button"
      class="btn-secondary"
      :disabled="rows.length === 0"
      @click="exportExcel"
    >
      خروجی Excel
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  rows: {
    type: Array,
    default: () => []
  },
  reportType: {
    type: String,
    default: 'report'
  }
})

function filename(extension) {
  const date = new Date().toISOString().slice(0, 10)

  return `${props.reportType}-${date}.${extension}`
}

function cellValue(value) {
  if (value === null || value === undefined) {
    return ''
  }

  return String(value)
}

function escapeCsvValue(value) {
  const text = cellValue(value)

  return `"${text.replaceAll('"', '""')}"`
}

function downloadBlob(blob, fileName) {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')

  link.href = url
  link.download = fileName

  document.body.appendChild(link)
  link.click()

  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

function exportCsv() {
  const header = props.columns.map((column) => escapeCsvValue(column.label)).join(',')
  const body = props.rows.map((row) => {
    return props.columns.map((column) => escapeCsvValue(row[column.key])).join(',')
  })

  const csv = '\uFEFF' + [header, ...body].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })

  downloadBlob(blob, filename('csv'))
}

function exportExcel() {
  const headerCells = props.columns.map((column) => {
    return `<th>${cellValue(column.label)}</th>`
  }).join('')

  const bodyRows = props.rows.map((row) => {
    const cells = props.columns.map((column) => {
      return `<td>${cellValue(row[column.key])}</td>`
    }).join('')

    return `<tr>${cells}</tr>`
  }).join('')

  const html = `
    <html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel">
      <head>
        <meta charset="UTF-8" />
      </head>
      <body>
        <table border="1">
          <thead>
            <tr>${headerCells}</tr>
          </thead>
          <tbody>${bodyRows}</tbody>
        </table>
      </body>
    </html>
  `

  const blob = new Blob([html], { type: 'application/vnd.ms-excel;charset=utf-8;' })

  downloadBlob(blob, filename('xls'))
}
</script>
