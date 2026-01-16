<template>
  <div class="record-page">
    <!-- 未拍照状态 -->
    <div v-if="!imageData && !showFoodSelector" class="camera-view">
      <div class="camera-placeholder">
        <div class="camera-icon">📷</div>
        <p>对准你的饭菜拍照</p>
      </div>
      <button class="capture-btn" @click="capturePhoto">
        拍照
      </button>
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        style="display: none"
        @change="handleFileSelect"
      >
    </div>

    <!-- 加载中 -->
    <div v-else-if="analyzing" class="loading-view">
      <div class="spinner"></div>
      <p>正在识别食物...</p>
    </div>

    <!-- AI识别失败 - 食物分类选择界面 -->
    <div v-else-if="showFoodSelector" class="food-selector-view">
      <div class="selector-header">
        <h2>识别有点困难，请选择食物</h2>
        <p>从常见食物中选择，或使用搜索功能</p>
      </div>

      <!-- 搜索框 -->
      <div class="search-section">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索食物名称..."
            @input="handleSearch"
            class="search-input"
          >
          <button v-if="searchQuery" @click="clearSearch" class="clear-btn">×</button>
        </div>
      </div>

      <!-- 搜索结果 -->
      <div v-if="searchQuery && searchResults.length > 0" class="search-results">
        <div class="section-title">搜索结果 ({{ searchResults.length }})</div>
        <div class="food-grid">
          <button
            v-for="food in searchResults"
            :key="food.name"
            class="food-result-item"
            @click="selectFood(food.name)"
          >
            <span class="food-result-name">{{ food.name }}</span>
            <span class="food-result-calories">{{ food.calories_per_100g }} 大卡/100g</span>
          </button>
        </div>
      </div>

      <!-- 无搜索结果 -->
      <div v-else-if="searchQuery && searchResults.length === 0" class="no-results">
        <p>未找到相关食物，请尝试其他关键词</p>
      </div>

      <!-- 分类选项卡 -->
      <div v-if="!searchQuery" class="categories-section">
        <div class="section-title">选择分类</div>
        <div class="category-tabs">
          <button
            v-for="category in categories"
            :key="category.key"
            class="category-tab"
            :class="{ active: selectedCategory?.key === category.key }"
            @click="selectCategory(category)"
          >
            <span class="category-icon">{{ category.icon }}</span>
            <span class="category-name">{{ category.name }}</span>
          </button>
        </div>
      </div>

      <!-- 选中分类的食物列表 -->
      <div v-if="!searchQuery && selectedCategory && foodsInCategory.length > 0" class="foods-section">
        <div class="section-title">
          {{ selectedCategory.icon }} {{ selectedCategory.name }}
          <span class="food-count">({{ foodsInCategory.length }}种)</span>
        </div>
        <div class="food-grid">
          <button
            v-for="food in foodsInCategory"
            :key="food.name"
            class="food-item"
            @click="selectFood(food.name)"
          >
            <span class="food-name">{{ food.name }}</span>
            <span class="food-calories">{{ food.calories_per_100g }} 大卡/100g</span>
          </button>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button class="btn-secondary" @click="retakePhoto">
          重新拍照
        </button>
      </div>
    </div>

    <!-- 多食物选择界面 -->
    <div v-else-if="analyzeResult && multiFoodResults && !currentSelectingFood" class="multi-food-view">
      <div class="preview-image">
        <img :src="imageData" alt="Food photo" />
      </div>

      <div class="recognition-result">
        <h2>识别到 {{ multiFoodResults.length }} 种食物</h2>
        <p class="food-list-text">识别到：{{ multiFoodResults.map(f => f.food_name).join('、') }}</p>
        <p>请选择要添加份量的食物：</p>
      </div>

      <div class="food-selection-list">
        <button
          v-for="food in multiFoodResults"
          :key="food.food_name"
          class="food-item"
          :class="{ added: isFoodAdded(food.food_name) }"
          @click="selectFoodForPortion(food)"
          :disabled="isFoodAdded(food.food_name)"
        >
          <span class="food-status">{{ isFoodAdded(food.food_name) ? '✓' : '➕' }}</span>
          <span class="food-name">{{ food.food_name }}</span>
          <span class="food-count">{{ getAddedPortionCount(food.food_name) }} 份</span>
        </button>
      </div>

      <!-- 本餐已添加列表 -->
      <div v-if="addedItems.length > 0" class="added-items-section">
        <h3>本餐已添加 ({{ addedItems.length }} 项)</h3>
        <div class="added-items-list">
          <div
            v-for="(item, index) in addedItems"
            :key="index"
            class="added-item"
          >
            <div class="added-item-info">
              <span class="added-food-name">{{ item.food_name }}</span>
              <span class="added-portion">{{ item.portion_name }}</span>
              <span class="added-calories">{{ item.calories.toFixed(0) }} 大卡</span>
            </div>
            <button class="remove-btn" @click="removeAddedItem(index)">✕</button>
          </div>
        </div>
        <div class="total-calories">
          本餐总计: {{ totalMealCalories.toFixed(0) }} 大卡
        </div>
      </div>

      <div class="action-buttons">
        <button class="btn-secondary" @click="retakePhoto">
          重新拍照
        </button>
        <button class="btn-primary" @click="confirmAllRecords" :disabled="addedItems.length === 0">
          确认记录 ({{ addedItems.length }})
        </button>
      </div>
    </div>

    <!-- 单个食物份量选择界面 -->
    <div v-else-if="currentSelectingFood && !selectedPortion" class="portion-view">
      <div class="portion-header">
        <h2>{{ currentSelectingFood.food_name }}</h2>
        <p>选择份量大小：</p>
      </div>

      <div class="portion-options">
        <button
          v-for="option in currentSelectingFood.portion_options"
          :key="option.id"
          class="portion-option"
          :class="{ selected: selectedPortion?.id === option.id }"
          @click="selectPortion(option)"
        >
          <span class="option-name">○ {{ option.portion_name }}</span>
          <span class="option-info">约{{ option.weight_grams }}g · {{ option.calories.toFixed(0) }}大卡 · {{ option.protein.toFixed(1) }}g蛋白质</span>
        </button>
      </div>

      <div class="action-buttons">
        <button class="btn-secondary" @click="cancelPortionSelection">
          返回
        </button>
        <button class="btn-primary" @click="addToMeal" :disabled="!selectedPortion">
          添加到本餐
        </button>
      </div>
    </div>

    <!-- 记录成功 -->
    <div v-else-if="recordSuccess" class="success-view">
      <div class="success-icon">✓</div>
      <h2>记录成功！</h2>
      <div class="success-info">
        <p>已添加 {{ addedItemsCount }} 种食物</p>
        <p class="success-calories">+{{ totalRecordedCalories.toFixed(0) }} 大卡</p>
      </div>
      <div class="success-actions">
        <button class="btn-secondary" @click="continueAdding">
          继续添加
        </button>
        <button class="btn-primary" @click="goHome">
          完成用餐
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, type PortionOption, type CategoryInfo, type FoodItemInfo, type ApiErrorResponse } from '@/api'

