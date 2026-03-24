<template>
  <div class="max-w-3xl mx-auto animate-fade-in">
    <div class="page-header">
      <h1 class="page-title">Generate Test Cases</h1>
      <p class="page-subtitle">Provide context via a prompt, URL, or file — TestAI will do the rest</p>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-5">

      <!-- Prompt textarea -->
      <BaseCard title="Describe your feature or requirement" subtitle="Be as specific as possible for better results">
        <div class="space-y-3">
          <textarea
            id="prompt-input"
            v-model="form.text"
            rows="6"
            class="form-input resize-none"
            placeholder="e.g. Write test cases for the checkout flow of our e-commerce app. Users should be able to add items, apply discount codes, and complete payment via credit card or PayPal..."
            :class="{ 'ring-2 ring-red-500 border-red-500': errors.text }"
          />
          <div class="flex items-center justify-between text-xs text-gray-500">
            <span :class="form.text.length > 2000 ? 'text-amber-600 font-medium' : ''">
              {{ form.text.length }} / 5000 chars
              <span v-if="form.text.length > 2000" class="ml-1">⚠️ Large input may slow generation</span>
            </span>
            <span v-if="errors.text" class="text-red-500">{{ errors.text }}</span>
          </div>
        </div>
      </BaseCard>

      <!-- URL & File row -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

        <!-- URL input -->
        <BaseCard title="Confluence / Jira URL" subtitle="Optional – fetched automatically">
          <div class="space-y-2">
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                </svg>
              </span>
              <input
                v-model="form.url"
                type="url"
                class="form-input pl-9"
                placeholder="https://confluence.example.com/..."
                :class="{ 'ring-2 ring-red-500 border-red-500': errors.url }"
              />
            </div>
            <p v-if="errors.url" class="text-xs text-red-500">{{ errors.url }}</p>

            <!-- Parsed URL preview -->
            <Transition name="fade">
              <div v-if="parsedInput.confluenceLinks.length || parsedInput.jiraTickets.length" class="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl space-y-1 text-xs">
                <div v-if="parsedInput.confluenceLinks.length">
                  <span class="font-medium text-blue-600 dark:text-blue-400">Confluence:</span>
                  <span class="ml-1 text-gray-600 dark:text-gray-400">{{ parsedInput.confluenceLinks[0] }}</span>
                </div>
                <div v-if="parsedInput.jiraTickets.length">
                  <span class="font-medium text-purple-600 dark:text-purple-400">Jira:</span>
                  <span class="ml-1 text-gray-600 dark:text-gray-400">{{ parsedInput.jiraTickets.join(', ') }}</span>
                </div>
              </div>
            </Transition>
          </div>
        </BaseCard>

        <!-- File upload -->
        <BaseCard title="Upload Document" subtitle="PDF or DOCX supported">
          <div
            class="border-2 border-dashed rounded-xl p-5 text-center transition-all duration-200 cursor-pointer"
            :class="dragOver ? 'border-brand-400 bg-brand-50 dark:bg-brand-950/30' : 'border-gray-200 dark:border-gray-700 hover:border-brand-300'"
            @dragover.prevent="dragOver = true"
            @dragleave="dragOver = false"
            @drop.prevent="handleDrop"
            @click="fileInput?.click()"
          >
            <input ref="fileInput" type="file" class="hidden" accept=".pdf,.docx" @change="handleFile" />
            <div v-if="form.file">
              <div class="text-3xl mb-2">📄</div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ form.file.name }}</p>
              <p class="text-xs text-gray-500">{{ (form.file.size / 1024).toFixed(0) }} KB</p>
              <button type="button" @click.stop="form.file = undefined" class="text-xs text-red-500 mt-1 hover:underline">Remove</button>
            </div>
            <div v-else>
              <div class="text-3xl mb-2">📁</div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Drag & drop or click to upload</p>
              <p class="text-xs text-gray-400 mt-1">PDF, DOCX up to 10MB</p>
            </div>
          </div>
          <p v-if="errors.file" class="text-xs text-red-500 mt-1">{{ errors.file }}</p>
        </BaseCard>
      </div>

      <!-- Options row -->
      <BaseCard title="Generation Options">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Test type -->
          <div>
            <label class="form-label">Test Type</label>
            <select v-model="form.testType" class="form-input">
              <option value="UI">UI Tests</option>
              <option value="API">API Tests</option>
              <option value="Regression">Regression Tests</option>
            </select>
          </div>

          <!-- Toggles -->
          <div class="md:col-span-2 flex flex-col gap-3 pt-1">
            <label class="flex items-center gap-3 cursor-pointer group">
              <div
                @click="form.generateBDD = !form.generateBDD"
                class="w-10 h-5.5 rounded-full transition-colors duration-200 flex items-center px-0.5 cursor-pointer"
                :class="form.generateBDD ? 'bg-brand-600' : 'bg-gray-200 dark:bg-gray-700'"
                style="height:22px;width:40px;"
              >
                <div
                  class="w-4 h-4 bg-white rounded-full shadow transition-transform duration-200"
                  :class="form.generateBDD ? 'translate-x-4' : 'translate-x-0'"
                />
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Generate BDD Scenarios</p>
                <p class="text-xs text-gray-500">Gherkin feature files</p>
              </div>
            </label>

            <label class="flex items-center gap-3 cursor-pointer group">
              <div
                @click="form.generateSelenium = !form.generateSelenium"
                class="w-10 rounded-full transition-colors duration-200 flex items-center px-0.5 cursor-pointer"
                :class="form.generateSelenium ? 'bg-brand-600' : 'bg-gray-200 dark:bg-gray-700'"
                style="height:22px;width:40px;"
              >
                <div
                  class="w-4 h-4 bg-white rounded-full shadow transition-transform duration-200"
                  :class="form.generateSelenium ? 'translate-x-4' : 'translate-x-0'"
                />
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Generate Selenium Code</p>
                <p class="text-xs text-gray-500">Java TestNG automation scripts</p>
              </div>
            </label>
          </div>
        </div>
      </BaseCard>

      <!-- Submit -->
      <div class="flex justify-end gap-3">
        <button type="button" @click="resetForm" class="btn-secondary">Reset</button>
        <button
          type="submit"
          class="btn-primary"
          :disabled="isSubmitting"
        >
          <svg v-if="isSubmitting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          {{ isSubmitting ? 'Validating...' : 'Generate Test Cases' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import BaseCard from '@/components/ui/BaseCard.vue'
