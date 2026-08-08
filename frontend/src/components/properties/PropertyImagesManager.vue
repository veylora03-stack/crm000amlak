<template>
  <section class="card p-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <h3 class="text-base font-semibold">مدیریت تصاویر</h3>

      <label class="btn-primary cursor-pointer">
        آپلود تصویر
        <input
          type="file"
          multiple
          accept="image/jpg,image/jpeg,image/png,image/webp"
          class="hidden"
          @change="onFileChange"
        />
      </label>
    </div>

    <p class="mt-2 text-xs text-text-secondary-light dark:text-text-secondary-dark">
      فرمت‌های مجاز: jpg، jpeg، png، webp — حداکثر حجم هر فایل: 10 مگابایت
    </p>

    <div
      v-if="images.length === 0"
      class="mt-4 rounded-md border border-dashed border-border-light py-10 text-center text-sm text-text-secondary-light dark:border-border-dark dark:text-text-secondary-dark"
    >
      هنوز تصویری آپلود نشده است.
    </div>

    <ul v-else class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
      <li
        v-for="(image, index) in images"
        :key="image.id"
        class="rounded-md border border-border-light p-2 dark:border-border-dark"
      >
        <img
          :src="image.url"
          :alt="image.alt_text || 'تصویر ملک'"
          class="h-28 w-full rounded-md object-cover"
        />

        <p class="mt-2 truncate text-xs text-text-secondary-light dark:text-text-secondary-dark">
          {{ image.alt_text || 'بدون نام' }}
        </p>

        <div class="mt-3 flex flex-wrap items-center gap-2">
          <span
            v-if="image.is_primary"
            class="rounded-full bg-success-50 px-2 py-1 text-xs font-medium text-success-700 dark:bg-success-900/20 dark:text-success-400"
          >
            تصویر اصلی
          </span>

          <button
            v-else
            type="button"
            class="btn-secondary"
            @click="$emit('set-primary', image.id)"
          >
            تصویر اصلی
          </button>

          <button
            type="button"
            class="btn-secondary"
            :disabled="index === 0"
            aria-label="انتقال به بالا"
            @click="$emit('move', image.id, -1)"
          >
            ↑
          </button>

          <button
            type="button"
            class="btn-secondary"
            :disabled="index === images.length - 1"
            aria-label="انتقال به پایین"
            @click="$emit('move', image.id, 1)"
          >
            ↓
          </button>

          <button
            type="button"
            class="btn-danger"
            @click="$emit('delete', image.id)"
          >
            حذف
          </button>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  images: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['add', 'set-primary', 'delete', 'move'])

function onFileChange(event) {
  const files = event.target.files

  if (files && files.length > 0) {
    emit('add', files)
  }

  event.target.value = ''
}
</script>
