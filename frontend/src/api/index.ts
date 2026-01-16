/**
 * API 服务层 - 对接后端
 */

const API_BASE_URL = 'http://localhost:8000/api'
const API_TIMEOUT = 5000 // 5 seconds timeout

/**
 * API Error Types
 */
export enum ApiErrorType {
  TIMEOUT = 'TIMEOUT',
  NETWORK = 'NETWORK',
  SERVER = 'SERVER',
  VALIDATION = 'VALIDATION',
  UNKNOWN = 'UNKNOWN'
}

export class ApiError extends Error {
  constructor(
    message: string,
    public type: ApiErrorType = ApiErrorType.UNKNOWN,
    public userMessage: string = message
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

/**
 * Fetch with timeout wrapper
 * Prevents API calls from hanging indefinitely
 * Distinguishes between timeout and network errors
 */
async function fetchWithTimeout(url: string, options: RequestInit = {}, timeout = API_TIMEOUT): Promise<Response> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    })
    clearTimeout(timeoutId)

    // Check for HTTP errors
    if (!response.ok) {
      if (response.status >= 500) {
        throw new ApiError(
          `Server error: ${response.status}`,
          ApiErrorType.SERVER,
          '服务器错误，请稍后重试'
        )
      }
      if (response.status === 404) {
        throw new ApiError(
          `Not found: ${url}`,
          ApiErrorType.VALIDATION,
          '请求的资源不存在'
        )
      }
      throw new ApiError(
        `HTTP error: ${response.status}`,
        ApiErrorType.SERVER,
        '请求失败，请稍后重试'
      )
    }

    return response
  } catch (error) {
    clearTimeout(timeoutId)

    // Check for AbortError (timeout)
    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiError(
        'Request timeout',
        ApiErrorType.TIMEOUT,
        '请求超时，请检查后端服务是否已启动'
      )
    }

    // Check for network errors (failed to fetch)
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiError(
        'Network error',
        ApiErrorType.NETWORK,
        '网络连接失败，请检查后端服务是否已启动'
      )
    }

    // Re-throw ApiError as-is
    if (error instanceof ApiError) {
      throw error
    }

    // Unknown error
    throw new ApiError(
      error instanceof Error ? error.message : 'Unknown error',
      ApiErrorType.UNKNOWN,
      '发生未知错误，请重试'
    )
  }
}

/**
 * Get user-friendly error message from ApiError or Error
 */
export function getUserErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.userMessage
  }
  if (error instanceof Error) {
    return error.message
  }
  return '发生错误，请重试'
}

// 请求响应类型
export interface PortionOption {
  id: number
  food_name: string
  portion_name: string
  weight_grams: number
  calories: number
  protein: number
}

export interface AnalyzeImageResponse {
  food_name: string
  portion_options: PortionOption[]
}

export interface MealRecordResponse {
  id: number
  image_url: string
  food_name: string
  visual_portion_id: number
  calories: number
  protein: number
  record_date: string
}

export interface DailyBalanceResponse {
  remaining_calories: number
  remaining_protein: number
  consumed_calories: number
  consumed_protein: number
  target_calories: number
  target_protein: number
  meals_count: number
  suggestions: SuggestionItem[]
}

export interface SuggestionItem {
  id: number
  food_name: string
  portion_name: string
  calories: number
  protein: number
  reason: string
}

export interface ProgressDataPoint {
  date: string
  calorie_deficit: number
  consumed_calories: number
}

export interface ProgressResponse {
  total_calorie_deficit: number
  estimated_fat_lost: number
  days_tracked: number
  data_points: ProgressDataPoint[]
  encouragement: string
}

export interface GoalResponse {
  id: number
  gender: string
  age: number
  height_cm: number
  weight_kg: number
  deficit_target: number
  calorie_target: number
  protein_target: number
}

// 食物分类相关类型（AI识别失败备选流程）
export interface CategoryInfo {
  key: string
  name: string
  icon: string
  description: string
}

export interface FoodItemInfo {
  name: string
  category: string
  aliases: string[]
  calories_per_100g: number
  protein_per_100g: number
  portion_count: number
}

export interface FoodCategoriesResponse {
  categories: CategoryInfo[]
}

export interface FoodsByCategoryResponse {
  category: CategoryInfo
  foods: FoodItemInfo[]
}

// 系统信息相关类型
export interface LocalIpResponse {
  ips: string[]
  primary_ip: string
  hostname: string
  count: number
}

