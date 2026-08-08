import { createI18n } from 'vue-i18n'
import fa from './locales/fa'
import en from './locales/en'

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('locale') || 'fa',
  fallbackLocale: 'fa',
  messages: { fa, en },
  numberFormats: {
    fa: {
      currency: { style: 'currency', currency: 'IRR' },
      decimal: { style: 'decimal', minimumFractionDigits: 0 },
      percent: { style: 'percent', minimumFractionDigits: 0 }
    },
    en: {
      currency: { style: 'currency', currency: 'USD' },
      decimal: { style: 'decimal', minimumFractionDigits: 0 },
      percent: { style: 'percent', minimumFractionDigits: 0 }
    }
  },
  datetimeFormats: {
    fa: {
      short: { year: 'numeric', month: 'long', day: 'numeric' },
      long: { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }
    },
    en: {
      short: { year: 'numeric', month: 'long', day: 'numeric' },
      long: { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }
    }
  },
  // v11: explicitly disable warnings in development
  missingWarn: false,
  fallbackWarn: false
})

export function setLocale(locale) {
  i18n.global.locale.value = locale
  localStorage.setItem('locale', locale)
  document.documentElement.setAttribute('lang', locale)
  document.documentElement.setAttribute('dir', locale === 'fa' ? 'rtl' : 'ltr')
}

export function getLocale() {
  return i18n.global.locale.value
}

export function toggleLocale() {
  setLocale(getLocale() === 'fa' ? 'en' : 'fa')
}

// Initialize
const savedLocale = localStorage.getItem('locale') || 'fa'
document.documentElement.setAttribute('lang', savedLocale)
document.documentElement.setAttribute('dir', savedLocale === 'fa' ? 'rtl' : 'ltr')

export default i18n
