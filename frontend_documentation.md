# Frontend Documentation — AI Test Automation Platform

Complete reference for every folder, file, and component in the Vue 3 / TypeScript / TailwindCSS frontend.

---

## Tech Stack

| Tool | Role |
|---|---|
| **Vue 3** (Composition API) | UI framework |
| **TypeScript** | Static typing |
| **TailwindCSS v3** | Utility-first CSS |
| **Vite** | Dev server & bundler |
| **Vue Router 4** | Client-side routing |
| **Pinia** | Global state management |
| **vue-toastification** | Toast notification system |
| **@vueuse/core** | Composable utilities (useStorage) |

---

## High-Level Architecture

```
src/
├── main.ts               ← Application bootstrap
├── App.vue               ← Root component (dark-mode persistence)
├── assets/               ← Global CSS + design tokens
├── types/                ← Shared TypeScript interfaces
├── router/               ← Vue Router route definitions
├── stores/               ← Pinia global state stores
├── mocks/                ← Simulated API layer (dev/demo)
├── layouts/              ← Page shell (sidebar + navbar)
├── components/           ← Reusable UI building blocks
│   ├── layout/           ← Structural layout components
│   └── ui/               ← Generic UI primitives
└── pages/                ← Full-page route components (8 pages)
```

### 8-Step Pipeline → Page Mapping

