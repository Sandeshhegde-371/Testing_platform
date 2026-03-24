<template>
  <div class="animate-fade-in">
    <div class="page-header flex items-center justify-between">
      <div>
        <h1 class="page-title">Review Test Cases</h1>
        <p class="page-subtitle">Edit, approve, or reject generated BDD scenarios and Selenium code</p>
      </div>
      <div class="flex gap-2">
        <button @click="approveAll" class="btn-success btn-sm">
          ✓ Approve All
        </button>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="store.testCases.length === 0" class="glass-card p-12 text-center">
      <div class="text-5xl mb-4">📭</div>
      <h3 class="text-base font-semibold text-gray-900 dark:text-white mb-2">No test cases yet</h3>
      <p class="text-sm text-gray-500 mb-4">Generate test cases from a prompt to start reviewing</p>
      <RouterLink to="/prompt" class="btn-primary">Generate Test Cases</RouterLink>
    </div>

    <div v-else class="grid grid-cols-1 xl:grid-cols-5 gap-6">

      <!-- Left: TC list -->
      <div class="xl:col-span-2 space-y-2">
        <div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2 px-1">
          {{ store.testCases.length }} test cases · {{ store.approvedCases.length }} approved
        </div>
        <div
          v-for="tc in store.testCases"
          :key="tc.id"
          class="glass-card p-4 cursor-pointer transition-all duration-150 hover:shadow-md"
          :class="{ 'ring-2 ring-brand-500': selectedId === tc.id }"
          @click="select(tc.id)"
        >
          <div class="flex items-start gap-3">
            <input
              type="checkbox"
              :checked="store.selectedIds.has(tc.id)"
              @click.stop="store.toggleSelect(tc.id)"
              class="mt-1 rounded"
            />
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-xs font-mono text-gray-500">{{ tc.id }}</span>
                <BaseBadge :variant="statusVariant(tc.status)">{{ tc.status }}</BaseBadge>
                <BaseBadge variant="gray">{{ tc.type }}</BaseBadge>
              </div>
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ tc.title }}</p>
            </div>
          </div>

          <!-- Quick actions row -->
          <div class="flex gap-1.5 mt-3 pl-7">
            <button @click.stop="quickApprove(tc.id)" class="btn-success btn-sm py-1 text-xs">✓</button>
            <button @click.stop="quickReject(tc.id)" class="btn-danger btn-sm py-1 text-xs">✗</button>
            <button @click.stop="select(tc.id)" class="btn-secondary btn-sm py-1 text-xs">Edit</button>
          </div>
        </div>
      </div>

      <!-- Right: editor area -->
      <div class="xl:col-span-3">
        <div v-if="!selected" class="glass-card p-12 text-center h-full flex flex-col items-center justify-center">
          <div class="text-4xl mb-3">👈</div>
          <p class="text-sm text-gray-500">Select a test case to view and edit</p>
        </div>

        <div v-else class="space-y-4">
          <!-- Header -->
          <BaseCard>
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                <input
                  v-model="selected.title"
                  class="form-input text-base font-semibold mb-2"
                  placeholder="Test case title"
                />
                <div class="flex items-center gap-2">
                  <BaseBadge :variant="statusVariant(selected.status)">{{ selected.status }}</BaseBadge>
                  <BaseBadge variant="gray">{{ selected.type }}</BaseBadge>
                  <span class="text-xs text-gray-500">Last updated {{ formatDate(selected.updatedAt) }}</span>
                </div>
              </div>
              <div class="flex gap-2 shrink-0">
                <button @click="reject" class="btn-danger btn-sm">Reject</button>
                <button @click="regenerate" class="btn-secondary btn-sm">↻ Regen</button>
                <button @click="approve" class="btn-success btn-sm">✓ Approve</button>
              </div>
            </div>
          </BaseCard>

          <!-- BDD / Selenium tabs -->
          <div class="glass-card overflow-hidden">
            <div class="flex border-b border-gray-200 dark:border-gray-800">
              <button
                v-for="tab in ['BDD Scenario', 'Selenium Code']"
                :key="tab"
                @click="activeTab = tab"
                class="px-5 py-3 text-sm font-medium transition-colors"
                :class="activeTab === tab
                  ? 'text-brand-600 dark:text-brand-400 border-b-2 border-brand-600 dark:border-brand-400 -mb-px bg-brand-50/50 dark:bg-brand-950/30'
                  : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'"
              >
                {{ tab }}
              </button>
            </div>

            <div class="p-4">
              <textarea
                v-if="activeTab === 'BDD Scenario'"
                v-model="selected.bddContent"
                rows="18"
                class="w-full bg-gray-950 text-gray-100 font-mono text-xs p-4 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-brand-500 border border-gray-800"
                placeholder="BDD feature file content..."
              />
              <textarea
                v-else
                v-model="selected.seleniumCode"
                rows="18"
                class="w-full bg-gray-950 text-gray-100 font-mono text-xs p-4 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-brand-500 border border-gray-800"
                placeholder="Selenium Java code..."
              />
            </div>

            <!-- Save action -->
            <div class="px-4 pb-4 flex justify-between items-center">
              <span v-if="hasUnsaved" class="text-xs text-amber-600 dark:text-amber-400">⚠️ Unsaved changes</span>
              <span v-else class="text-xs text-gray-400">All changes saved</span>
              <button @click="save" :disabled="!hasUnsaved" class="btn-primary btn-sm">Save Changes</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useToast } from 'vue-toastification'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { useTestCaseStore } from '@/stores/useTestCaseStore'
import type { TestCase } from '@/types'

const store = useTestCaseStore()
const toast = useToast()

const selectedId = ref<string | null>(null)
const activeTab = ref('BDD Scenario')
const hasUnsaved = ref(false)
const editBuffer = ref<TestCase | null>(null)

const selected = computed(() => editBuffer.value)

function select(id: string) {
  if (hasUnsaved.value) {
    if (!confirm('You have unsaved changes. Discard?')) return
  }
  selectedId.value = id
  const tc = store.testCases.find(t => t.id === id)
  editBuffer.value = tc ? { ...tc } : null
  hasUnsaved.value = false
}

watch(editBuffer, () => { hasUnsaved.value = true }, { deep: true })

function statusVariant(status: string): 'success' | 'danger' | 'warning' | 'gray' | 'info' | 'purple' {
  return { approved: 'success', rejected: 'danger', pending: 'warning', draft: 'gray' }[status] as 'success' | 'danger' | 'warning' | 'gray' || 'gray'
}

function formatDate(d: string) { return new Date(d).toLocaleDateString() }

async function save() {
  if (!editBuffer.value) return
  await store.updateContent(editBuffer.value.id, { ...editBuffer.value })
  hasUnsaved.value = false
  toast.success('Changes saved')
}

async function approve() {
  if (!editBuffer.value) return
  await save()
  await store.updateStatus(editBuffer.value.id, 'approved')
  toast.success('Test case approved')
}

async function reject() {
  if (!editBuffer.value) return
  await store.updateStatus(editBuffer.value.id, 'rejected')
  toast.info('Test case rejected')
}

async function quickApprove(id: string) {
  await store.updateStatus(id, 'approved')
  toast.success('Approved')
}

async function quickReject(id: string) {
  await store.updateStatus(id, 'rejected')
}

function regenerate() {
  toast.info('Regenerating... (simulated)')
}

async function approveAll() {
  for (const tc of store.testCases) {
    await store.updateStatus(tc.id, 'approved')
  }
  toast.success('All test cases approved!')
}
</script>