interface FoodRecognitionItem {
  food_name: string
  portion_options: PortionOption[]
}

interface AddedItem {
  food_name: string
  portion_name: string
  weight_grams: number
  calories: number
  protein: number
  visual_portion_id: number
}

const router = useRouter()

// 原有状态
const imageData = ref<string>('')
const analyzing = ref(false)
const recordSuccess = ref(false)
const multiFoodResults = ref<FoodRecognitionItem[]>([])
const currentSelectingFood = ref<FoodRecognitionItem | null>(null)
const selectedPortion = ref<PortionOption | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const addedItems = ref<AddedItem[]>([])
const addedItemsCount = ref(0)
const totalRecordedCalories = ref(0)
const analyzeResult = ref<any>(null)

// 新增：食物选择器状态
const showFoodSelector = ref(false)
const categories = ref<CategoryInfo[]>([])
const selectedCategory = ref<CategoryInfo | null>(null)
const foodsInCategory = ref<FoodItemInfo[]>([])
const searchQuery = ref('')
const searchResults = ref<FoodItemInfo[]>([])

// 计算本餐总热量
const totalMealCalories = computed(() => {
  return addedItems.value.reduce((sum, item) => sum + item.calories, 0)
})

// 检查食物是否已添加
function isFoodAdded(foodName: string): boolean {
  return addedItems.value.some(item => item.food_name === foodName)
}

