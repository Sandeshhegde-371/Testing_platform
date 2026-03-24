import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/AppLayout.vue'),
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('@/pages/DashboardPage.vue'),
        meta: { title: 'Dashboard' },
      },
      {
        path: 'prompt',
        name: 'prompt',
        component: () => import('@/pages/PromptInputPage.vue'),
        meta: { title: 'New Prompt' },
      },
      {
        path: 'processing',
        name: 'processing',
        component: () => import('@/pages/ProcessingPage.vue'),
        meta: { title: 'Generating...' },
      },
      {
        path: 'review',
        name: 'review',
        component: () => import('@/pages/ReviewPage.vue'),
        meta: { title: 'Review Test Cases' },
      },
      {
        path: 'approval',
        name: 'approval',
        component: () => import('@/pages/ApprovalPage.vue'),
        meta: { title: 'Approval' },
      },
      {
        path: 'zephyr',
        name: 'zephyr',
        component: () => import('@/pages/ZephyrPage.vue'),
        meta: { title: 'Zephyr Integration' },
      },
      {
        path: 'execution',
        name: 'execution',
        component: () => import('@/pages/ExecutionPage.vue'),
        meta: { title: 'Test Execution' },
      },
      {
        path: 'results',
        name: 'results',
        component: () => import('@/pages/ResultsPage.vue'),
        meta: { title: 'Results & Insights' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.afterEach((to) => {
  document.title = to.meta?.title ? `${to.meta.title} – TestAI` : 'TestAI Platform'
})

export default router
