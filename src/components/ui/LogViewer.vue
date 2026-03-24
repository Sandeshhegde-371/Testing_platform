<template>
  <div class="relative overflow-hidden rounded-xl bg-gray-950 border border-gray-800">
    <!-- Header bar -->
    <div class="flex items-center justify-between px-4 py-2 bg-gray-900 border-b border-gray-800">
      <span class="text-xs font-mono text-gray-400">{{ title || 'Live Logs' }}</span>
      <div class="flex items-center gap-3">
        <label class="flex items-center gap-1.5 text-xs text-gray-500 cursor-pointer select-none">
          <input type="checkbox" v-model="autoScroll" class="rounded" />
          Auto-scroll
        </label>
        <button @click="clear" class="text-xs text-gray-500 hover:text-gray-300 transition-colors">Clear</button>
      </div>
    </div>

    <!-- Log lines -->
    <div
      ref="logContainer"
      class="h-64 overflow-y-auto p-3 space-y-0.5 font-mono text-xs"
    >
      <div
        v-if="logs.length === 0"
        class="flex items-center justify-center h-full text-gray-600"
      >
        <div class="text-center">
          <div class="text-2xl mb-2">📋</div>
          <p>Waiting for logs...</p>
        </div>
      </div>

      <div
        v-for="(log, i) in logs"
        :key="i"
        class="log-line flex gap-3 items-start"
        :class="`log-line.${log.level || 'info'}`"
      >
        <span class="text-gray-600 shrink-0">{{ log.timestamp }}</span>
        <span
          :class="{
            'text-gray-300': log.level === 'info',
            'text-emerald-400': log.level === 'success',
            'text-red-400': log.level === 'error',
            'text-amber-400': log.level === 'warn',
            'text-brand-400': log.level === 'action',
          }"
        >{{ log.message }}</span>
      </div>

      <!-- Streaming indicator -->
      <div v-if="streaming" class="flex items-center gap-2 text-gray-500 pl-16">
        <span class="w-1.5 h-1.5 bg-brand-500 rounded-full animate-pulse" />
        <span>Streaming...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import type { LogEntry } from '@/types'

const props = defineProps<{
  logs: LogEntry[]
  streaming?: boolean
  title?: string
}>()

const logContainer = ref<HTMLElement | null>(null)
const autoScroll = ref(true)
const localLogs = ref<LogEntry[]>([...props.logs])

function clear() {
  localLogs.value = []
}

watch(() => props.logs, async (newLogs) => {
  localLogs.value = [...newLogs]
  if (autoScroll.value) {
    await nextTick()
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  }
}, { deep: true })
</script>