// 获取食物已添加的份数
function getAddedPortionCount(foodName: string): number {
  return addedItems.value.filter(item => item.food_name === foodName).length
}

// 加载食物分类
async function loadFoodCategories() {
  try {
    categories.value = await api.getFoodCategories()
  } catch (error) {
    console.error('加载食物分类失败:', error)
  }
}

// 选择分类
async function selectCategory(category: CategoryInfo) {
  selectedCategory.value = category
  try {
    const result = await api.getFoodsByCategory(category.key)
    foodsInCategory.value = result.foods
  } catch (error) {
    console.error('加载食物列表失败:', error)
  }
}

// 搜索食物
async function handleSearch() {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }

  try {
    searchResults.value = await api.searchFoods(searchQuery.value)
  } catch (error) {
    console.error('搜索食物失败:', error)
  }
}

// 清除搜索
function clearSearch() {
  searchQuery.value = ''
  searchResults.value = []
}

// 选择食物（从分类或搜索结果）
async function selectFood(foodName: string) {
  analyzing.value = true
  showFoodSelector.value = false

  try {
    const portions = await api.getPortionsByFoodName(foodName)

    // 转换为多食物格式
    multiFoodResults.value = [{
      food_name: foodName,
      portion_options: portions
    }]
    analyzeResult.value = { food_name: foodName }
  } catch (error) {
    console.error('获取份量选项失败:', error)
    alert('获取份量选项失败，请重试')
    showFoodSelector.value = true
  } finally {
    analyzing.value = false
  }
}

// 拍照
function capturePhoto() {
  fileInput.value?.click()
}

// 选择文件
async function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = async (e) => {
      imageData.value = e.target?.result as string
      // 使用多食物识别API
      await analyzeFoodMulti(imageData.value)
    }
    reader.readAsDataURL(file)
  }
}

// 分析食物（多食物模式）
async function analyzeFoodMulti(dataUrl: string) {
  analyzing.value = true
  showFoodSelector.value = false

  try {
    const base64 = dataUrl.split(',')[1]
    const response = await fetch('http://localhost:8000/api/analyze-multi', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_base64: base64, multi_food: true })
    })

    if (!response.ok) {
      const error: ApiErrorResponse = await response.json()

      // 检查是否是识别失败错误
      if (error.code === 'RECOGNITION_FAILED' || response.status === 400) {
        console.log('AI识别失败，显示食物选择器')
        showFoodSelector.value = true
        return
      }

      throw new Error(error.message || '识别失败')
    }

    const data = await response.json()
    multiFoodResults.value = data.foods || []
    analyzeResult.value = data
  } catch (error) {
    console.error('识别失败:', error)
    // 显示食物选择器
    showFoodSelector.value = true
  } finally {
    analyzing.value = false
  }
}

// 选择食物进行份量选择
function selectFoodForPortion(food: FoodRecognitionItem) {
  currentSelectingFood.value = food
  selectedPortion.value = null
}

// 选择份量
function selectPortion(option: PortionOption) {
  selectedPortion.value = option
}

// 取消份量选择
function cancelPortionSelection() {
  currentSelectingFood.value = null
  selectedPortion.value = null
}

