<template>
  <header class="h-16 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 flex items-center px-4 gap-4 shrink-0 z-10">
    <!-- Sidebar toggle -->
    <button
      id="sidebar-toggle"
      @click="$emit('toggle-sidebar')"
      class="btn-ghost p-2 rounded-lg"
      aria-label="Toggle sidebar"
    >
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <!-- Breadcrumb / page title -->
    <div class="flex-1">
      <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">{{ currentRoute }}</span>
    </div>

    <!-- Right actions -->
    <div class="flex items-center gap-2">
      <!-- Search -->
      <div class="relative hidden md:block">
        <input
          type="text"
          placeholder="Search test cases..."
          class="form-input pl-9 py-1.5 w-56 text-sm"
        />
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>

      <!-- Dark mode toggle -->
      <button
        id="dark-mode-toggle"
        @click="toggleDark"
        class="btn-ghost p-2 rounded-lg"
        :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
      >
        <svg v-if="isDark" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </button>

      <!-- Notification bell -->
      <button class="btn-ghost p-2 rounded-lg relative">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
      </button>

      <!-- Avatar -->
      <div class="w-8 h-8 rounded-full bg-brand-600 flex items-center justify-center text-white text-xs font-bold cursor-pointer">
        AJ
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStorage } from '@vueuse/core'

defineEmits<{ 'toggle-sidebar': [] }>()

const route = useRoute()
const isDark = useStorage('testai-dark-mode', false)

const currentRoute = computed(() => {
  const names: Record<string, string> = {
    dashboard: 'Dashboard',
    prompt: 'New Prompt',
    processing: 'AI Generation',
    review: 'Review Test Cases',
    approval: 'Approval',
    zephyr: 'Zephyr Integration',
    execution: 'Test Execution',
    results: 'Results & Insights',
  }
  return names[String(route.name)] || 'TestAI Platform'
})

function toggleDark() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
}
</script>
