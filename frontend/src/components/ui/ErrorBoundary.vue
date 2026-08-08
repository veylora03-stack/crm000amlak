<template>
  <slot v-if="!error" />
  
  <div v-else class="error-boundary">
    <div class="error-boundary-content">
      <div class="error-boundary-icon">
        <svg class="h-16 w-16 text-danger-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
        </svg>
      </div>
      
      <h2 class="error-boundary-title">مشکلی پیش آمد!</h2>
      
      <p class="error-boundary-message">
        متأسفانه یک خطای غیرمنتظره رخ داده است. نگران نباشید، تیم فنی ما از این مشکل مطلع شده و در حال بررسی آن است.
      </p>
      
      <div class="error-boundary-actions">
        <button class="btn-primary" @click="reload">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          تلاش مجدد
        </button>
        
        <button class="btn-secondary" @click="goHome">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          بازگشت به خانه
        </button>
      </div>
      
      <details v-if="showDetails" class="error-boundary-details">
        <summary>جزئیات فنی (برای توسعه‌دهندگان)</summary>
        <pre class="error-boundary-stack">{{ error.message }}</pre>
      </details>
    </div>
  </div>
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const error = ref(null)
const errorInfo = ref(null)
const showDetails = ref(import.meta.env.DEV)

onErrorCaptured((err, instance, info) => {
  error.value = err
  errorInfo.value = info
  
  // Log error to console in development
  if (import.meta.env.DEV) {
    console.error('ErrorBoundary caught:', err, info)
  }
  
  // In production, send to error tracking service (Sentry, LogRocket, etc.)
  // sendToErrorTracking(err, info)
  
  // Don't propagate the error
  return false
})

function reload() {
  error.value = null
  errorInfo.value = null
}

function goHome() {
  error.value = null
  errorInfo.value = null
  router.push('/')
}
</script>

<style scoped>
.error-boundary {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: var(--color-bg-primary);
}

.error-boundary-content {
  max-width: 480px;
  text-align: center;
}

.error-boundary-icon {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.error-boundary-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
}

.error-boundary-message {
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

.error-boundary-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.error-boundary-details {
  text-align: right;
  background: var(--color-bg-secondary);
  border-radius: 0.5rem;
  padding: 1rem;
  font-size: 0.75rem;
}

.error-boundary-details summary {
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.error-boundary-stack {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--color-text-muted);
  max-height: 200px;
  overflow-y: auto;
}
</style>
