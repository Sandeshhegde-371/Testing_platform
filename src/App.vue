<template>
  <RouterView />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useStorage } from '@vueuse/core'

const darkMode = useStorage('testai-dark-mode', false)

onMounted(() => {
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
  }
})
</script>
