<template>
  <div class="max-w-2xl mx-auto animate-fade-in">
    <div class="page-header text-center">
      <h1 class="page-title">Generating Test Cases</h1>
      <p class="page-subtitle">AI is analyzing your input and creating test cases</p>
    </div>

    <BaseCard>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Step progress -->
        <div>
          <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">Generation Steps</h3>
          <StepProgress :steps="STEPS" :current-step="currentStep" :sub-label="subLabel" />
        </div>

        <!-- Live Log -->
        <div>
          <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">Live Output</h3>
          <div class="h-72 overflow-y-auto bg-gray-950 rounded-xl border border-gray-800 p-3 space-y-1 font-mono text-xs" ref="logEl">
            <div v-if="logs.length === 0" class="flex items-center justify-center h-full text-gray-600">Waiting...</div>
            <div
              v-for="(log, i) in logs"
              :key="i"
              class="py-0.5"
              :class="{
                'text-brand-400': log.startsWith('✓') || log.startsWith('[TC'),
                'text-amber-300': log.startsWith('Fetching'),
                'text-gray-300': !log.startsWith('✓') && !log.startsWith('Fetching'),
              }"
            >
              <span class="text-gray-600 mr-2">{{ getTime() }}</span>{{ log }}
            </div>
            <div v-if="running" class="text-gray-600 animate-pulse">▋</div>
          </div>
        </div>
      </div>

      <!-- Status / Actions -->
      <div class="mt-6 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div
            class="w-2.5 h-2.5 rounded-full"
            :class="{
              'bg-brand-500 animate-pulse': running,
              'bg-emerald-500': done,
              'bg-red-500': failed,
            }"
          />
          <span class="text-sm text-gray-600 dark:text-gray-400">
            {{ running ? 'Generation in progress...' : done ? 'Completed successfully!' : failed ? 'Generation failed' : 'Starting...' }}
          </span>
        </div>

        <div class="flex gap-2">
          <button v-if="running" @click="cancel" class="btn-secondary btn-sm">
            Cancel
          </button>
          <button v-if="failed" @click="retry" class="btn-primary btn-sm">
            Retry
          </button>
          <button v-if="done" @click="goToReview" class="btn-primary btn-sm">
            Review Test Cases →
          </button>
        </div>
      </div>

      <!-- Timeout warning -->
      <Transition name="fade">
        <div v-if="showTimeout" class="mt-4 p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl">
          <p class="text-sm text-amber-700 dark:text-amber-400">
            ⚠️ Generation is taking longer than expected. You can wait or cancel and try again.
          </p>
        </div>
      </Transition>

      <!-- Partial success warning -->
      <Transition name="fade">
        <div v-if="done && partialSuccess" class="mt-4 p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl">
          <p class="text-sm text-amber-700 dark:text-amber-400">
            ⚠️ Selenium code generation was skipped for 1 test case due to complexity. You can regenerate it in the Review screen.
          </p>
        </div>
      </Transition>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import BaseCard from '@/components/ui/BaseCard.vue'
import StepProgress from '@/components/ui/StepProgress.vue'
import { api } from '@/mocks/api'
import { useTestCaseStore } from '@/stores/useTestCaseStore'
import { useToast } from 'vue-toastification'

const router = useRouter()
const store = useTestCaseStore()
const toast = useToast()

const STEPS = ['Parsing prompt', 'Fetching Confluence/Jira', 'Generating test cases', 'Generating Selenium code']

const logs = ref<string[]>([])
const currentStep = ref(0)
const subLabel = ref('')
const running = ref(false)
const done = ref(false)
const failed = ref(false)
const partialSuccess = ref(false)
const showTimeout = ref(false)
const logEl = ref<HTMLElement | null>(null)
let cancelled = false
let timeoutTimer: ReturnType<typeof setTimeout>

function getTime() {
  return new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

function addLog(msg: string) {
  logs.value.push(msg)
  nextTick(() => {
    if (logEl.value) logEl.value.scrollTop = logEl.value.scrollHeight
  })

  // Advance step based on log content
  if (msg.includes('Fetching')) currentStep.value = 1
  else if (msg.includes('Generating test')) currentStep.value = 2
  else if (msg.includes('Generating Selenium') || msg.includes('code')) currentStep.value = 3
  else if (msg.includes('✓')) { currentStep.value = 4 }
}

async function start() {
  if (cancelled) return
  cancelled = false
  running.value = true
  done.value = false
  failed.value = false
  logs.value = []
  currentStep.value = 0

  timeoutTimer = setTimeout(() => { showTimeout.value = true }, 12000)

  try {
    const input = JSON.parse(sessionStorage.getItem('promptInput') || '{}')
    const generated = await api.generateTestCases(input, addLog)
    store.seedFromGeneration(generated)
    clearTimeout(timeoutTimer)
    done.value = true
    running.value = false
    currentStep.value = 4
    toast.success(`${generated.length} test cases generated!`)
  } catch (e) {
    clearTimeout(timeoutTimer)
    if (cancelled) return
    failed.value = true
    running.value = false
    toast.error('Generation failed. Please try again.')
    logs.value.push('ERROR: ' + String(e))
  }
}

function cancel() {
  cancelled = true
  running.value = false
  clearTimeout(timeoutTimer)
  router.push('/prompt')
}

function retry() {
  showTimeout.value = false
  start()
}

function goToReview() {
  router.push('/review')
}

onMounted(start)
</script>
