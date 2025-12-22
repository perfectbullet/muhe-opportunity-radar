import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/analysis',
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: () => import('@/views/SingleAnalysis.vue'),
      meta: { title: '单一视角分析' },
    },
    {
      path: '/comparison',
      name: 'comparison',
      component: () => import('@/views/MultiComparison.vue'),
      meta: { title: '多视角对比' },
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/HistoryRecords.vue'),
      meta: { title: '历史记录' },
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('@/views/Statistics.vue'),
      meta: { title: '统计信息' },
    },
  ],
})

export default router
