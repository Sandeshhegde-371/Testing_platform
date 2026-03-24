<template>
  <div class="glass-card p-5 animate-fade-in" v-bind="$attrs">
    <div v-if="title || $slots.header" class="flex items-center justify-between mb-4">
      <div>
        <h3 v-if="title" class="text-sm font-semibold text-gray-900 dark:text-white">{{ title }}</h3>
        <p v-if="subtitle" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ subtitle }}</p>
      </div>
      <slot name="header" />
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
  subtitle?: string
}>()
</script>
