<template>
  <section>
    <div
      v-if="images.length === 0"
      class="flex flex-col items-center justify-center gap-3 rounded-md border border-dashed border-border-light py-14 text-center dark:border-border-dark"
    >
      <p class="text-text-secondary-light dark:text-text-secondary-dark">
        تصویری برای این ملک ثبت نشده است.
      </p>
    </div>

    <div v-else class="grid gap-4 lg:grid-cols-[2fr_1fr]">
      <div class="card overflow-hidden p-0">
        <img
          :src="selectedImage.url"
          :alt="selectedImage.alt_text || 'تصویر ملک'"
          class="h-80 w-full object-cover"
        />
      </div>

      <div class="grid grid-cols-3 gap-2 lg:grid-cols-2">
        <button
          v-for="(image, index) in images"
          :key="image.id"
          type="button"
          :class="[
            'overflow-hidden rounded-md border-2 transition duration-normal ease-out',
            index === selectedIndex
              ? 'border-primary-600 dark:border-primary-400'
              : 'border-transparent hover:border-border-strong-light dark:hover:border-border-strong-dark'
          ]"
          :aria-label="`نمایش تصویر ${index + 1}`"
          @click="selectedIndex = index"
        >
          <img
            :src="image.url"
            :alt="image.alt_text || ''"
            class="h-20 w-full object-cover"
          />
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  }
})

const selectedIndex = ref(0)

const selectedImage = computed(() => {
  return props.images[selectedIndex.value] || props.images[0] || {}
})

watch(
  () => props.images.length,
  (length) => {
    if (selectedIndex.value >= length) {
      selectedIndex.value = 0
    }
  }
)
</script>