| Step | Pipeline Action | Page |
|---|---|---|
| 1 | Submit prompt | [PromptInputPage.vue](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue) |
| 2 | View AI processing | [ProcessingPage.vue](file:///d:/Testing%20automation%20frontend/src/pages/ProcessingPage.vue) |
| 3–4 | AI fetches context + generates | [ProcessingPage.vue](file:///d:/Testing%20automation%20frontend/src/pages/ProcessingPage.vue) (progress) |
| 5 | Review BDD + Selenium | [ReviewPage.vue](file:///d:/Testing%20automation%20frontend/src/pages/ReviewPage.vue) |
| 6 | Approve/reject + Zephyr push | [ApprovalPage.vue](file:///d:/Testing%20automation%20frontend/src/pages/ApprovalPage.vue) + [ZephyrPage.vue](file:///d:/Testing%20automation%20frontend/src/pages/ZephyrPage.vue) |
| 7 | Trigger Harness execution | [ExecutionPage.vue](file:///d:/Testing%20automation%20frontend/src/pages/ExecutionPage.vue) |
| 8 | View results + AI insights | [ResultsPage.vue](file:///d:/Testing%20automation%20frontend/src/pages/ResultsPage.vue) |

---

## Root-Level Config Files

### [package.json](file:///d:/Testing%20automation%20frontend/package.json)
Defines all npm dependencies and project scripts.

**Key dependencies:**
| Package | Purpose |
|---|---|
| [vue](file:///d:/Testing%20automation%20frontend/src/App.vue) | Core framework |
| `pinia` | State management |
| `vue-router` | Client routing |
| `vue-toastification` | Toast notifications |
| `@vueuse/core` | `useStorage`, dark-mode composable |

**Scripts:**
- `npm run dev` — start Vite dev server (port 5173, hot-reload)
- `npm run build` — compile TypeScript + bundle for production
- `npm run preview` — preview the production build locally

---

### [vite.config.ts](file:///d:/Testing%20automation%20frontend/vite.config.ts)
Configures the Vite bundler.

- **`@vitejs/plugin-vue`** — enables [.vue](file:///d:/Testing%20automation%20frontend/src/App.vue) Single File Component (SFC) processing
- **Path alias `@`** — resolves to `src/` so `@/components/...` works throughout the project instead of `../../components/...`

---

### [tsconfig.json](file:///d:/Testing%20automation%20frontend/tsconfig.json)
TypeScript compiler configuration.

Key settings:
- `"target": "ESNext"` — modern JavaScript output
- `"module": "ESNext"` — native ESM modules
- `"strict": true` — full strict mode (null checks, no implicit any)
- `"paths": { "@/*": ["./src/*"] }` — mirrors the Vite alias for IDE support
- `"types": ["vite/client"]` — adds `import.meta.env` type support

---

### [tailwind.config.js](file:///d:/Testing%20automation%20frontend/tailwind.config.js)
TailwindCSS configuration extended with project-specific design tokens.

**Custom colours (brand palette):**
- `brand` — primary blue shades (50–900)
- `surface` — card/panel background colours for dark/light mode
- [success](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#28-41), `warning`, `danger` — semantic status colours (used by badges)

**Custom animations:**
- `fade-in`, `slide-up`, `pulse-ring` — micro-animations used on loading states and processing steps

**Content paths:**
Tells Tailwind to scan [.vue](file:///d:/Testing%20automation%20frontend/src/App.vue) and [.ts](file:///d:/Testing%20automation%20frontend/src/main.ts) files for class names to include in the production CSS bundle.

---

## [src/main.ts](file:///d:/Testing%20automation%20frontend/src/main.ts) — Application Bootstrap

The entry point executed when the browser loads the app. Sets up the Vue application instance and mounts it to the `#app` div in [index.html](file:///d:/Testing%20automation%20frontend/index.html).

**What it does:**
1. Creates the Vue 3 app via `createApp(App)`
2. Creates and registers a Pinia store instance (`createPinia()`)
3. Registers Vue Router
4. Registers `vue-toastification` with global defaults:
   - Position: `bottom-right`
   - Timeout: 4 seconds
   - Hover-to-pause, draggable, progress bar visible
5. Calls `app.mount('#app')` — injects the component tree into the DOM

---

## [src/App.vue](file:///d:/Testing%20automation%20frontend/src/App.vue) — Root Component

The single root component rendered for every URL. Contains only two things:

**`<RouterView />`** — the Vue Router outlet. Every page component renders here based on the current URL.

**Dark-mode persistence (`onMounted`):**
Uses `@vueuse/core`'s `useStorage('testai-dark-mode', false)` to read the user's dark-mode preference from `localStorage`. On mount, if `darkMode.value` is true, it adds the `dark` class to `<html>` — which activates Tailwind's dark-mode variants across all components.

---

## [src/assets/main.css](file:///d:/Testing%20automation%20frontend/src/assets/main.css) — Global Stylesheet

The single CSS file imported in [main.ts](file:///d:/Testing%20automation%20frontend/src/main.ts). Contains:

**Tailwind directives:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**CSS custom properties (design tokens):**
Variables like `--color-primary`, `--color-surface`, `--radius-card` defined on `:root` and overridden in `[data-theme="dark"]`. These cascade through all components.

**Base layer resets:**
Smooth font rendering, box-sizing, and focus-visible ring styles.

**Component layer utilities:**
Reusable CSS classes compiled by Tailwind:
- `.card` — surface card with border, radius, and shadow
- `.btn-primary`, `.btn-ghost` — button variants
- `.badge-success`, `.badge-danger`, `.badge-warning`, `.badge-info` — status pill labels
- `.log-line-*` — coloured log line styles for the log viewer

---

## [src/types/index.ts](file:///d:/Testing%20automation%20frontend/src/types/index.ts) — Shared TypeScript Types

The single source of type truth for the entire frontend. Every component, store, and page imports interfaces from here. Ensures type consistency between mock data, store state, and component props.

### Union Types (string literals)
```ts
TestType    = 'UI' | 'API' | 'Regression'
TestStatus  = 'draft' | 'approved' | 'rejected' | 'pending'
SyncStatus  = 'synced' | 'not_synced' | 'failed' | 'syncing'
ExecutionStatus = 'running' | 'passed' | 'failed' | 'pending' | 'cancelled'
UserRole    = 'admin' | 'tester' | 'viewer'
```

### Interfaces

**[TestCase](file:///d:/Testing%20automation%20frontend/backend/app/models/testcase.py#22-66)** — Central data model:
| Field | Type | Source |
|---|---|---|
| [id](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue#202-217) | string | Server-assigned (TC-001) |
| [title](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#97-106) | string | AI-generated |
| `description` | string | AI-generated |
| `type` | TestType | User-selected |
| [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60) | TestStatus | Lifecycle state |
| `bddContent` | string | BDDAgent output |
| `seleniumCode` | string | SeleniumAgent output |
| `tags` | string[] | AI-assigned labels |
| `zephyrId?` | string | Set after Zephyr sync |
| `syncStatus` | SyncStatus | Zephyr sync state |
| `createdAt` / `updatedAt` | string | ISO timestamps |

**[PromptInput](file:///d:/Testing%20automation%20frontend/src/types/index.ts#25-33)** — form data submitted on `PromptInputPage`:
[text](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#64-79), `url?`, `file?`, `testType`, `generateBDD`, `generateSelenium`

**[ParsedInput](file:///d:/Testing%20automation%20frontend/src/types/index.ts#34-39)** — detected links returned from parse API:
`confluenceLinks[]`, `jiraTickets[]`, `promptText`

**[Execution](file:///d:/Testing%20automation%20frontend/src/types/index.ts#42-51)** — a Harness pipeline run:
[id](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue#202-217), `testCaseIds[]`, [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60), `startTime`, `endTime?`, [pipeline](file:///d:/Testing%20automation%20frontend/backend/app/integrations/harness_client.py#66-74), `logs[]`

**[LogEntry](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#31-36)** — single log line:
`timestamp`, `level` (`info | success | error | warn | action`), `message`

**[TestResult](file:///d:/Testing%20automation%20frontend/src/types/index.ts#60-70)** — per-test outcome in a run:
`testCaseId`, [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60), [duration](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#83-93), `logs[]`, `screenshots[]`, `artifacts[]`, `aiInsight?`

**[AIInsight](file:///d:/Testing%20automation%20frontend/src/types/index.ts#71-77)** — AI root cause analysis for a failure:
`rootCause`, `suggestedFix`, `impactedTests[]`, `confidence` (0–1)

**[ExecutionSummary](file:///d:/Testing%20automation%20frontend/src/types/index.ts#78-88)** — complete run report:
`totalTests`, `passed`, `failed`, `skipped`, `passRate`, [duration](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#83-93), `results[]`

**[DashboardStats](file:///d:/Testing%20automation%20frontend/src/types/index.ts#91-97)** — KPI card data:
`totalTestCases`, `passed`, `failed`, `recentExecutions`

**[ActivityItem](file:///d:/Testing%20automation%20frontend/src/types/index.ts#98-105)** — recent activity feed entry:
[id](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue#202-217), `type` (`generated | approved | executed | synced | failed`), [title](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#97-106), `timestamp`, [user](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#87-106)

**[ZephyrConfig](file:///d:/Testing%20automation%20frontend/src/types/index.ts#117-123)** — connection status:
`connected`, `projectKey`, `baseUrl`, `lastSync?`

**`ApiResponse<T>`** — generic response wrapper:
[data](file:///d:/Testing%20automation%20frontend/backend/alembic/env.py#39-48), `message`, [success](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#28-41)

---

## [src/router/index.ts](file:///d:/Testing%20automation%20frontend/src/router/index.ts) — Vue Router

Defines all 8 application routes using Vue Router 4 with hash-less HTML5 history mode (`createWebHistory()`).

### Route Hierarchy

All routes are **children** of the `/` root, which renders [AppLayout.vue](file:///d:/Testing%20automation%20frontend/src/layouts/AppLayout.vue) as their shell:

```
/          → AppLayout (shell)
├──  ""    → DashboardPage      (Dashboard)
├── prompt → PromptInputPage    (New Prompt)
├── processing → ProcessingPage (Generating...)
├── review → ReviewPage         (Review Test Cases)
├── approval → ApprovalPage     (Approval)
├── zephyr → ZephyrPage         (Zephyr Integration)
├── execution → ExecutionPage   (Test Execution)
└── results → ResultsPage       (Results & Insights)
```

**Lazy loading:** Every page component uses a dynamic import ([() => import('@/pages/...')](file:///d:/Testing%20automation%20frontend/src/types/index.ts#128-135)). This means each page is a separate code chunk — pages don't download until first visit, reducing initial load time.

**`meta.title`:** Each route carries a title string used by the `afterEach` navigation guard to update `document.title` to `"Page Title – TestAI"`.

---

## [src/mocks/api.ts](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts) — Simulated API Layer

The complete API simulation layer used while the real FastAPI backend is not yet connected. Components and stores call `api.*` methods, which return realistic data after simulated network delays.

### Mock Data Exports

**`mockUser`** — a pre-built admin user (`Alex Johnson`, `alex@testai.io`) used as the authenticated session.

**`mockTestCases: TestCase[]`** — 6 realistic test cases covering all states:

| ID | Title | Type | Status | Zephyr |
|---|---|---|---|---|
| TC-001 | User Login with Valid Credentials | UI | approved | ZTC-2341 |
| TC-002 | Product Search – Filter by Category | UI | approved | ZTC-2342 |
| TC-003 | Checkout Flow – Payment Processing | UI | pending | — |
| TC-004 | API – User Registration Endpoint | API | approved | ZTC-2343 |
| TC-005 | Password Reset Email Flow | UI | rejected | failed |
| TC-006 | Dashboard KPI Cards Load | Regression | pending | — |

Each `mockTestCase` contains realistic multi-line `bddContent` (Gherkin) and `seleniumCode` (Java).

**`mockExecution`** — a completed run of TC-001, TC-002, TC-004 with 10 timestamped log entries.

**`mockExecutionSummary`** — full results: 3 passed, 0 failed, 100% pass rate, 512s duration, per-test logs, screenshots, and artifact links.

**`mockDashboardStats`** — `{ totalTestCases: 6, passed: 3, failed: 1, recentExecutions: 4 }`

**`mockActivityFeed`** — 5 recent activity entries covering execution, sync, approval, and generation events.

**`mockZephyrConfig`** — connected to `ESHOP` project at `zephyr.atlassian.net`.

### API Function Object (`api`)

All functions return `Promise<T>` and simulate network latency via [delay(ms)](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#3-4):

| Method | Delay | What it does |
|---|---|---|
| [getDashboardStats()](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#350-354) | 800ms | Returns `mockDashboardStats` |
| [getActivityFeed()](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#355-359) | 600ms | Returns `mockActivityFeed` |
| [getTestCases()](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#360-364) | 900ms | Returns copy of `mockTestCases[]` |
| [getTestCase(id)](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#365-371) | 400ms | Finds and returns single test case or throws 404 |
| [updateTestCase(id, patch)](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#372-379) | 500ms | Mutates `mockTestCases` in-place, returns updated |
| [deleteTestCase(id)](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#380-385) | 400ms | Splices from `mockTestCases` array |
| [generateTestCases(input, onLog)](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#386-403) | ~12s total | Plays through 8 step messages (with delays), calls `onLog` for each, returns first 3 mock test cases |
| [pushToZephyr(ids, onProgress)](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#404-411) | 800ms/item | Calls `onProgress(id)` for each item to simulate progressive sync |
| [runExecution(ids, onLog)](file:///d:/Testing%20automation%20frontend/src/pages/ExecutionPage.vue#159-170) | 900ms/log | Plays through 12 execution log lines, calls `onLog` for each, returns `mockExecution` |
| [getExecutionResults(id)](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#435-439) | 700ms | Returns `mockExecutionSummary` |
| [getZephyrConfig()](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#440-444) | 500ms | Returns `mockZephyrConfig` |
| [getSyncedTestCases()](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#445-449) | 700ms | Filters mock test cases where `syncStatus === 'synced'` |

> **Note:** [generateTestCases](file:///d:/Testing%20automation%20frontend/src/mocks/api.ts#386-403) and [runExecution](file:///d:/Testing%20automation%20frontend/src/pages/ExecutionPage.vue#159-170) use a **streaming callback pattern** — they call `onLog` progressively rather than returning all at once. This is what powers the live log animation in `ProcessingPage` and `ExecutionPage`.

---

## `src/stores/` — Pinia State Management

### `useTestCaseStore.ts` — Test Case State

The most-used store, shared by `ReviewPage`, `ApprovalPage`, `ZephyrPage`, and `ExecutionPage`.

**State:**
| Field | Type | Purpose |
|---|---|---|
| `testCases` | `TestCase[]` | All test cases in memory, hydrated with `mockTestCases` immediately on store creation |
| `loading` | `boolean` | Shows skeleton loaders while fetching |
| `error` | `string \| null` | Displayed when API calls fail |
| `selectedIds` | `Set<string>` | IDs selected via checkboxes (for bulk operations) |

**Computed:**
| Getter | Returns |
|---|---|
| `approvedCases` | `testCases` filtered to `status === 'approved'` |
| `pendingCases` | `testCases` filtered to `status === 'pending'` |
| `rejectedCases` | `testCases` filtered to `status === 'rejected'` |

**Actions:**
| Method | Behaviour |
|---|---|
| `fetchAll()` | Calls `api.getTestCases()`, updates `testCases`, sets `loading` and `error` |
| `seedFromGeneration(generated)` | Adds newly generated test cases to the front of the list, skipping duplicates by ID |
| `updateStatus(id, status)` | Calls `api.updateTestCase()`, then mutates the matching item's `status` and `updatedAt` in-place (no re-fetch) |
| `updateContent(id, patch)` | Patches any fields (BDD, Selenium, description) via API and local state |
| `deleteTC(id)` | Deletes via API, removes from array, removes from `selectedIds` |
| `toggleSelect(id)` | Add or remove ID from `selectedIds` |
| `selectAll()` | Add every test case ID to `selectedIds` |
| `clearSelection()` | Empty `selectedIds` |

**Initial hydration:**
The store immediately sets `testCases.value = [...mockTestCases]` at module level, so pages render with data before any async fetch completes.

---

### `useExecutionStore.ts` — Execution State

Manages the lifecycle of a single Harness pipeline run. Used by `ExecutionPage` and `ResultsPage`.

**State:**
| Field | Type | Purpose |
|---|---|---|
| `currentExecution` | `Execution \| null` | Active/last executed run |
| `executionSummary` | `ExecutionSummary \| null` | Full results for the results page |
| `logs` | `LogEntry[]` | Live-streaming log entries |
| `status` | `ExecutionStatus` | Current run state (pending → running → passed/failed) |
| `loading` | `boolean` | Loading indicator |
| `error` | `string \| null` | Error message |

**Actions:**

**`runExecution(testCaseIds)`**
1. Sets `status = 'running'`, clears `logs`, sets `loading = true`
2. Calls `api.runExecution(ids, callback)` — the callback classifies incoming log messages by content:
   - Contains "PASSED" or "successfully" → `level: 'success'`
   - Contains "STARTED" or "Starting" → `level: 'action'`
   - Otherwise → `level: 'info'`
3. Pushes each classified `LogEntry` into `logs` array in real time
4. On success: sets `status = 'passed'`, stores `currentExecution`
5. On failure: sets `status = 'failed'`, sets `error`

**`fetchResults(executionId)`**
Calls `api.getExecutionResults()`, stores the full `ExecutionSummary` for the results page.

**`reset()`**
Clears all state back to initial values. Called before starting a new execution.

---

## `src/layouts/AppLayout.vue` — Page Shell

The outer wrapper component that wraps every page. Every route renders through this layout.

**Template structure:**
```
<div class="app-shell">
  <AppSidebar />          ← left navigation
  <div class="main-area">
    <AppNavbar />         ← top bar
    <main>
      <RouterView />      ← page content renders here
    </main>
  </div>
</div>
```

Every authenticated page automatically gets the sidebar and navbar without needing to include them individually.

---

## `src/components/layout/` — Layout Components

### `AppSidebar.vue`
The persistent left navigation panel.

**Structure:**
- Top: Platform logo and name ("TestAI Platform")
- Navigation links: 8 items, one per page, using `<RouterLink>` with `active-class` for active state highlighting
  - Dashboard, New Prompt, Review, Approval, Zephyr, Execution, Results, Settings (placeholder)
- Each link has an icon (SVG inline) and a label
- Bottom section: current user avatar, name, role badge, and a dark-mode toggle button

**Dark-mode toggle:**
Uses `useStorage('testai-dark-mode')` from `@vueuse/core`. On toggle, adds/removes `dark` class on `document.documentElement`. Setting persists across page refreshes via `localStorage`.

**Active state:**
`RouterLink` automatically adds the `router-link-active` class. The sidebar styles this with a highlighted background and coloured left border.

**Responsive:**
On mobile screens, the sidebar collapses to icon-only. The labels are hidden and the sidebar narrows to 64px.

---

### `AppNavbar.vue`
The top navigation bar displayed above page content.

**Structure:**
- Left: Page title (read from `useRoute().meta.title`) and breadcrumb
- Centre: Global search bar (placeholder, not yet wired)
- Right: Quick-action button ("+ New Prompt" → routes to `/prompt`), notification bell (placeholder), and user avatar dropdown

**User dropdown:**
Shows `mockUser.name` and `mockUser.email`. Includes "View Profile" and "Sign Out" options (sign-out clears localStorage and reloads).

---

## `src/components/ui/` — Reusable UI Primitives

### `BaseBadge.vue`
A small coloured pill label for status, type, and sync state display.

**Props:**
| Prop | Type | Values |
|---|---|---|
| `variant` | string | `success`, `warning`, `danger`, `info`, `default` |
| `size` | string | `sm`, `md` (default) |

**Usage:** Status column in tables, type labels on cards.
Each variant maps to a Tailwind colour combination (e.g. `success` → green background, green text).

---

### `BaseCard.vue`
A white/dark surface container with a shadow and border radius. The visual building block for all content sections.

**Props:**
| Prop | Type | Default |
|---|---|---|
| `padding` | string | `'p-6'` (Tailwind class) |
| `hoverable` | boolean | `false` |

**Slot:** Default slot accepts any content. When `hoverable` is true, adds a lift effect on hover.

---

### `BaseModal.vue`
A full-screen overlay modal dialog.

**Props:** `isOpen: boolean`, `title: string`, `size: 'sm' | 'md' | 'lg'`

**Emits:** `close` — emitted when the backdrop or ✕ button is clicked.

**Behaviour:**
- Overlay darkens the background with a semi-transparent colour
- Clicking outside the modal panel emits `close`
- ESC key emits `close` (keyboard accessible)
- Uses Vue's `<Transition>` for fade+scale animation on open/close
- Scrollable body slot for long content

---

### `LogViewer.vue`
Displays live streaming log lines for `ProcessingPage` and `ExecutionPage`.

**Props:** `logs: LogEntry[]`, `autoScroll: boolean` (default `true`)

**Template:**
A dark-themed terminal-style panel. Each `LogEntry` renders as a coloured line:

| Level | Colour | Usage |
|---|---|---|
| `info` | Grey | Standard informational messages |
| `success` | Green | Step completed, test passed |
| `error` | Red | Failure or exception |
| `warn` | Yellow | Non-fatal warnings |
| `action` | Blue | Pipeline stage transitions (STARTED, RUNNING) |

**Auto-scroll:**
When `autoScroll` is true, the component watches the `logs` array and calls `scrollTop = scrollHeight` after each new entry, keeping the latest log visible.

**Empty state:** Shows "Waiting for logs..." with an animated pulsing dot.

---

### `SkeletonLoader.vue`
A shimmering placeholder shown while data is loading.

**Props:** `count: number` (number of skeleton rows), `type: 'card' | 'table-row' | 'text'`

Each skeleton row has a CSS keyframe animation (`shimmer`) that sweeps a lighter gradient left-to-right to convey loading. Used in all pages while `store.loading === true`.

---

### `StepProgress.vue`
The 4-step horizontal progress indicator shown on `ProcessingPage`.

**Props:** `currentStep: number` (1–4), `steps: string[]` (step labels)

**Template:** A row of circles connected by lines. Completed steps are filled (primary colour), the current step pulses, and future steps are grey. Step labels appear below each circle.

**Usage steps in context:**
1. Parsing Prompt
2. Fetching Context (Confluence/Jira)
3. AI Generating Test Cases
4. Generating Selenium Code

---

## `src/pages/` — Page Components

All 8 pages use the Composition API (`<script setup lang="ts">`). They receive no props — they read global state from Pinia stores and the route.

---

### `DashboardPage.vue` — `/`

The landing page of the platform.

**Template sections:**
1. **Welcome header** — "Good morning/afternoon, [name]" with current date
2. **KPI cards (4)** — Total Test Cases, Passed, Failed, Recent Executions. Each card shows a count, an icon, and a percentage change indicator
3. **Quick actions** — two large CTA cards: "Generate Test Cases" (→ `/prompt`) and "View Executions" (→ `/execution`)
4. **Activity feed** — recent events (executions, approvals, syncs, generations) in a timeline with type-coloured icons

**Data:**
- `stats` fetched from `api.getDashboardStats()` on `onMounted`
- `activity` fetched from `api.getActivityFeed()` on `onMounted`
- Both show `SkeletonLoader` while loading

**Onboarding state:**
If no test cases exist yet, a hero banner is shown with a "Start by creating your first prompt" CTA.

---

### `PromptInputPage.vue` — `/prompt`

**Step 1** of the pipeline. Users submit their requirements here.

**Template sections:**
1. **Text area** — multi-line input for free-text requirements (max 10,000 chars with live counter)
2. **URL field** — paste a Confluence page URL
3. **File upload** — drag-and-drop zone for PDF/DOCX/TXT files. Shows file name and size after selection
4. **Options panel** — dropdown for Test Type (UI / API / Regression), toggles for "Generate BDD" and "Generate Selenium Code"
5. **Live parsing preview** — as the user types, detected Confluence links and Jira tickets appear as chips in real time
6. **Submit button** — "Generate Test Cases" triggers the process

**State:**
- `promptText`, `confluenceUrl`, `uploadedFile`, `testType`, `generateBDD`, `generateSelenium`
- `isGenerating: boolean` — disables the form and shows a spinner while processing

**Validation:**
- Submit disabled if `promptText` is empty (after trim)
- File size warning if > 10MB
- URL format validated with a regex check

**Navigation:**
On successful submit, stores the prompt options in the Pinia test case store and navigates to `/processing`.

---

### `ProcessingPage.vue` — `/processing`

**Steps 2–4** visualised. Shows the AI generation pipeline in real time.

**Template sections:**
1. **`StepProgress`** component — 4-step progress bar updated as each stage completes
2. **`LogViewer`** — live log stream from `api.generateTestCases(input, onLog)`. Each message from the mock API updates the log in real time
3. **Estimated time indicator** — shows remaining time estimate based on current step
4. **Cancel button** — aborts the process (resets state and navigates back to `/prompt`)

**Lifecycle:**
On `onMounted`, immediately calls `api.generateTestCases()` with the stored prompt options. As log messages stream in via the callback, the step index advances at key message keywords ("Fetching", "Generating", "Selenium", "successfully").

On completion:
- Calls `store.seedFromGeneration(results)` to add generated test cases to the store
- Navigates automatically to `/review`

**Error state:**
If generation fails, shows a red error banner with a "Try again" button.

---

### `ReviewPage.vue` — `/review`

**Step 5** — review individual test cases before approval.

**Template sections:**
1. **Test case selector** — scrollable left panel listing all test cases. Clicking one loads it in the detail panel. Active item highlighted
2. **Split-pane detail view:**
   - Left pane: BDD Gherkin content in a dark code editor (syntax-highlighted `<pre>`)
   - Right pane: Selenium Java code in a dark code editor
3. **Metadata panel** — title, description, type badge, tags, created/updated timestamps
4. **Inline edit** — clicking the pencil icon on either pane makes it a `<textarea>` for direct editing. Changes saved via `store.updateContent(id, patch)` on blur
5. **Quick approve/reject buttons** — "Approve" / "Reject" per test case, calling `store.updateStatus(id, status)`

**State:**
`selectedTestCaseId` — the currently visible test case. Defaults to the first in the list.

**Empty state:**
If no test cases exist, shows "No test cases generated yet" with a link to the prompt page.

---

### `ApprovalPage.vue` — `/approval`

**Step 6a** — bulk review and approval table.

**Template sections:**
1. **Filter bar** — filter by status (All / Pending / Approved / Rejected), test type, and a search box
2. **Bulk action bar** — appears when 1+ rows are checked: "Approve All Selected", "Reject All Selected", "Delete Selected"
3. **Test case table** — columns: checkbox, title, type badge, status badge, tags, created date, actions

**Table per-row actions:**
- View (→ `ReviewPage.vue` for that test case)
- Approve (immediate)
- Reject (opens a modal for rejection reason)
- Delete (with confirmation)

**Bulk operations:**
- Select all with header checkbox
- `selectAll()` / `clearSelection()` from the store
- Batch status update via `Promise.all(selectedIds.map(id => store.updateStatus(id, ...)))`

**Sorting:**
Column headers on title, type, status, and date are clickable to toggle ascending/descending sort.

---

### `ZephyrPage.vue` — `/zephyr`

**Step 6b** — push approved test cases to Zephyr Scale.

**Template sections:**
1. **Connection status card** — shows green "Connected" or red "Disconnected" badge, project key, base URL, and last sync timestamp. "Test Connection" button re-fetches `api.getZephyrConfig()`
2. **Sync queue table** — lists all approved test cases showing title, type, sync status badge, Zephyr ID (if synced)
3. **Push controls** — "Push All Approved" button (bulk) and per-row "Sync" button
4. **Sync progress drawer** — slides in during a push showing per-item progress: queued → syncing → synced / failed

**Push logic:**
Calls `api.pushToZephyr(ids, onProgress)`. For each completed sync, `onProgress(id)` is called, which updates that test case's status badge from "Not Synced" to "Synced" in real time, and the `zephyrId` field is populated.

**Error handling:**
Failed syncs show a red status badge, the error reason, and a "Retry" button for that specific item.

---

### `ExecutionPage.vue` — `/execution`

**Step 7** — trigger and monitor a Harness pipeline run.

**Template sections:**
1. **Test case selector** — list of approved test cases with checkboxes. Multi-select enabled. Filter by type
2. **Pipeline configuration panel:**
   - Pipeline ID dropdown (pre-filled with configured Harness pipeline)
   - Environment selector (staging / qa / production)
   - "Run Selected Tests" CTA button
3. **Live execution panel** (appears after triggering):
   - Status banner (running / passed / failed) with animated spinner while running
   - `LogViewer` component showing live log stream
   - Duration counter
4. **Cancel button** — available only while status is "running"

**Execution flow:**
1. User selects test cases and clicks Run
2. `executionStore.runExecution(selectedIds)` is called
3. Logs populate in real time via the callback
4. On completion, status banner updates and a "View Results" button appears

**State persistence:**
`executionStore.currentExecution` persists the result so `ResultsPage` can read it immediately without a re-fetch.

---

### `ResultsPage.vue` — `/results`

**Step 8** — full results view with AI insights.

**Template sections:**
1. **Summary KPI row** — Total, Passed, Failed, Skipped counts + Pass Rate percentage + Duration
2. **Pass rate bar chart** — a horizontal bar with green (passed) and red (failed) segments
3. **Results table** — per test case rows showing: title, status badge, duration, log count, screenshot count
4. **Expandable row detail** — clicking a row expands it to show:
   - Step-by-step logs for that test case
   - Screenshot thumbnails (clickable to enlarge in a `BaseModal`)
   - Artifact download links (HTML/JSON reports)
   - **AI Insight panel** (shown only for failed tests):
     - "Root Cause" — AI plain-language explanation
     - "Suggested Fix" — recommended code change
     - "Impacted Tests" — other tests likely affected
     - Confidence badge (e.g. "92% confident")
5. **Export button** — Downloads results as a JSON report

**Data:**
`executionStore.executionSummary` is read on mount. If null (user navigated directly), `executionStore.fetchResults(executionId)` is called with the ID from the URL query param.

**Empty/error state:**
If no execution has run yet, shows "No results available" with a link to `/execution`.

---

## Data Flow Diagram

```
User types prompt
    │
    ▼
PromptInputPage.vue
    │  stores options in component state
    │  navigates to /processing
    ▼
ProcessingPage.vue
    │  api.generateTestCases(input, onLog)
    │  ← log callbacks update LogViewer in real time
    │  on complete: store.seedFromGeneration(results)
    │  navigates to /review
    ▼
useTestCaseStore (Pinia)  ←──────────────────────┐
    │  testCases[]                                │
    │                                             │
    ├─▶ ReviewPage.vue      (read + edit)         │
    ├─▶ ApprovalPage.vue    (read + updateStatus) │
    ├─▶ ZephyrPage.vue      (read + sync)         │
    └─▶ ExecutionPage.vue   (read selectedIds)    │
              │                                   │
              │ runExecution(selectedIds)          │
              ▼                                   │
    useExecutionStore (Pinia)                     │
              │  logs[] updated live              │
              ▼                                   │
    ResultsPage.vue                               │
         reads executionSummary                   │
         shows AI insights per failed test        │
         "Retry" → back to PromptInputPage ───────┘
```

---

## Component Dependency Map

```
AppLayout.vue
├── AppSidebar.vue   (uses useStorage, RouterLink)
├── AppNavbar.vue    (uses useRoute)
└── <RouterView>
    ├── DashboardPage.vue       (api calls → displays stats + activity)
    ├── PromptInputPage.vue     (form → navigates to ProcessingPage)
    ├── ProcessingPage.vue      (api.generateTestCases → StepProgress + LogViewer)
    ├── ReviewPage.vue          (useTestCaseStore → split-pane editor)
    ├── ApprovalPage.vue        (useTestCaseStore → table + bulk actions + BaseModal)
    ├── ZephyrPage.vue          (useTestCaseStore + api.pushToZephyr → sync table)
    ├── ExecutionPage.vue       (useTestCaseStore + useExecutionStore → LogViewer)
    └── ResultsPage.vue         (useExecutionStore → results table + AI insights + BaseModal)

Shared UI Components (used across pages):
├── BaseBadge.vue    → used by ALL pages for status/type display
├── BaseCard.vue     → used by ALL pages as content container
├── BaseModal.vue    → ApprovalPage (rejection), ResultsPage (screenshots)
├── LogViewer.vue    → ProcessingPage, ExecutionPage
├── SkeletonLoader.vue → DashboardPage, ReviewPage, ApprovalPage
└── StepProgress.vue → ProcessingPage
```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| **Mock API layer (`mocks/api.ts`)** | Decouples UI development from backend readiness. Swap `import { api } from '@/mocks/api'` to `import { api } from '@/services/api'` when connecting the real backend |
| **Streaming callback pattern** | `generateTestCases(input, onLog)` calls a callback for each log instead of resolving once at the end. Enables the live log animation |
| **Pinia stores hydrated at module level** | `testCases.value = [...mockTestCases]` runs immediately on first import, so pages never flash empty on first render |
| **`useStorage` from @vueuse/core** | Persists dark-mode preference to `localStorage` with one line, no custom serialisation needed |
| **Lazy-loaded routes** | All 8 pages are separate code chunks. First load only downloads Layout + Dashboard; other pages download on first visit |
| **`Set<string>` for selectedIds** | O(1) lookup for add/remove/has — important for large test case lists with frequent checkbox toggling |