export interface IpConfig {
  ips: string[]
  primary_ip: string
  hostname: string
  port: number
  timestamp: number
}

// API错误响应类型
export interface ApiErrorResponse {
  message: string
  code?: string
  recognized_food?: string
  ai_used?: boolean
  available_foods?: string[]
}

// API 服务
export const api = {
  /**
   * 分析食物图片
   */
  async analyzeImage(imageBase64: string): Promise<AnalyzeImageResponse> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_base64: imageBase64 })
    })
    if (!response.ok) throw new Error('图片识别失败')
    return response.json()
  },

  /**
   * 创建饮食记录
   */
  async createRecord(data: {
    image_url: string
    food_name: string
    visual_portion_id: number
  }): Promise<MealRecordResponse> {
    const response = await fetch(`${API_BASE_URL}/records`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('创建记录失败')
    return response.json()
  },

  /**
   * 获取今日余额
   */
  async getBalance(): Promise<DailyBalanceResponse> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/balance`)
    if (!response.ok) throw new Error('获取余额失败')
    return response.json()
  },

  /**
   * 获取进度统计
   */
  async getProgress(range: 'week' | 'month' | 'all' = 'all'): Promise<ProgressResponse> {
    const response = await fetch(`${API_BASE_URL}/progress?range=${range}`)
    if (!response.ok) throw new Error('获取进度失败')
    return response.json()
  },

  /**
   * 设置目标
   */
  async setGoal(data: {
    gender: string
    age: number
    height_cm: number
    weight_kg: number
    deficit_target: number
  }): Promise<GoalResponse> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/goals`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('设置目标失败')
    return response.json()
  },

  /**
   * 获取当前目标
   */
  async getGoal(): Promise<GoalResponse | null> {
    try {
      const response = await fetchWithTimeout(`${API_BASE_URL}/goals`)
      if (!response.ok) return null
      const data = await response.json()
      return data || null
    } catch {
      // On timeout or network error, return null
      return null
    }
  },

  /**
   * 快速记录 - 无需拍照
   */
  async quickRecord(visualPortionId: number): Promise<MealRecordResponse> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/quick-record`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ visual_portion_id: visualPortionId })
    })
    if (!response.ok) throw new Error('快速记录失败')
    return response.json()
  },

  /**
   * 获取食物分类列表（AI识别失败备选流程）
   */
  async getFoodCategories(): Promise<CategoryInfo[]> {
    const response = await fetch(`${API_BASE_URL}/food-categories`)
    if (!response.ok) throw new Error('获取食物分类失败')
    const data: FoodCategoriesResponse = await response.json()
    return data.categories
  },

  /**
   * 获取指定分类下的食物列表
   */
  async getFoodsByCategory(categoryKey: string): Promise<FoodsByCategoryResponse> {
    const response = await fetch(`${API_BASE_URL}/foods-by-category/${categoryKey}`)
    if (!response.ok) throw new Error('获取食物列表失败')
    return response.json()
  },

  /**
   * 搜索食物
   */
  async searchFoods(query: string): Promise<FoodItemInfo[]> {
    const response = await fetch(`${API_BASE_URL}/food-search?q=${encodeURIComponent(query)}`)
    if (!response.ok) throw new Error('搜索食物失败')
    return response.json()
  },

  /**
   * 获取指定食物的份量选项（通过食物名称，无需AI识别）
   */
  async getPortionsByFoodName(foodName: string): Promise<PortionOption[]> {
    const response = await fetch(`${API_BASE_URL}/portions/${encodeURIComponent(foodName)}`)
    if (!response.ok) {
      const error: ApiErrorResponse = await response.json()
      throw error
    }
    const data: AnalyzeImageResponse = await response.json()
    return data.portion_options
  },

  /**
   * 获取本地IP地址（从后端API）
   */
  async getLocalIp(): Promise<LocalIpResponse | null> {
    try {
      const response = await fetch('http://localhost:8000/api/system/local-ip')
      if (!response.ok) return null
      return await response.json()
    } catch {
      return null
    }
  },

  /**
   * 从静态配置文件获取IP地址
   */
  async getIpFromConfig(): Promise<IpConfig | null> {
    try {
      const response = await fetch('/ip-config.json')
      if (!response.ok) return null
      return await response.json()
    } catch {
      return null
    }
  }
}
