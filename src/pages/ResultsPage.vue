<template>
  <div class="animate-fade-in">
    <div class="page-header flex items-center justify-between">
      <div>
        <h1 class="page-title">Results & Insights</h1>
        <p class="page-subtitle">Execution summary with AI-powered root cause analysis</p>
      </div>
      <div class="flex gap-2">
        <RouterLink to="/execution" class="btn-secondary">↩ Back to Execution</RouterLink>
        <button class="btn-primary">📥 Export Report</button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div class="grid grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="glass-card p-5 h-24 skeleton" />
      </div>
      <div class="glass-card p-5 h-64 skeleton" />
    </div>

    <!-- No results -->
    <div v-else-if="!summary" class="glass-card p-12 text-center">
      <div class="text-5xl mb-4">📊</div>
      <h3 class="text-base font-semibold text-gray-900 dark:text-white mb-2">No results yet</h3>
      <p class="text-sm text-gray-500 mb-4">Run an execution to see results and AI insights here</p>
      <RouterLink to="/execution" class="btn-primary">Go to Execution</RouterLink>
    </div>

    <div v-else>
      <!-- Summary stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div class="glass-card p-5">
          <div class="text-2xl mb-1">
            <span class="text-3xl font-bold text-gray-900 dark:text-white">{{ summary.passRate }}%</span>
          </div>
          <p class="text-xs text-gray-500">Pass Rate</p>
          <div class="mt-2 h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 rounded-full" :style="{ width: summary.passRate + '%' }" />
          </div>
        </div>
        <div class="glass-card p-5">
          <div class="text-3xl font-bold text-emerald-600 dark:text-emerald-400 mb-1">{{ summary.passed }}</div>
          <p class="text-xs text-gray-500">Tests Passed</p>
        </div>
        <div class="glass-card p-5">
          <div class="text-3xl font-bold text-red-600 dark:text-red-400 mb-1">{{ summary.failed }}</div>
          <p class="text-xs text-gray-500">Tests Failed</p>
        </div>
        <div class="glass-card p-5">
          <div class="text-3xl font-bold text-gray-900 dark:text-white mb-1">{{ formatDuration(summary.duration) }}</div>
          <p class="text-xs text-gray-500">Total Duration</p>
        </div>
      </div>

      <!-- Results table + detail panel -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">

        <!-- Results table -->
        <div class="lg:col-span-3">
          <BaseCard title="Test Results" :subtitle="`Execution ID: ${summary.executionId}`">
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead class="border-b border-gray-200 dark:border-gray-800">
                  <tr>
                    <th class="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase">Test Case</th>
                    <th class="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase">Status</th>
                    <th class="py-2 px-3 text-left text-xs font-semibold text-gray-500 uppercase">Duration</th>
                    <th class="py-2 px-3 text-right text-xs font-semibold text-gray-500 uppercase">Details</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr
                    v-for="result in summary.results"
                    :key="result.testCaseId"
                    class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition-colors cursor-pointer"
                    :class="{ 'bg-brand-50/30 dark:bg-brand-950/20': selectedResult?.testCaseId === result.testCaseId }"
                    @click="selectedResult = result"
                  >
                    <td class="py-3 px-3">
                      <p class="font-medium text-gray-900 dark:text-white text-xs leading-snug">{{ result.testCaseTitle }}</p>
                      <p class="text-xs text-gray-500 font-mono">{{ result.testCaseId }}</p>
                    </td>
                    <td class="py-3 px-3">
                      <BaseBadge :variant="result.status === 'passed' ? 'success' : 'danger'" dot>{{ result.status }}</BaseBadge>
                    </td>
                    <td class="py-3 px-3 text-xs text-gray-500">{{ (result.duration / 1000).toFixed(1) }}s</td>
                    <td class="py-3 px-3 text-right">
                      <button @click.stop="selectedResult = result" class="btn-ghost btn-sm text-xs">View →</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- No failures message -->
            <div v-if="summary.failed === 0" class="mt-4 p-3 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl text-sm text-emerald-700 dark:text-emerald-400">
              🎉 No failures! All test cases passed successfully.
            </div>
          </BaseCard>
        </div>

        <!-- Detail panel -->
        <div class="lg:col-span-2 space-y-4">
          <div v-if="!selectedResult" class="glass-card p-8 text-center">
            <div class="text-3xl mb-2">👈</div>
            <p class="text-sm text-gray-500">Click a result to see details</p>
          </div>

          <template v-else>
            <!-- Logs -->
            <BaseCard :title="selectedResult.testCaseTitle" subtitle="Execution logs">
              <LogViewer :logs="selectedResult.logs" title="Test Logs" />
            </BaseCard>

            <!-- Artifacts -->
            <BaseCard title="Artifacts" subtitle="Screenshots and reports">
              <div class="space-y-2">
                <div
                  v-for="artifact in [...selectedResult.screenshots, ...selectedResult.artifacts]"
                  :key="artifact"
                  class="flex items-center gap-3 p-2.5 bg-gray-50 dark:bg-gray-800 rounded-xl"
                >
                  <span class="text-lg">{{ artifact.endsWith('.png') ? '🖼️' : '📄' }}</span>
                  <span class="text-xs font-mono text-gray-700 dark:text-gray-300 flex-1">{{ artifact }}</span>
                  <button class="btn-ghost btn-sm text-xs">Download</button>
                </div>
                <div v-if="!selectedResult.screenshots.length && !selectedResult.artifacts.length" class="text-xs text-gray-500 text-center py-2">
                  No artifacts
                </div>
              </div>
            </BaseCard>

            <!-- AI Insights -->
            <BaseCard title="🤖 AI Insights" subtitle="Root cause analysis">
              <div v-if="selectedResult.status === 'passed'" class="p-3 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl text-sm text-emerald-700 dark:text-emerald-400">
                ✅ This test passed. No issues detected.
              </div>
              <div v-else-if="selectedResult.aiInsight" class="space-y-3">
                <div class="p-3 bg-red-50 dark:bg-red-900/20 rounded-xl">
                  <p class="text-xs font-semibold text-red-700 dark:text-red-400 mb-1">Root Cause</p>
                  <p class="text-sm text-red-800 dark:text-red-300">{{ selectedResult.aiInsight.rootCause }}</p>
                </div>
                <div class="p-3 bg-amber-50 dark:bg-amber-900/20 rounded-xl">
                  <p class="text-xs font-semibold text-amber-700 dark:text-amber-400 mb-1">Suggested Fix</p>
                  <p class="text-sm text-amber-800 dark:text-amber-300">{{ selectedResult.aiInsight.suggestedFix }}</p>
                </div>
                <div v-if="selectedResult.aiInsight.impactedTests.length" class="p-3 bg-brand-50 dark:bg-brand-900/20 rounded-xl">
                  <p class="text-xs font-semibold text-brand-700 dark:text-brand-400 mb-1">Impacted Tests</p>
                  <div class="flex flex-wrap gap-1">
                    <BaseBadge v-for="t in selectedResult.aiInsight.impactedTests" :key="t" variant="info">{{ t }}</BaseBadge>
                  </div>
                </div>
              </div>
              <div v-else class="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl text-sm text-gray-500">
                AI analysis not available for this test case.
              </div>
            </BaseCard>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import LogViewer from '@/components/ui/LogViewer.vue'
import { useExecutionStore } from '@/stores/useExecutionStore'
import type { TestResult } from '@/types'

const execStore = useExecutionStore()
const loading = ref(false)
const summary = ref(execStore.executionSummary)
const selectedResult = ref<TestResult | null>(null)

function formatDuration(ms: number) {
  const s = Math.floor(ms / 1000)
  if (s < 60) return `${s}s`
  return `${Math.floor(s / 60)}m ${s % 60}s`
}

onMounted(async () => {
  if (!summary.value && execStore.currentExecution) {
    loading.value = true
    await execStore.fetchResults(execStore.currentExecution.id)
    summary.value = execStore.executionSummary
    loading.value = false
  }
})
</script>
