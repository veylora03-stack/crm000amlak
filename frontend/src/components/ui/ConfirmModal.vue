<template>
  <Modal
    :open="open"
    :title="title"
    size="sm"
    :closable="!loading"
    @close="$emit('cancel')"
  >
    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark">
      {{ message }}
    </p>

    <template #footer>
      <div class="flex items-center justify-between gap-2">
        <button
          type="button"
          class="btn-secondary"
          :disabled="loading"
          @click="$emit('cancel')"
        >
          {{ cancelLabel }}
        </button>

        <button
          type="button"
          :class="danger ? 'btn-danger' : 'btn-primary'"
          :disabled="loading"
          @click="$emit('confirm')"
        >
          {{ loading ? 'در حال انجام...' : confirmLabel }}
        </button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import Modal from '@/components/ui/Modal.vue'

defineProps({
  open: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'تأیید عملیات'
  },
  message: {
    type: String,
    default: 'آیا از انجام این عملیات مطمئن هستید؟'
  },
  confirmLabel: {
    type: String,
    default: 'تأیید'
  },
  cancelLabel: {
    type: String,
    default: 'انصراف'
  },
  danger: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['confirm', 'cancel'])
</script>
