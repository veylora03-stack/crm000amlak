/**
 * useJalaaliDate Composable
 * 
 * Provides Jalaali (Persian/Shamsi) calendar utilities for Vue 3.
 * Uses jalaali-js library for accurate conversions.
 * 
 * @example
 * const { todayJalaali, toJalaali, toGregorian, formatDate } = useJalaaliDate()
 * const jDate = toJalaali(new Date())
 * const formatted = formatDate(new Date(), 'YYYY/MM/DD')
 */
import { ref, computed } from 'vue'
import jalaali from 'jalaali-js'

export function useJalaaliDate() {
  // Persian month names
  const monthNames = [
    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
  ]
  
  const weekdayNames = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']
  const weekdayShort = ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج']

  /**
   * Convert Gregorian date to Jalaali
   */
  const toJalaali = (date) => {
    if (!date) return null
    const d = date instanceof Date ? date : new Date(date)
    return jalaali.toJalaali(d.getFullYear(), d.getMonth() + 1, d.getDate())
  }

  /**
   * Convert Jalaali date to Gregorian
   */
  const toGregorian = (jy, jm, jd) => {
    const result = jalaali.toGregorian(jy, jm, jd)
    return new Date(result.gy, result.gm - 1, result.gd)
  }

  /**
   * Get today's date in Jalaali
   */
  const todayJalaali = computed(() => toJalaali(new Date()))

  /**
   * Format date to Jalaali string
   * @param {Date} date - Gregorian date
   * @param {string} format - Format string (YYYY, MM, DD)
   */
  const formatDate = (date, format = 'YYYY/MM/DD') => {
    const j = toJalaali(date)
    if (!j) return ''
    
    const jy = j.jy.toString()
    const jm = j.jm.toString().padStart(2, '0')
    const jd = j.jd.toString().padStart(2, '0')
    
    return format
      .replace('YYYY', jy)
      .replace('MM', jm)
      .replace('DD', jd)
  }

  /**
   * Format date with month name
   */
  const formatDateLong = (date) => {
    const j = toJalaali(date)
    if (!j) return ''
    return `${j.jd} ${monthNames[j.jm - 1]} ${j.jy}`
  }

  /**
   * Format relative time (e.g., "2 ساعت پیش")
   */
  const formatRelative = (date) => {
    const now = new Date()
    const target = new Date(date)
    const diffMs = now - target
    const diffSec = Math.floor(diffMs / 1000)
    const diffMin = Math.floor(diffSec / 60)
    const diffHour = Math.floor(diffMin / 60)
    const diffDay = Math.floor(diffHour / 24)
    
    if (diffSec < 60) return 'چند لحظه پیش'
    if (diffMin < 60) return `${diffMin} دقیقه پیش`
    if (diffHour < 24) return `${diffHour} ساعت پیش`
    if (diffDay < 7) return `${diffDay} روز پیش`
    return formatDate(target)
  }

  /**
   * Get days in a Jalaali month
   */
  const daysInMonth = (jy, jm) => {
    return jalaali.jalaaliMonthLength(jy, jm)
  }

  /**
   * Check if Jalaali year is leap
   */
  const isLeapYear = (jy) => {
    return jalaali.isLeapJalaaliYear(jy)
  }

  /**
   * Get weekday name for a date
   */
  const getWeekday = (date) => {
    const d = date instanceof Date ? date : new Date(date)
    // JavaScript: 0 = Sunday, 6 = Saturday
    // Persian: 0 = Saturday, 6 = Friday
    const jsDay = d.getDay()
    const persianDay = (jsDay + 1) % 7
    return {
      name: weekdayNames[persianDay],
      short: weekdayShort[persianDay],
      index: persianDay
    }
  }

  /**
   * Generate calendar grid for a Jalaali month
   */
  const generateMonthGrid = (jy, jm) => {
    const daysInMonthCount = daysInMonth(jy, jm)
    const firstDay = toGregorian(jy, jm, 1)
    const firstWeekday = getWeekday(firstDay).index
    
    const grid = []
    let week = new Array(7).fill(null)
    
    // Fill initial empty slots
    for (let i = 0; i < firstWeekday; i++) {
      week[i] = null
    }
    
    // Fill days
    let dayIndex = firstWeekday
    for (let day = 1; day <= daysInMonthCount; day++) {
      week[dayIndex] = {
        day,
        jDate: { jy, jm, jd: day },
        gDate: toGregorian(jy, jm, day),
        isToday: false
      }
      dayIndex++
      
      if (dayIndex === 7) {
        grid.push(week)
        week = new Array(7).fill(null)
        dayIndex = 0
      }
    }
    
    // Add last week if not empty
    if (dayIndex > 0) {
      grid.push(week)
    }
    
    // Mark today
    const today = todayJalaali.value
    if (today && today.jy === jy && today.jm === jm) {
      grid.forEach(week => {
        week.forEach(cell => {
          if (cell && cell.day === today.jd) {
            cell.isToday = true
          }
        })
      })
    }
    
    return grid
  }

  return {
    // Data
    monthNames,
    weekdayNames,
    weekdayShort,
    todayJalaali,
    
    // Conversions
    toJalaali,
    toGregorian,
    
    // Formatting
    formatDate,
    formatDateLong,
    formatRelative,
    
    // Utilities
    daysInMonth,
    isLeapYear,
    getWeekday,
    generateMonthGrid
  }
}
