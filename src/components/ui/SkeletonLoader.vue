<template>
  <div class="space-y-2">
    <div v-for="i in count" :key="i" class="skeleton" :style="{ height: height, width: widths[(i-1) % widths.length] }" />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  count?: number
  height?: string
}>()

const widths = ['100%', '85%', '92%', '78%', '95%']

withDefaults(defineProps<{
  count?: number
  height?: string
}>(), {
  count: 3,
  height: '20px',
})
</script>