// 添加到本餐
function addToMeal() {
  if (!selectedPortion.value || !currentSelectingFood.value) return

  addedItems.value.push({
    food_name: currentSelectingFood.value.food_name,
    portion_name: selectedPortion.value.portion_name,
    weight_grams: selectedPortion.value.weight_grams,
    calories: selectedPortion.value.calories,
    protein: selectedPortion.value.protein,
    visual_portion_id: selectedPortion.value.id
  })

  // 重置选择状态
  currentSelectingFood.value = null
  selectedPortion.value = null
}

// 移除已添加项
function removeAddedItem(index: number) {
  addedItems.value.splice(index, 1)
}

// 重新拍照
function retakePhoto() {
  imageData.value = ''
  analyzeResult.value = null
  multiFoodResults.value = []
  currentSelectingFood.value = null
  selectedPortion.value = null
  addedItems.value = []
  showFoodSelector.value = false
  selectedCategory.value = null
  foodsInCategory.value = []
  searchQuery.value = ''
  searchResults.value = []
}

// 确认所有记录
async function confirmAllRecords() {
  if (addedItems.value.length === 0) return

  try {
    // 批量创建记录
    for (const item of addedItems.value) {
      await api.createRecord({
        image_url: imageData.value,
        food_name: item.food_name,
        visual_portion_id: item.visual_portion_id
      })
    }

    addedItemsCount.value = addedItems.value.length
    totalRecordedCalories.value = totalMealCalories.value
    recordSuccess.value = true
  } catch (error) {
    console.error('记录失败:', error)
    alert('记录失败，请重试')
  }
}

// 继续添加
function continueAdding() {
  // 重置状态，保留图片
  addedItems.value = []
  currentSelectingFood.value = null
  selectedPortion.value = null
  recordSuccess.value = false
  addedItemsCount.value = 0
  totalRecordedCalories.value = 0
}

// 返回首页
function goHome() {
  router.push('/')
}

// 组件挂载时加载食物分类
onMounted(() => {
  loadFoodCategories()
})
</script>

<style scoped>
.record-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.camera-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  gap: 30px;
}

.camera-placeholder {
  text-align: center;
}

.camera-icon {
  font-size: 6rem;
  margin-bottom: 20px;
}

.camera-placeholder p {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.capture-btn {
  padding: 20px 60px;
  font-size: 1.3rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(52, 152, 219, 0.3);
}

/* 食物选择器样式 */
.food-selector-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 15px;
  overflow-y: auto;
}

.selector-header {
  text-align: center;
  padding: 15px;
}

.selector-header h2 {
  margin: 0 0 10px 0;
  font-size: 1.4rem;
  color: #2c3e50;
}

.selector-header p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.95rem;
}

.search-section {
  position: sticky;
  top: 0;
  background: #f5f7fa;
  z-index: 10;
  padding: 10px 0;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 14px 40px 14px 16px;
  font-size: 1rem;
  border: 2px solid #ecf0f1;
  border-radius: 25px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #3498db;
}

.clear-btn {
  position: absolute;
  right: 12px;
  width: 28px;
  height: 28px;
  border: none;
  background: #e74c3c;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.food-count {
  font-size: 0.9rem;
  color: #7f8c8d;
  font-weight: normal;
}

.categories-section {
  background: white;
  border-radius: 15px;
  padding: 15px;
}

.category-tabs {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
}

.category-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 12px 8px;
  background: #f8f9fa;
  border: 2px solid transparent;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-tab:hover {
  background: #f0f9ff;
  border-color: #3498db;
}

.category-tab.active {
  background: #e3f2fd;
  border-color: #3498db;
}

.category-icon {
  font-size: 1.8rem;
}

.category-name {
  font-size: 0.75rem;
  color: #2c3e50;
  text-align: center;
}

