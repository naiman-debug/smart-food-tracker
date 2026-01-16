/**
 * 路由配置
 */
import { createRouter, createWebHistory, type Router } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { checkGoalForRoute } from '@/composables/useGoal'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresGoal: true }
  },
  {
    path: '/record',
    name: 'Record',
    component: () => import('@/views/Record.vue'),
    meta: { requiresGoal: true }
  },
  {
    path: '/progress',
    name: 'Progress',
    component: () => import('@/views/Progress.vue'),
    meta: { requiresGoal: true }
  },
  {
    path: '/goal',
    name: 'Goal',
    component: () => import('@/views/Goal.vue'),
    meta: { requiresGoal: false }  // Goal page is always accessible
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

/**
 * Route guard - Check if goal is set before accessing protected routes
 */
router.beforeEach(async (to, from, next) => {
  // Check if route requires goal
  const requiresGoal = to.meta?.requiresGoal !== false

  if (requiresGoal) {
    // Check if goal is set
    const hasGoalSet = await checkGoalForRoute()

    if (!hasGoalSet) {
      // No goal set, redirect to goal page
      // Store the intended destination for redirect after goal is set
      const returnUrl = to.fullPath !== '/' ? to.fullPath : '/'
      if (returnUrl !== '/') {
        sessionStorage.setItem('smartfood_return_url', returnUrl)
      }
      next({ name: 'Goal', query: { redirect: returnUrl === '/' ? undefined : returnUrl } })
      return
    }
  }

  next()
})

export default router
