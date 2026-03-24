<template>
  <div class="animate-fade-in">
    <div class="page-header flex items-center justify-between">
      <div>
        <h1 class="page-title">Approval Queue</h1>
        <p class="page-subtitle">Review and approve test cases before pushing to Zephyr</p>
      </div>
      <div class="flex gap-2">
        <button
          @click="bulkApprove"
          :disabled="store.selectedIds.size === 0"
          class="btn-success"
        >
          ✓ Approve Selected ({{ store.selectedIds.size }})
        </button>
        <button
          @click="pushSelected"
          :disabled="store.approvedCases.length === 0 || pushing"
          class="btn-primary"
        >
          <svg v-if="pushing" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Push to Zephyr
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="glass-card p-4 mb-4 flex items-center gap-3 flex-wrap">
      <input v-model="search" type="text" placeholder="Search test cases..." class="form-input w-56" />
      <select v-model="filterStatus" class="form-input w-40">
        <option value="">All Status</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
        <option value="pending">Pending</option>
        <option value="draft">Draft</option>
      </select>
      <select v-model="filterType" class="form-input w-36">
        <option value="">All Types</option>
        <option value="UI">UI</option>
        <option value="API">API</option>
        <option value="Regression">Regression</option>
      </select>
      <button @click="store.selectAll()" class="btn-ghost btn-sm">Select All</button>
      <button @click="store.clearSelection()" class="btn-ghost btn-sm">Clear</button>
      <span class="text-xs text-gray-500 ml-auto">{{ filtered.length }} results</span>
    </div>

    <!-- Empty state -->
    <div v-if="filtered.length === 0" class="glass-card p-12 text-center">
      <div class="text-5xl mb-4">🔍</div>
      <h3 class="text-base font-semibold text-gray-900 dark:text-white mb-2">No test cases found</h3>
      <p class="text-sm text-gray-500">Try adjusting your filters or generate new test cases</p>
    </div>

    <!-- Table -->
    <div v-else class="glass-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700">
            <tr>
              <th class="px-4 py-3 text-left w-10">
                <input type="checkbox" :checked="allSelected" @change="toggleAll" class="rounded" />
              </th>
              <th class="px-4 py-3 text-left font-semibold text-gray-600 dark:text-gray-400 cursor-pointer" @click="sort('id')">
                ID <span class="text-gray-400">{{ sortKey === 'id' ? (sortAsc ? '↑' : '↓') : '↕' }}</span>
              </th>
              <th class="px-4 py-3 text-left font-semibold text-gray-600 dark:text-gray-400 cursor-pointer" @click="sort('title')">
                Title <span class="text-gray-400">{{ sortKey === 'title' ? (sortAsc ? '↑' : '↓') : '↕' }}</span>
              </th>
              <th class="px-4 py-3 text-left font-semibold text-gray-600 dark:text-gray-400">Type</th>
              <th class="px-4 py-3 text-left font-semibold text-gray-600 dark:text-gray-400 cursor-pointer" @click="sort('status')">
                Status <span class="text-gray-400">{{ sortKey === 'status' ? (sortAsc ? '↑' : '↓') : '↕' }}</span>
              </th>
              <th class="px-4 py-3 text-left font-semibold text-gray-600 dark:text-gray-400">Zephyr ID</th>
              <th class="px-4 py-3 text-left font-semibold text-gray-600 dark:text-gray-400 cursor-pointer" @click="sort('updatedAt')">
                Updated <span class="text-gray-400">{{ sortKey === 'updatedAt' ? (sortAsc ? '↑' : '↓') : '↕' }}</span>
              </th>
              <th class="px-4 py-3 text-right font-semibold text-gray-600 dark:text-gray-400">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr
              v-for="tc in sorted"
              :key="tc.id"
              class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition-colors"
              :class="{ 'bg-brand-50/30 dark:bg-brand-950/20': store.selectedIds.has(tc.id) }"
            >
              <td class="px-4 py-3">
                <input type="checkbox" :checked="store.selectedIds.has(tc.id)" @change="store.toggleSelect(tc.id)" class="rounded" />
              </td>
              <td class="px-4 py-3 font-mono text-xs text-gray-500">{{ tc.id }}</td>
              <td class="px-4 py-3">
                <RouterLink :to="'/review'" class="font-medium text-gray-900 dark:text-white hover:text-brand-600 dark:hover:text-brand-400 truncate max-w-xs block">
                  {{ tc.title }}
                </RouterLink>
              </td>
              <td class="px-4 py-3"><BaseBadge variant="gray">{{ tc.type }}</BaseBadge></td>
              <td class="px-4 py-3"><BaseBadge :variant="statusVariant(tc.status)" dot>{{ tc.status }}</BaseBadge></td>
              <td class="px-4 py-3 font-mono text-xs text-gray-500">{{ tc.zephyrId || '—' }}</td>
              <td class="px-4 py-3 text-xs text-gray-500">{{ formatDate(tc.updatedAt) }}</td>
              <td class="px-4 py-3">
                <div class="flex items-center justify-end gap-1">
                  <button @click="quickApprove(tc.id)" class="btn-ghost btn-sm text-emerald-600" title="Approve">✓</button>
                  <button @click="quickReject(tc.id)" class="btn-ghost btn-sm text-red-600" title="Reject">✗</button>
                  <button @click="deleteTC(tc.id)" class="btn-ghost btn-sm text-gray-500" title="Delete">🗑</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <BaseModal v-model="showDeleteModal" title="Delete Test Case" description="Are you sure? This action cannot be undone." size="sm">
      <template #footer>
        <button @click="showDeleteModal = false" class="btn-secondary">Cancel</button>
        <button @click="confirmDelete" class="btn-danger">Delete</button>
      </template>
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import { useTestCaseStore } from '@/stores/useTestCaseStore'
import { api } from '@/mocks/api'
import type { TestCase } from '@/types'

