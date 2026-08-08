export function formatNumber(value) {
  const numericValue = Number(value || 0)

  return new Intl.NumberFormat('fa-IR').format(numericValue)
}

export function formatCurrency(value) {
  return formatNumber(value) + ' ریال'
}

export function formatDate(value) {
  if (!value) {
    return '-'
  }

  try {
    return new Intl.DateTimeFormat('fa-IR', {
      dateStyle: 'medium'
    }).format(new Date(value))
  } catch (error) {
    return '-'
  }
}

export function formatDateTime(value) {
  if (!value) {
    return '-'
  }

  try {
    return new Intl.DateTimeFormat('fa-IR', {
      dateStyle: 'medium',
      timeStyle: 'short'
    }).format(new Date(value))
  } catch (error) {
    return '-'
  }
}

export function formatPercent(value) {
  return formatNumber(value) + '٪'
}
