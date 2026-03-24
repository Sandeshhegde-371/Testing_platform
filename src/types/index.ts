// ─── Test Case Types ────────────────────────────────────────────────────────

export type TestType = 'UI' | 'API' | 'Regression'
export type TestStatus = 'draft' | 'approved' | 'rejected' | 'pending'
export type SyncStatus = 'synced' | 'not_synced' | 'failed' | 'syncing'
export type ExecutionStatus = 'running' | 'passed' | 'failed' | 'pending' | 'cancelled'

export interface TestCase {
  id: string
  title: string
  description: string
  type: TestType
  status: TestStatus
  bddContent: string
  seleniumCode: string
  tags: string[]
  createdAt: string
  updatedAt: string
  zephyrId?: string
  syncStatus: SyncStatus
}

// ─── Prompt Types ────────────────────────────────────────────────────────────

export interface PromptInput {
  text: string
  url?: string
  file?: File
  testType: TestType
  generateBDD: boolean
  generateSelenium: boolean
}

export interface ParsedInput {
  confluenceLinks: string[]
  jiraTickets: string[]
  promptText: string
}

// ─── Execution Types ─────────────────────────────────────────────────────────

export interface Execution {
  id: string
  testCaseIds: string[]
  status: ExecutionStatus
  startTime: string
  endTime?: string
  pipeline: string
  logs: LogEntry[]
}

export interface LogEntry {
  timestamp: string
  level: 'info' | 'success' | 'error' | 'warn' | 'action'
  message: string
}

// ─── Result Types ─────────────────────────────────────────────────────────────

export interface TestResult {
  testCaseId: string
  testCaseTitle: string
  status: ExecutionStatus
  duration: number
  logs: LogEntry[]
  screenshots: string[]
  artifacts: string[]
  aiInsight?: AIInsight
}

export interface AIInsight {
  rootCause: string
  suggestedFix: string
  impactedTests: string[]
  confidence: number
}

export interface ExecutionSummary {
  executionId: string
  totalTests: number
  passed: number
  failed: number
  skipped: number
  duration: number
  passRate: number
  results: TestResult[]
}

// ─── Dashboard Types ─────────────────────────────────────────────────────────

export interface DashboardStats {
  totalTestCases: number
  passed: number
  failed: number
  recentExecutions: number
}

export interface ActivityItem {
  id: string
  type: 'generated' | 'approved' | 'executed' | 'synced' | 'failed'
  title: string
  timestamp: string
  user: string
}

// ─── Zephyr Types ─────────────────────────────────────────────────────────────

export interface ZephyrTestCase {
  testCaseId: string
  title: string
  zephyrId: string
  syncStatus: SyncStatus
  syncedAt?: string
  projectKey: string
}

export interface ZephyrConfig {
  connected: boolean
  projectKey: string
  baseUrl: string
  lastSync?: string
}

// ─── User / Auth Types ────────────────────────────────────────────────────────

export type UserRole = 'admin' | 'tester' | 'viewer'

export interface User {
  id: string
  name: string
  email: string
  role: UserRole
  avatar?: string
}

// ─── API Response Wrapper ─────────────────────────────────────────────────────

export interface ApiResponse<T> {
  data: T
  message: string
  success: boolean
}
