<template>
  <div class="animate-fade-in">
    <!-- Page Header -->
    <div class="page-header flex items-center justify-between">
      <div>
        <h1 class="page-title">Welcome back, Alex 👋</h1>
        <p class="page-subtitle">Here's what's happening with your test automation platform</p>
      </div>
      <div class="flex gap-2">
        <RouterLink to="/prompt" class="btn-primary">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Generate Test Cases
        </RouterLink>
        <RouterLink to="/execution" class="btn-secondary">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          </svg>
          Run Execution
        </RouterLink>
      </div>
    </div>

    <!-- Skeleton state -->
    <div v-if="loading" class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div v-for="i in 4" :key="i" class="glass-card p-5 h-28 skeleton" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="glass-card p-8 text-center mb-6">
      <div class="text-red-400 text-4xl mb-3">⚠️</div>
      <p class="text-gray-600 dark:text-gray-400 mb-3">Failed to load dashboard data</p>
      <button @click="load" class="btn-primary btn-sm">Retry</button>
    </div>

    <!-- Stats Cards -->
    <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="glass-card p-5 group hover:shadow-md transition-all duration-200"
      >
        <div class="flex items-start justify-between mb-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="stat.iconBg">
            <span class="text-lg">{{ stat.icon }}</span>
          </div>
          <BaseBadge :variant="stat.trend > 0 ? 'success' : 'danger'" size="sm">
            {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
          </BaseBadge>
        </div>
        <div class="text-2xl font-bold text-gray-900 dark:text-white mb-0.5">{{ stat.value }}</div>
        <div class="text-xs text-gray-500 dark:text-gray-400">{{ stat.label }}</div>
      </div>
    </div>

    <!-- Quick Actions & Activity Feed -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Quick Actions -->
      <BaseCard title="Quick Actions" subtitle="Jump right in">
        <div class="space-y-2">
          <RouterLink
            v-for="action in quickActions"
            :key="action.label"
            :to="action.to"
            class="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group"
          >
            <div class="w-9 h-9 rounded-xl flex items-center justify-center text-base" :class="action.iconBg">
              {{ action.icon }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ action.label }}</p>
              <p class="text-xs text-gray-500 truncate">{{ action.desc }}</p>
            </div>
            <svg class="w-4 h-4 text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </RouterLink>
        </div>
      </BaseCard>

      <!-- Recent Activity -->
      <BaseCard title="Recent Activity" subtitle="Last 7 days" class="lg:col-span-2">
        <div v-if="activity.length === 0" class="py-8 text-center">
          <div class="text-4xl mb-2">📭</div>
          <p class="text-sm text-gray-500 dark:text-gray-400">No recent activity</p>
          <RouterLink to="/prompt" class="btn-primary btn-sm mt-3 inline-flex">Get Started</RouterLink>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="item in activity"
            :key="item.id"
            class="flex items-start gap-3 p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
          >
            <div
              class="w-8 h-8 rounded-full flex items-center justify-center text-sm shrink-0"
              :class="activityIconClass(item.type)"
            >
              {{ activityIcon(item.type) }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-gray-800 dark:text-gray-200 font-medium leading-snug">{{ item.title }}</p>
              <p class="text-xs text-gray-500 mt-0.5">{{ formatTime(item.timestamp) }} · {{ item.user }}</p>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>

    <!-- Onboarding banner (shown only if no test cases) -->
    <Transition name="fade">
      <div v-if="showOnboarding" class="mt-6 glass-card p-6 border-l-4 border-brand-500 bg-brand-50/50 dark:bg-brand-950/30">
        <div class="flex items-start gap-4">
          <div class="text-3xl">🚀</div>
          <div>
            <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-1">Get started with TestAI</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Start by entering a prompt — paste a Confluence link, Jira ticket, or describe your feature. TestAI will generate BDD test cases and Selenium code automatically.
            </p>
            <RouterLink to="/prompt" class="btn-primary btn-sm">Create Your First Test Case →</RouterLink>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { api } from '@/mocks/api'
import type { DashboardStats, ActivityItem } from '@/types'

const loading = ref(true)
const error = ref<string | null>(null)
const statsData = ref<DashboardStats | null>(null)
const activity = ref<ActivityItem[]>([])

const showOnboarding = computed(() => !loading.value && activity.value.length === 0)

const stats = computed(() => {
  if (!statsData.value) return []
  return [
    { label: 'Total Test Cases', value: statsData.value.totalTestCases, icon: '🗂️', iconBg: 'bg-brand-100 dark:bg-brand-900/40', trend: 12 },
    { label: 'Tests Passed', value: statsData.value.passed, icon: '✅', iconBg: 'bg-emerald-100 dark:bg-emerald-900/30', trend: 8 },
    { label: 'Tests Failed', value: statsData.value.failed, icon: '❌', iconBg: 'bg-red-100 dark:bg-red-900/30', trend: -3 },
    { label: 'Recent Executions', value: statsData.value.recentExecutions, icon: '⚡', iconBg: 'bg-amber-100 dark:bg-amber-900/30', trend: 25 },
  ]
})

const quickActions = [
  { label: 'Generate Test Cases', desc: 'Enter a prompt to create BDD + Selenium tests', to: '/prompt', icon: '✨', iconBg: 'bg-brand-100 dark:bg-brand-900/40 text-brand-600' },
  { label: 'Review Test Cases', desc: 'Edit and approve generated tests', to: '/review', icon: '🔍', iconBg: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600' },
  { label: 'Push to Zephyr', desc: 'Sync approved tests to Zephyr', to: '/zephyr', icon: '☁️', iconBg: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600' },
  { label: 'Run Execution', desc: 'Execute tests via Harness pipeline', to: '/execution', icon: '▶️', iconBg: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600' },
]

function activityIcon(type: string) {
  return { generated: '✨', approved: '✅', executed: '⚡', synced: '☁️', failed: '❌' }[type] || '•'
}
function activityIconClass(type: string) {
  return {
    generated: 'bg-brand-100 dark:bg-brand-900/40',
    approved: 'bg-emerald-100 dark:bg-emerald-900/30',
    executed: 'bg-amber-100 dark:bg-amber-900/30',
    synced: 'bg-purple-100 dark:bg-purple-900/30',
    failed: 'bg-red-100 dark:bg-red-900/30',
  }[type] || 'bg-gray-100'
}
function formatTime(ts: string) {
  return new Date(ts).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function load() {
  loading.value = true
  error.value = null
  try {
    const [s, a] = await Promise.all([api.getDashboardStats(), api.getActivityFeed()])
    statsData.value = s
    activity.value = a
  } catch (e) {
    error.value = String(e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
