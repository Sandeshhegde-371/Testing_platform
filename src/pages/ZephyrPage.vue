<template>
  <div class="animate-fade-in">
    <div class="page-header flex items-center justify-between">
      <div>
        <h1 class="page-title">Zephyr Integration</h1>
        <p class="page-subtitle">Sync approved test cases to your Zephyr Scale project</p>
      </div>
      <button @click="syncAll" :disabled="syncing" class="btn-primary">
        <svg v-if="syncing" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        {{ syncing ? 'Syncing...' : 'Sync All Approved' }}
      </button>
    </div>

    <!-- Connection Status & Project Info -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <BaseCard>
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="config?.connected ? 'bg-emerald-100 dark:bg-emerald-900/30' : 'bg-red-100 dark:bg-red-900/30'">
            <span class="text-xl">{{ config?.connected ? '🟢' : '🔴' }}</span>
          </div>
          <div>
            <p class="text-xs text-gray-500">Connection</p>
            <p class="text-sm font-semibold" :class="config?.connected ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'">
              {{ config?.connected ? 'Connected' : 'Disconnected' }}
            </p>
          </div>
        </div>
      </BaseCard>
      <BaseCard>
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-brand-100 dark:bg-brand-900/30 flex items-center justify-center text-xl">🗂️</div>
          <div>
            <p class="text-xs text-gray-500">Project Key</p>
            <p class="text-sm font-semibold font-mono text-gray-900 dark:text-white">{{ config?.projectKey || '—' }}</p>
          </div>
        </div>
      </BaseCard>
      <BaseCard>
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-xl">🕒</div>
          <div>
            <p class="text-xs text-gray-500">Last Sync</p>
            <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ config?.lastSync ? formatDate(config.lastSync) : 'Never' }}</p>
          </div>
        </div>
      </BaseCard>
    </div>

    <!-- Not connected warning -->
    <Transition name="fade">
      <div v-if="config && !config.connected" class="glass-card p-5 mb-4 border-l-4 border-red-500 bg-red-50/50 dark:bg-red-950/20">
        <div class="flex items-start gap-3">
          <span class="text-2xl">⚠️</span>
          <div>
            <p class="text-sm font-semibold text-gray-900 dark:text-white mb-1">Zephyr not connected</p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Check your Zephyr API credentials in Settings. Contact your admin if the issue persists.</p>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Synced cases table -->
    <BaseCard title="Synced Test Cases" :subtitle="`${syncedCases.length} cases synced to Zephyr`">
      <div v-if="loading" class="space-y-3 py-2">
        <div v-for="i in 4" :key="i" class="skeleton h-10 rounded-lg" />
      </div>

      <div v-else-if="syncedCases.length === 0" class="py-8 text-center">
        <div class="text-4xl mb-3">☁️</div>
        <p class="text-sm text-gray-500">No test cases synced yet</p>
        <p class="text-xs text-gray-400 mt-1">Approve test cases first, then sync them here</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="border-b border-gray-200 dark:border-gray-800">
            <tr>
              <th class="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">ID</th>
              <th class="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Title</th>
              <th class="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Zephyr ID</th>
              <th class="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Sync Status</th>
              <th class="py-2 px-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr
              v-for="tc in syncedCases"
              :key="tc.id"
              class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition-colors"
            >
              <td class="py-3 px-3 font-mono text-xs text-gray-500">{{ tc.id }}</td>
              <td class="py-3 px-3 font-medium text-gray-900 dark:text-white">{{ tc.title }}</td>
              <td class="py-3 px-3 font-mono text-xs text-brand-600 dark:text-brand-400">{{ tc.zephyrId || '—' }}</td>
              <td class="py-3 px-3">
                <BaseBadge :variant="syncVariant(tc.syncStatus)" dot>{{ tc.syncStatus }}</BaseBadge>
              </td>
              <td class="py-3 px-3 text-right">
                <button @click="repush(tc.id)" class="btn-ghost btn-sm text-xs">Re-sync</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>

    <!-- Pending cases -->
    <BaseCard class="mt-4" title="Awaiting Sync" :subtitle="`${pendingCases.length} approved cases not yet synced`">
      <div v-if="pendingCases.length === 0" class="py-4 text-center text-sm text-gray-500">All approved cases are synced ✓</div>
      <div v-else class="space-y-2">
        <div
          v-for="tc in pendingCases"
          :key="tc.id"
          class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl"
        >
          <div>
            <span class="font-mono text-xs text-gray-500 mr-2">{{ tc.id }}</span>
            <span class="text-sm font-medium text-gray-900 dark:text-white">{{ tc.title }}</span>
          </div>
          <button @click="pushOne(tc.id)" :disabled="syncing" class="btn-primary btn-sm">Push</button>
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { useTestCaseStore } from '@/stores/useTestCaseStore'
import { api } from '@/mocks/api'
import type { ZephyrConfig } from '@/types'

const store = useTestCaseStore()
const toast = useToast()

const config = ref<ZephyrConfig | null>(null)
const loading = ref(true)
const syncing = ref(false)

const syncedCases = computed(() => store.testCases.filter(t => t.syncStatus === 'synced'))
const pendingCases = computed(() => store.testCases.filter(t => t.status === 'approved' && t.syncStatus !== 'synced'))

function formatDate(d: string) { return new Date(d).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }

function syncVariant(s: string): 'success' | 'danger' | 'warning' | 'gray' | 'info' | 'purple' {
  return { synced: 'success', failed: 'danger', syncing: 'info', not_synced: 'gray' }[s] as 'success' | 'danger' | 'warning' | 'gray' | 'info' | 'purple' || 'gray'
}

async function syncAll() {
  if (!config.value?.connected) { toast.error('Zephyr not connected'); return }
  const ids = pendingCases.value.map(t => t.id)
  if (!ids.length) { toast.info('All approved cases are already synced'); return }
  syncing.value = true
  try {
    await api.pushToZephyr(ids, (id) => {
      const tc = store.testCases.find(t => t.id === id)
      if (tc) { tc.syncStatus = 'synced'; tc.zephyrId = `ZTC-${Math.floor(Math.random() * 9000) + 1000}` }
    })
    toast.success(`${ids.length} test cases synced to Zephyr!`)
  } catch {
    toast.error('Sync failed. Check your connection and retry.')
  } finally {
    syncing.value = false
  }
}

async function pushOne(id: string) {
  syncing.value = true
  try {
    await api.pushToZephyr([id], () => {
      const tc = store.testCases.find(t => t.id === id)
      if (tc) { tc.syncStatus = 'synced'; tc.zephyrId = `ZTC-${Math.floor(Math.random() * 9000) + 1000}` }
    })
    toast.success('Pushed to Zephyr')
  } finally { syncing.value = false }
}

async function repush(id: string) {
  toast.info(`Re-syncing ${id}...`)
  await new Promise(r => setTimeout(r, 800))
  toast.success(`${id} re-synced`)
}

onMounted(async () => {
  config.value = await api.getZephyrConfig()
  loading.value = false
})
</script>