const store = useTestCaseStore()
const toast = useToast()

const search = ref('')
const filterStatus = ref('')
const filterType = ref('')
const sortKey = ref<keyof TestCase>('updatedAt')
const sortAsc = ref(false)
const pushing = ref(false)
const showDeleteModal = ref(false)
const deleteTargetId = ref<string | null>(null)

const filtered = computed(() =>
  store.testCases.filter(tc => {
    const matchSearch = !search.value || tc.title.toLowerCase().includes(search.value.toLowerCase()) || tc.id.toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = !filterStatus.value || tc.status === filterStatus.value
    const matchType = !filterType.value || tc.type === filterType.value
    return matchSearch && matchStatus && matchType
  })
)

const sorted = computed(() => {
  return [...filtered.value].sort((a, b) => {
    const av = String(a[sortKey.value] || '')
    const bv = String(b[sortKey.value] || '')
    return sortAsc.value ? av.localeCompare(bv) : bv.localeCompare(av)
  })
})

const allSelected = computed(() => filtered.value.length > 0 && filtered.value.every(t => store.selectedIds.has(t.id)))

function sort(key: keyof TestCase) {
  if (sortKey.value === key) sortAsc.value = !sortAsc.value
  else { sortKey.value = key; sortAsc.value = true }
}

function toggleAll(e: Event) {
  if ((e.target as HTMLInputElement).checked) store.selectAll()
  else store.clearSelection()
}

function statusVariant(status: string): 'success' | 'danger' | 'warning' | 'gray' | 'info' | 'purple' {
  return { approved: 'success', rejected: 'danger', pending: 'warning', draft: 'gray' }[status] as 'success' | 'danger' | 'warning' | 'gray' || 'gray'
}

function formatDate(d: string) { return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: '2-digit' }) }

async function quickApprove(id: string) {
  await store.updateStatus(id, 'approved')
  toast.success('Approved')
}
async function quickReject(id: string) {
  await store.updateStatus(id, 'rejected')
  toast.info('Rejected')
}

function deleteTC(id: string) {
  deleteTargetId.value = id
  showDeleteModal.value = true
}
async function confirmDelete() {
  if (deleteTargetId.value) {
    await store.deleteTC(deleteTargetId.value)
    toast.success('Test case deleted')
  }
  showDeleteModal.value = false
}

async function bulkApprove() {
  for (const id of store.selectedIds) {
    await store.updateStatus(id, 'approved')
  }
  toast.success(`${store.selectedIds.size} test cases approved`)
  store.clearSelection()
}

async function pushSelected() {
  const ids = store.approvedCases.map(t => t.id)
  if (ids.length === 0) return
  pushing.value = true
  try {
    await api.pushToZephyr(ids, (id) => {
      toast.info(`Pushed ${id} to Zephyr`)
    })
    toast.success(`${ids.length} test cases pushed to Zephyr`)
  } catch {
    toast.error('Failed to push to Zephyr. Please try again.')
  } finally {
    pushing.value = false
  }
}
</script>
