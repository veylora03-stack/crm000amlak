<template>
  <div class="jalaali-date-picker relative">
    <!-- Input -->
    <div class="relative">
      <input
        :value="displayValue"
        type="text"
        class="input w-full pr-10"
        :placeholder="placeholder"
        readonly
        @click="isOpen = !isOpen"
      />
      <button
        type="button"
        class="absolute right-2.5 top-1/2 -translate-y-1/2 text-base-400 hover:text-base-700 dark:hover:text-base-200"
        @click="isOpen = !isOpen"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </button>
    </div>

    <!-- Dropdown -->
    <teleport to="body">
      <transition name="fade">
        <div
          v-if="isOpen"
          class="fixed inset-0 z-modal"
          @click="close"
        >
          <div
            class="absolute w-[320px] rounded-xl border border-app-border bg-app-panel p-4 shadow-xl dark:border-app-border-dark"
            :style="dropdownStyle"
            @click.stop
          >
            <!-- Header -->
            <div class="mb-3 flex items-center justify-between">
              <button
                type="button"
                class="btn-ghost btn-sm"
                @click="prevMonth"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
              
              <div class="text-center">
                <div class="text-sm font-bold">{{ monthNames[viewMonth - 1] }} {{ viewYear }}</div>
                <button
                  type="button"
                  class="text-[10px] text-brand-600 hover:text-brand-700 dark:text-brand-400"
                  @click="goToToday"
                >
                  {{ t('calendar.today') }}
                </button>
              </div>
              
              <button
                type="button"
                class="btn-ghost btn-sm"
                @click="nextMonth"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
            </div>

            <!-- Weekday headers -->
            <div class="mb-2 grid grid-cols-7 gap-1">
              <div
                v-for="(day, idx) in weekdayShort"
                :key="idx"
                class="py-1 text-center text-[10px] font-semibold text-base-500"
                :class="{ 'text-danger-500': idx === 6 }"
              >
                {{ day }}
              </div>
            </div>

            <!-- Days grid -->
            <div class="grid grid-cols-7 gap-1">
              <template v-for="(week, wi) in monthGrid" :key="wi">
                <button
                  v-for="(cell, ci) in week"
                  :key="ci"
                  type="button"
                  :disabled="!cell"
                  :class="[
                    'aspect-square rounded-md text-xs font-medium transition-all',
                    !cell ? 'invisible' : '',
                    cell && isSelected(cell) ? 'bg-brand-600 text-white' : '',
                    cell && !isSelected(cell) && cell.isToday ? 'bg-brand-500/20 text-brand-700 dark:text-brand-300' : '',
                    cell && !isSelected(cell) && !cell.isToday ? 'hover:bg-base-100 text-base-800 dark:text-base-200 dark:hover:bg-base-800' : '',
                    cell && ci === 6 && !isSelected(cell) ? 'text-danger-500' : ''
                  ]"
                  @click="cell && selectDate(cell)"
                >
                  {{ cell ? cell.day : '' }}
                </button>
              </template>
            </div>

            <!-- Footer -->
            <div class="mt-3 flex items-center justify-between border-t border-app-border pt-3 dark:border-app-border-dark">
              <button
                type="button"
                class="btn-ghost btn-sm"
                @click="clear"
              >
                پاک کردن
              </button>
              <button
                type="button"
                class="btn-secondary btn-sm"
                @click="close"
              >
                بستن
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useJalaaliDate } from '@/composables/useJalaaliDate'

const props = defineProps({
  modelValue: { type: [Date, String, null], default: null },
  placeholder: { type: String, default: 'انتخاب تاریخ' },
  format: { type: String, default: 'YYYY/MM/DD' }
})

const emit = defineEmits(['update:modelValue'])

const { t } = useI18n()
const { toJalaali, toGregorian, formatDate, monthNames, weekdayShort, todayJalaali, generateMonthGrid } = useJalaaliDate()

const isOpen = ref(false)
const dropdownStyle = ref({})

// View state
const today = todayJalaali.value
const viewYear = ref(today ? today.jy : 1403)
const viewMonth = ref(today ? today.jm : 1)

// Current selected value
const selectedDate = computed(() => {
  if (!props.modelValue) return null
  const d = props.modelValue instanceof Date ? props.modelValue : new Date(props.modelValue)
  return toJalaali(d)
})

// Display value
const displayValue = computed(() => {
  if (!props.modelValue) return ''
  const d = props.modelValue instanceof Date ? props.modelValue : new Date(props.modelValue)
  return formatDate(d, props.format)
})

// Month grid
const monthGrid = computed(() => generateMonthGrid(viewYear.value, viewMonth.value))

// Check if cell is selected
const isSelected = (cell) => {
  if (!selectedDate.value) return false
  return cell.jDate.jy === selectedDate.value.jy &&
         cell.jDate.jm === selectedDate.value.jm &&
         cell.jDate.jd === selectedDate.value.jd
}

// Navigation
const prevMonth = () => {
  if (viewMonth.value === 1) {
    viewMonth.value = 12
    viewYear.value--
  } else {
    viewMonth.value--
  }
}

const nextMonth = () => {
  if (viewMonth.value === 12) {
    viewMonth.value = 1
    viewYear.value++
  } else {
    viewMonth.value++
  }
}

const goToToday = () => {
  if (todayJalaali.value) {
    viewYear.value = todayJalaali.value.jy
    viewMonth.value = todayJalaali.value.jm
  }
}

// Selection
const selectDate = (cell) => {
  const gDate = toGregorian(cell.jDate.jy, cell.jDate.jm, cell.jDate.jd)
  emit('update:modelValue', gDate)
  close()
}

const clear = () => {
  emit('update:modelValue', null)
  close()
}

const close = () => {
  isOpen.value = false
}

// Reset view when opening
watch(isOpen, (val) => {
  if (val && selectedDate.value) {
    viewYear.value = selectedDate.value.jy
    viewMonth.value = selectedDate.value.jm
  } else if (val) {
    goToToday()
  }
})

// Close on ESC
const onKeydown = (e) => {
  if (e.key === 'Escape' && isOpen.value) close()
}

onMounted(() => {
  document.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
.jalaali-date-picker {
  position: relative;
}
</style>