.search-results,
.foods-section {
  background: white;
  border-radius: 15px;
  padding: 15px;
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.food-item,
.food-result-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: #f8f9fa;
  border: 2px solid transparent;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.food-item:hover,
.food-result-item:hover {
  border-color: #3498db;
  background: #f0f9ff;
}

.food-name,
.food-result-name {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.95rem;
}

.food-calories,
.food-result-calories {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.no-results {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
}

.multi-food-view,
.portion-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 20px;
}

.preview-image {
  width: 100%;
  max-height: 250px;
  overflow: hidden;
  border-radius: 20px;
  background: #000;
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recognition-result,
.portion-header {
  text-align: center;
  padding: 15px;
}

.recognition-result h2,
.portion-header h2 {
  margin: 0 0 10px 0;
  font-size: 1.4rem;
  color: #2c3e50;
}

.food-list-text {
  margin: 5px 0;
  color: #3498db;
  font-weight: 500;
}

.recognition-result p {
  margin: 5px 0;
  color: #7f8c8d;
}

.food-selection-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.food-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 20px;
  background: white;
  border: 2px solid #ecf0f1;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.food-item:hover:not(.added) {
  border-color: #3498db;
  background: #f0f9ff;
}

.food-item.added {
  border-color: #2ecc71;
  background: #f0fdf4;
  cursor: default;
}

.food-status {
  font-size: 1.3rem;
}

.food-name {
  flex: 1;
  text-align: left;
  font-weight: 500;
  color: #2c3e50;
}

.food-count {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.added-items-section {
  background: white;
  border-radius: 15px;
  padding: 15px;
}

.added-items-section h3 {
  margin: 0 0 15px 0;
  font-size: 1rem;
  color: #2c3e50;
}

.added-items-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.added-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  background: #f8f9fa;
  border-radius: 10px;
}

.added-item-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.added-food-name {
  font-weight: 500;
  color: #2c3e50;
}

.added-portion {
  font-size: 0.85rem;
  color: #7f8c8d;
}

.added-calories {
  font-weight: 500;
  color: #3498db;
}

.remove-btn {
  width: 30px;
  height: 30px;
  border: none;
  background: #e74c3c;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.9rem;
}

.total-calories {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ecf0f1;
  text-align: center;
  font-weight: bold;
  color: #3498db;
  font-size: 1.1rem;
}

.portion-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.portion-option {
  padding: 18px 20px;
  background: white;
  border: 2px solid #ecf0f1;
  border-radius: 15px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
}

.portion-option.selected {
  border-color: #3498db;
  background: #f0f9ff;
}

.portion-option.selected .option-name::before {
  content: '● ';
}

.option-name {
  display: block;
  font-weight: 500;
  color: #2c3e50;
  font-size: 1.1rem;
}

.option-info {
  display: block;
  margin-top: 5px;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: auto;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 18px;
  font-size: 1.1rem;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #7f8c8d;
  border: 2px solid #ecf0f1;
}

.loading-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #ecf0f1;
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.success-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  gap: 20px;
}

.success-icon {
  width: 80px;
  height: 80px;
  background: #2ecc71;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
}

.success-view h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.success-info {
  text-align: center;
}

.success-info p {
  margin: 5px 0;
  color: #7f8c8d;
}

.success-calories {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3498db !important;
}

.success-actions {
  display: flex;
  gap: 15px;
  width: 100%;
}

.success-actions .btn-primary,
.success-actions .btn-secondary {
  flex: 1;
  padding: 18px;
  font-size: 1.1rem;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  font-weight: 500;
}

.success-actions .btn-primary {
  background: #3498db;
  color: white;
}

.success-actions .btn-secondary {
  background: white;
  color: #7f8c8d;
  border: 2px solid #ecf0f1;
}

/* 响应式适配 */
@media (max-width: 480px) {
  .category-tabs {
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
  }

  .category-tab {
    padding: 8px 4px;
  }

  .category-name {
    font-size: 0.65rem;
  }

  .food-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
}
</style>
