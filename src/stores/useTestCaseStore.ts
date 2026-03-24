import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { TestCase, TestStatus } from '@/types'
import { api, mockTestCases } from '@/mocks/api'

export const useTestCaseStore = defineStore('testCases', () => {
  const testCases = ref<TestCase[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedIds = ref<Set<string>>(new Set())

  const approvedCases = computed(() => testCases.value.filter(t => t.status === 'approved'))
  const pendingCases = computed(() => testCases.value.filter(t => t.status === 'pending'))
  const rejectedCases = computed(() => testCases.value.filter(t => t.status === 'rejected'))

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      testCases.value = await api.getTestCases()
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to load test cases'
    } finally {
      loading.value = false
    }
  }

  function seedFromGeneration(generated: TestCase[]) {
    // Add newly generated test cases (avoid duplicates)
    for (const tc of generated) {
      if (!testCases.value.find(t => t.id === tc.id)) {
        testCases.value.unshift(tc)
      }
    }
  }

  async function updateStatus(id: string, status: TestStatus) {
    try {
      await api.updateTestCase(id, { status })
      const tc = testCases.value.find(t => t.id === id)
      if (tc) {
        tc.status = status
        tc.updatedAt = new Date().toISOString()
      }
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to update'
      throw e
    }
  }

  async function updateContent(id: string, patch: Partial<TestCase>) {
    await api.updateTestCase(id, patch)
    const tc = testCases.value.find(t => t.id === id)
    if (tc) Object.assign(tc, patch, { updatedAt: new Date().toISOString() })
  }

  async function deleteTC(id: string) {
    await api.deleteTestCase(id)
    testCases.value = testCases.value.filter(t => t.id !== id)
    selectedIds.value.delete(id)
  }

  function toggleSelect(id: string) {
    if (selectedIds.value.has(id)) {
      selectedIds.value.delete(id)
    } else {
      selectedIds.value.add(id)
    }
  }

  function selectAll() {
    testCases.value.forEach(t => selectedIds.value.add(t.id))
  }

  function clearSelection() {
    selectedIds.value.clear()
  }

  // Hydrate with mock data immediately
  testCases.value = [...mockTestCases]

  return {
    testCases,
    loading,
    error,
    selectedIds,
    approvedCases,
    pendingCases,
    rejectedCases,
    fetchAll,
    seedFromGeneration,
    updateStatus,
    updateContent,
    deleteTC,
    toggleSelect,
    selectAll,
    clearSelection,
  }
})
