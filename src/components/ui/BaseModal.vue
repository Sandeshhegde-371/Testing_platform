<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="$emit('update:modelValue', false)"
      >
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="$emit('update:modelValue', false)" />
        <div
          class="relative bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 w-full animate-fade-in"
          :class="[sizeClass]"
        >
          <!-- Header -->
          <div class="flex items-center justify-between p-5 border-b border-gray-200 dark:border-gray-800">
            <div>
              <h3 class="text-base font-semibold text-gray-900 dark:text-white">{{ title }}</h3>
              <p v-if="description" class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{{ description }}</p>
            </div>
            <button
              @click="$emit('update:modelValue', false)"
              class="btn-ghost p-1.5 rounded-lg"
              aria-label="Close modal"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="p-5">
            <slot />
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="px-5 pb-5 flex justify-end gap-2">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  modelValue: boolean
  title: string
  description?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
}>()

defineEmits<{ 'update:modelValue': [value: boolean] }>()

const sizeClass = computed(() => ({
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-2xl',
}[props.size || 'md']))
</script>
