<template>
  <aside
    class="flex flex-col h-full bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 transition-all duration-300 z-20"
    :class="collapsed ? 'w-16' : 'w-60'"
  >
    <!-- Logo -->
    <div class="flex items-center gap-3 px-4 h-16 border-b border-gray-200 dark:border-gray-800 shrink-0">
      <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-brand-600 shrink-0">
        <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17H3a2 2 0 01-2-2V5a2 2 0 012-2h14a2 2 0 012 2v10a2 2 0 01-2 2h-2" />
        </svg>
      </div>
      <Transition name="fade">
        <span v-if="!collapsed" class="text-sm font-bold text-gray-900 dark:text-white whitespace-nowrap">
          TestAI Platform
        </span>
      </Transition>
    </div>

    <!-- Nav items -->
    <nav class="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
      <RouterLink
        v-for="item in navItems"
        :key="item.name"
        :to="item.to"
        class="sidebar-link group relative"
        :class="{ 'justify-center': collapsed }"
        :title="collapsed ? item.label : ''"
      >
        <component :is="item.icon" class="w-5 h-5 shrink-0" />
        <Transition name="fade">
          <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
        </Transition>
        <!-- Tooltip when collapsed -->
        <div
          v-if="collapsed"
          class="absolute left-full ml-2 px-2 py-1 bg-gray-900 text-white text-xs rounded-md whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50"
        >
          {{ item.label }}
        </div>
      </RouterLink>
    </nav>

    <!-- Bottom section -->
    <div class="border-t border-gray-200 dark:border-gray-800 p-3">
      <div class="flex items-center gap-3" :class="{ 'justify-center': collapsed }">
        <div class="w-8 h-8 rounded-full bg-brand-100 dark:bg-brand-900 flex items-center justify-center text-brand-700 dark:text-brand-300 text-sm font-bold shrink-0">
          AJ
        </div>
        <Transition name="fade">
          <div v-if="!collapsed" class="min-w-0">
            <p class="text-xs font-semibold text-gray-900 dark:text-white truncate">Alex Johnson</p>
            <p class="text-xs text-gray-500 dark:text-gray-400 truncate">Admin</p>
          </div>
        </Transition>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { h } from 'vue'

defineProps<{ collapsed: boolean }>()

// Inline icon components using SVG
const IconDashboard = { render: () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'w-5 h-5' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })]) }
const IconPrompt = { render: () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'w-5 h-5' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' })]) }
const IconReview = { render: () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'w-5 h-5' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })]) }
const IconApproval = { render: () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'w-5 h-5' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' })]) }
const IconZephyr = { render: () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'w-5 h-5' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12' })]) }
const IconExecution = { render: () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'w-5 h-5' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z' }), h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })]) }
const IconResults = { render: () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'w-5 h-5' }, [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })]) }

const navItems = [
  { name: 'dashboard', label: 'Dashboard', to: '/', icon: IconDashboard },
  { name: 'prompt', label: 'New Prompt', to: '/prompt', icon: IconPrompt },
  { name: 'review', label: 'Review', to: '/review', icon: IconReview },
  { name: 'approval', label: 'Approval', to: '/approval', icon: IconApproval },
  { name: 'zephyr', label: 'Zephyr Sync', to: '/zephyr', icon: IconZephyr },
  { name: 'execution', label: 'Execution', to: '/execution', icon: IconExecution },
  { name: 'results', label: 'Results', to: '/results', icon: IconResults },
]
</script>
