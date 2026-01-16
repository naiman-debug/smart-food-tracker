/**
 * 目标状态管理 Composable
 * 用于检查和管理用户的目标设置状态
 */
import { ref } from 'vue'
import { api, type GoalResponse, getUserErrorMessage } from '@/api'

// localStorage key for goal status
const GOAL_SET_KEY = 'smartfood_goal_set'
const GOAL_DATA_KEY = 'smartfood_goal_data'

// Global goal state
const hasGoal = ref<boolean | null>(null)  // null = not checked yet
const currentGoal = ref<GoalResponse | null>(null)

// Error state for user-facing messages
const goalError = ref<string | null>(null)
const isLoadingGoal = ref<boolean>(false)

/**
 * Check if goal is set (from localStorage)
 */
function isGoalSetInStorage(): boolean {
  try {
    return localStorage.getItem(GOAL_SET_KEY) === 'true'
  } catch {
    return false
  }
}

/**
 * Set goal status in localStorage
 */
function setGoalStatusInStorage(isSet: boolean) {
  try {
    localStorage.setItem(GOAL_SET_KEY, String(isSet))
  } catch (e) {
    console.warn('Failed to save goal status to localStorage:', e)
  }
}

/**
 * Get goal data from localStorage
 */
function getGoalFromStorage(): GoalResponse | null {
  try {
    const data = localStorage.getItem(GOAL_DATA_KEY)
    return data ? JSON.parse(data) : null
  } catch {
    return null
  }
}

/**
 * Save goal data to localStorage
 */
function saveGoalToStorage(goal: GoalResponse) {
  try {
    localStorage.setItem(GOAL_DATA_KEY, JSON.stringify(goal))
    setGoalStatusInStorage(true)
  } catch (e) {
    console.warn('Failed to save goal data to localStorage:', e)
  }
}

/**
 * Clear goal data from localStorage
 */
function clearGoalFromStorage() {
  try {
    localStorage.removeItem(GOAL_SET_KEY)
    localStorage.removeItem(GOAL_DATA_KEY)
  } catch (e) {
    console.warn('Failed to clear goal data from localStorage:', e)
  }
}

/**
 * Load goal from API with timeout
 */
async function loadGoalFromAPI(): Promise<GoalResponse | null> {
  isLoadingGoal.value = true
  goalError.value = null

  try {
    const goal = await api.getGoal()

    if (goal) {
      currentGoal.value = goal
      saveGoalToStorage(goal)
      hasGoal.value = true
      return goal
    } else {
      hasGoal.value = false
      clearGoalFromStorage()
      return null
    }
  } catch (error) {
    const errorMsg = getUserErrorMessage(error)
    console.error('Failed to load goal from API:', error)

    // Set user-facing error message
    goalError.value = errorMsg

    // If API fails, fall back to localStorage only
    const storedGoal = getGoalFromStorage()
    hasGoal.value = storedGoal !== null
    currentGoal.value = storedGoal
    return storedGoal
  } finally {
    isLoadingGoal.value = false
  }
}

/**
 * Initialize goal check
 * - First checks localStorage for quick response
 * - Then verifies with API (with timeout)
 */
async function initializeGoalCheck(): Promise<boolean> {
  goalError.value = null

  // Quick check from localStorage
  if (isGoalSetInStorage()) {
    const storedGoal = getGoalFromStorage()
    if (storedGoal) {
      currentGoal.value = storedGoal
      hasGoal.value = true
      // Verify with API in background (don't wait)
      loadGoalFromAPI().catch(() => {
        // Background verification failed, but we have localStorage data
        console.log('Background goal verification failed, using cached data')
      })
      return true
    }
  }

  // No goal in storage, check API with timeout
  try {
    const goal = await Promise.race([
      loadGoalFromAPI(),
      new Promise<null>((_, reject) =>
        setTimeout(() => reject(new Error('Init timeout')), 3000)
      )
    ])
    return goal !== null
  } catch (error) {
    // API timeout or error - treat as no goal set
    // Error message is already set by loadGoalFromAPI
    hasGoal.value = false
    return false
  }
}

/**
 * Composable for goal management
 */
export function useGoal() {
  return {
    // State
    hasGoal,
    currentGoal,
    goalError,
    isLoadingGoal,

    // Methods
    isGoalSetInStorage,
    initializeGoalCheck,
    loadGoalFromAPI,
    saveGoalToStorage,
    clearGoalFromStorage,

    // Helper: check if goal is set (returns cached value or checks storage)
    checkGoalSet(): boolean {
      if (hasGoal.value !== null) {
        return hasGoal.value
      }
      return isGoalSetInStorage()
    },

    // Clear error message
    clearError() {
      goalError.value = null
    }
  }
}

/**
 * Helper for router guard - async check
 */
export async function checkGoalForRoute(): Promise<boolean> {
  if (hasGoal.value !== null) {
    return hasGoal.value
  }
  const isSet = await initializeGoalCheck()
  return isSet
}
