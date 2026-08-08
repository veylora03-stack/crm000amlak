/**
 * API Error Handler
 * 
 * Centralized error handling for all API calls with user-friendly messages
 * and automatic toast notifications.
 * 
 * @example
 * try {
 *   await apiRequest()
 * } catch (error) {
 *   handleApiError(error, 'خطا در دریافت داده‌ها')
 * }
 */
import { useUiStore } from '@/stores/ui'

/**
 * Parse API error and extract user-friendly message
 */
export function parseApiError(error) {
  // Network error
  if (!error.response) {
    return {
      type: 'network',
      message: 'اتصال به سرور برقرار نشد. لطفاً اتصال اینترنت خود را بررسی کنید.',
      title: 'خطای شبکه'
    }
  }

  // HTTP errors
  const status = error.response.status
  const data = error.response.data
  
  // Extract message from API response
  let apiMessage = 'خطای ناشناخته'
  if (data?.errors?.[0]?.message) {
    apiMessage = data.errors[0].message
  } else if (data?.message) {
    apiMessage = data.message
  } else if (data?.detail) {
    apiMessage = data.detail
  }

  switch (status) {
    case 400:
      return {
        type: 'validation',
        message: apiMessage || 'اطلاعات ارسال شده نامعتبر است.',
        title: 'خطای اعتبارسنجی'
      }
    
    case 401:
      return {
        type: 'auth',
        message: 'نشست شما منقضی شده است. لطفاً دوباره وارد شوید.',
        title: 'نیاز به ورود'
      }
    
    case 403:
      return {
        type: 'forbidden',
        message: 'شما مجاز به انجام این عملیات نیستید.',
        title: 'دسترسی ممنوع'
      }
    
    case 404:
      return {
        type: 'not_found',
        message: apiMessage || 'مورد درخواستی یافت نشد.',
        title: 'یافت نشد'
      }
    
    case 429:
      return {
        type: 'rate_limit',
        message: 'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً چند لحظه صبر کنید.',
        title: 'محدودیت درخواست'
      }
    
    case 500:
    case 502:
    case 503:
    case 504:
      return {
        type: 'server',
        message: 'خطای سرور. لطفاً چند لحظه دیگر دوباره تلاش کنید.',
        title: 'خطای سرور'
      }
    
    default:
      return {
        type: 'unknown',
        message: apiMessage,
        title: 'خطا'
      }
  }
}

/**
 * Handle API error with automatic toast notification
 * 
 * @param {Error} error - The error object from API call
 * @param {string} fallbackMessage - Fallback message if parsing fails
 * @param {Object} options - Options for error handling
 * @param {boolean} options.showToast - Whether to show toast (default: true)
 * @param {boolean} options.log - Whether to log error (default: true)
 */
export function handleApiError(error, fallbackMessage = 'خطایی رخ داد', options = {}) {
  const { showToast = true, log = true } = options
  
  const parsedError = parseApiError(error)
  
  if (log) {
    console.error('[API Error]', {
      type: parsedError.type,
      message: parsedError.message,
      originalError: error
    })
  }
  
  if (showToast) {
    const ui = useUiStore()
    ui.pushToast({
      type: 'error',
      title: parsedError.title,
      message: parsedError.message
    })
  }
  
  // Special handling for auth errors
  if (parsedError.type === 'auth') {
    // Trigger logout flow
    const authStore = useAuthStore()
    authStore.logout()
    window.location.href = '/login'
  }
  
  return parsedError
}

/**
 * Wrapper for API calls with automatic error handling
 * 
 * @param {Function} apiCall - The API call function
 * @param {string} errorMessage - Error message to show on failure
 * @param {Object} options - Options
 */
export async function withErrorHandling(apiCall, errorMessage, options = {}) {
  try {
    const response = await apiCall()
    return { success: true, data: response.data || response }
  } catch (error) {
    const parsedError = handleApiError(error, errorMessage, options)
    return { success: false, error: parsedError }
  }
}
