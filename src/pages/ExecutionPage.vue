<template>
  <div class="animate-fade-in">
    <div class="page-header">
      <h1 class="page-title">Test Execution</h1>
      <p class="page-subtitle">Select test cases and trigger a Harness pipeline run</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">

      <!-- Test case selector -->
      <div class="lg:col-span-2 space-y-4">
        <BaseCard title="Select Test Cases" :subtitle="`${selectedCount} selected`">
          <div class="space-y-1 max-h-96 overflow-y-auto pr-1">
            <div
              v-for="tc in store.approvedCases"
              :key="tc.id"
              class="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800/50 cursor-pointer transition-colors"
              :class="{ 'bg-brand-50 dark:bg-brand-950/30': store.selectedIds.has(tc.id) }"
              @click="store.toggleSelect(tc.id)"
            >
              <input type="checkbox" :checked="store.selectedIds.has(tc.id)" class="rounded pointer-events-none" />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ tc.title }}</p>
                <div class="flex items-center gap-2 mt-0.5">
                  <span class="text-xs font-mono text-gray-500">{{ tc.id }}</span>
                  <BaseBadge variant="gray">{{ tc.type }}</BaseBadge>
                </div>
              </div>
            </div>

            <div v-if="store.approvedCases.length === 0" class="py-6 text-center">
              <div class="text-3xl mb-2">📋</div>
              <p class="text-xs text-gray-500">No approved test cases</p>
              <RouterLink to="/approval" class="text-xs text-brand-600 hover:underline">Go to Approval</RouterLink>
            </div>
          </div>

          <div class="flex gap-2 mt-3 pt-3 border-t border-gray-100 dark:border-gray-800">
            <button @click="store.selectAll()" class="btn-secondary btn-sm flex-1">Select All</button>
            <button @click="store.clearSelection()" class="btn-ghost btn-sm flex-1">Clear</button>
          </div>
        </BaseCard>

        <!-- Execution config -->
        <BaseCard title="Pipeline Configuration">
          <div class="space-y-3">
            <div>
              <label class="form-label">Pipeline</label>
              <select class="form-input">
                <option>harness-pipeline-main</option>
                <option>harness-pipeline-regression</option>
                <option>harness-pipeline-smoke</option>
              </select>
            </div>
            <div>
              <label class="form-label">Environment</label>
              <select class="form-input">
                <option>staging</option>
                <option>qa</option>
                <option>production</option>
              </select>
            </div>
            <button
              @click="runExecution"
              :disabled="selectedCount === 0 || execStore.loading"
              class="btn-primary w-full justify-center"
            >
              <svg v-if="execStore.loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              ▶ Run via Harness
            </button>
          </div>
        </BaseCard>
      </div>

      <!-- Execution panel -->
      <div class="lg:col-span-3 space-y-4">

        <!-- Status card -->
        <BaseCard title="Execution Status">
          <div v-if="!execStore.currentExecution && !execStore.loading" class="py-8 text-center">
            <div class="text-4xl mb-3">⚡</div>
            <p class="text-sm text-gray-500">No active execution</p>
            <p class="text-xs text-gray-400 mt-1">Select test cases and click "Run via Harness"</p>
          </div>

          <div v-else class="space-y-4">
            <!-- Execution info -->
            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl">
                <p class="text-xs text-gray-500 mb-1">Execution ID</p>
                <p class="text-sm font-mono font-medium text-gray-900 dark:text-white">
                  {{ execStore.currentExecution?.id || 'Pending...' }}
                </p>
              </div>
              <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl">
                <p class="text-xs text-gray-500 mb-1">Status</p>
                <BaseBadge :variant="statusVariant(execStore.status)" dot>{{ execStore.status }}</BaseBadge>
              </div>
            </div>

            <!-- Progress bar during run -->
            <div v-if="execStore.loading" class="space-y-1">
              <div class="flex justify-between text-xs text-gray-500">
                <span>Running {{ selectedCount }} test(s)...</span>
                <span>{{ Math.min(execStore.logs.length * 10, 95) }}%</span>
              </div>
              <div class="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                <div
                  class="h-full bg-brand-500 rounded-full transition-all duration-500"
                  :style="{ width: Math.min(execStore.logs.length * 10, 95) + '%' }"
                />
              </div>
            </div>

            <!-- Done state -->
            <div v-if="execStore.status === 'passed'" class="p-3 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl text-sm text-emerald-700 dark:text-emerald-400">
              ✅ Execution completed successfully!
              <RouterLink to="/results" class="ml-2 font-medium underline">View Results →</RouterLink>
            </div>
            <div v-if="execStore.status === 'failed'" class="p-3 bg-red-50 dark:bg-red-900/20 rounded-xl text-sm text-red-700 dark:text-red-400">
              ❌ Execution failed. Check logs for details.
              <button @click="runExecution" class="ml-2 font-medium underline">Retry</button>
            </div>
          </div>
        </BaseCard>

        <!-- Live logs -->
        <BaseCard title="Live Logs">
          <LogViewer :logs="execStore.logs" :streaming="execStore.loading" title="Harness Pipeline Output" />
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useToast } from 'vue-toastification'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import LogViewer from '@/components/ui/LogViewer.vue'
import { useTestCaseStore } from '@/stores/useTestCaseStore'
import { useExecutionStore } from '@/stores/useExecutionStore'
import type { ExecutionStatus } from '@/types'

const store = useTestCaseStore()
const execStore = useExecutionStore()
const toast = useToast()

const selectedCount = computed(() => store.selectedIds.size)

function statusVariant(s: ExecutionStatus): 'success' | 'danger' | 'warning' | 'gray' | 'info' | 'purple' {
  return { passed: 'success', failed: 'danger', running: 'info', pending: 'gray', cancelled: 'warning' }[s] as 'success' | 'danger' | 'warning' | 'gray' | 'info' | 'purple' || 'gray'
}

async function runExecution() {
  const ids = [...store.selectedIds]
  if (ids.length === 0) { toast.warning('Select at least one test case'); return }
  execStore.reset()
  try {
    await execStore.runExecution(ids)
    toast.success('Execution completed!')
  } catch {
    toast.error('Execution failed')
  }
}
</script>
