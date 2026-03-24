<template>
  <div class="space-y-3">
    <div
      v-for="(step, index) in steps"
      :key="index"
      class="flex items-start gap-4"
    >
      <!-- Step indicator -->
      <div class="flex flex-col items-center">
        <div
          class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold shrink-0 transition-all duration-500"
          :class="stepClass(index)"
        >
          <!-- Spinner for active -->
          <svg v-if="currentStep === index" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <!-- Check for done -->
          <svg v-else-if="index < currentStep" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
          </svg>
          <!-- Number for pending -->
          <span v-else>{{ index + 1 }}</span>
        </div>
        <!-- Connector line -->
        <div
          v-if="index < steps.length - 1"
          class="w-0.5 h-8 mt-1 transition-all duration-500"
          :class="index < currentStep ? 'bg-brand-500' : 'bg-gray-200 dark:bg-gray-700'"
        />
      </div>

      <!-- Step label -->
      <div class="pt-1.5 pb-6">
        <p
          class="text-sm font-medium transition-colors duration-300"
          :class="index <= currentStep ? 'text-gray-900 dark:text-white' : 'text-gray-400 dark:text-gray-600'"
        >{{ step }}</p>
        <p
          v-if="currentStep === index && subLabel"
          class="text-xs text-brand-600 dark:text-brand-400 mt-0.5 animate-pulse"
        >{{ subLabel }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  steps: string[]
  currentStep: number
  subLabel?: string
}>()

function stepClass(index: number) {
  if (index < props.currentStep) return 'bg-brand-600 text-white'
  if (index === props.currentStep) return 'bg-brand-600 text-white ring-4 ring-brand-100 dark:ring-brand-900/30'
  return 'bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-600'
}
</script>