import type { PromptInput, TestType } from '@/types'

const router = useRouter()

const form = ref<PromptInput>({
  text: '',
  url: '',
  testType: 'UI' as TestType,
  generateBDD: true,
  generateSelenium: true,
})

const errors = ref<Record<string, string>>({})
const isSubmitting = ref(false)
const dragOver = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const parsedInput = computed(() => {
  const url = form.value.url || ''
  return {
    confluenceLinks: url.includes('confluence') ? [url] : [],
    jiraTickets: url.match(/[A-Z]+-\d+/g) || [],
    promptText: form.value.text,
  }
})

function validate() {
  errors.value = {}
  if (!form.value.text.trim() && !form.value.url && !form.value.file) {
    errors.value.text = 'Please provide a prompt, URL, or file'
  }
  if (form.value.url) {
    try { new URL(form.value.url) } catch {
      errors.value.url = 'Invalid URL format'
    }
  }
  if (form.value.text.length > 5000) {
    errors.value.text = 'Prompt exceeds 5000 character limit'
  }
  return Object.keys(errors.value).length === 0
}

function handleFile(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    if (file.size > 10 * 1024 * 1024) {
      errors.value.file = 'File exceeds 10MB limit'
      return
    }
    form.value.file = file
    delete errors.value.file
  }
}

function handleDrop(e: DragEvent) {
  dragOver.value = false
  const file = e.dataTransfer?.files[0]
  if (file) {
    if (!['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(file.type)) {
      errors.value.file = 'Only PDF and DOCX files are supported'
      return
    }
    form.value.file = file
  }
}

async function handleSubmit() {
  if (!validate()) return
  isSubmitting.value = true
  // Store form in session for processing page
  sessionStorage.setItem('promptInput', JSON.stringify({
    text: form.value.text,
    url: form.value.url,
    testType: form.value.testType,
    generateBDD: form.value.generateBDD,
    generateSelenium: form.value.generateSelenium,
  }))
  await new Promise(r => setTimeout(r, 500))
  isSubmitting.value = false
  router.push('/processing')
}

function resetForm() {
  form.value = { text: '', url: '', testType: 'UI', generateBDD: true, generateSelenium: true }
  errors.value = {}
}
</script>
