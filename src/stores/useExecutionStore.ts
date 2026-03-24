import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Execution, ExecutionStatus, LogEntry, ExecutionSummary } from '@/types'
import { api } from '@/mocks/api'

export const useExecutionStore = defineStore('execution', () => {
  const currentExecution = ref<Execution | null>(null)
  const executionSummary = ref<ExecutionSummary | null>(null)
  const logs = ref<LogEntry[]>([])
  const status = ref<ExecutionStatus>('pending')
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function runExecution(testCaseIds: string[]) {
    loading.value = true
    error.value = null
    status.value = 'running'
    logs.value = []

    try {
      const execution = await api.runExecution(testCaseIds, (msg) => {
        logs.value.push({
          timestamp: new Date().toLocaleTimeString(),
          level: msg.includes('PASSED') || msg.includes('successfully') ? 'success'
            : msg.includes('STARTED') || msg.includes('Starting') ? 'action'
            : 'info',
          message: msg,
        })
      })
      currentExecution.value = execution
      status.value = 'passed'
      return execution
    } catch (e: unknown) {
      status.value = 'failed'
      error.value = e instanceof Error ? e.message : 'Execution failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchResults(executionId: string) {
    loading.value = true
    try {
      executionSummary.value = await api.getExecutionResults(executionId)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to load results'
    } finally {
      loading.value = false
    }
  }

  function reset() {
    currentExecution.value = null
    executionSummary.value = null
    logs.value = []
    status.value = 'pending'
    error.value = null
  }

  return { currentExecution, executionSummary, logs, status, loading, error, runExecution, fetchResults, reset }
})
