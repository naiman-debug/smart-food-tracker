<template>
  <div class="goal-page">
    <!-- 进度指示器 -->
    <div v-if="editing || !currentGoal" class="progress-indicator">
      <div class="progress-step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
        <span class="step-number">1</span>
        <span class="step-label">基本信息</span>
      </div>
      <div class="progress-line" :class="{ active: currentStep > 1 }"></div>
      <div class="progress-step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
        <span class="step-number">2</span>
        <span class="step-label">热量目标</span>
      </div>
    </div>

    <!-- 成功提示 -->
    <div v-if="showSuccessMessage" class="success-message">
      <span class="success-icon">✅</span>
      <div class="success-content">
        <strong>目标设置成功！</strong>
        <p>{{ countdown }}秒后跳转到首页...</p>
      </div>
    </div>

    <!-- 提示消息：需要设置目标 -->
    <div v-if="showGoalRequiredHint" class="goal-required-hint">
      <span class="hint-icon">⚠️</span>
      <div class="hint-content">
        <strong>请先设置您的减脂目标</strong>
        <p>设置目标后即可开始记录饮食</p>
      </div>
    </div>

    <header class="page-header">
      <h1>设置你的目标</h1>
    </header>

    <!-- 已有目标显示 -->
    <div v-if="currentGoal && !editing" class="current-goal-card">
      <h2>📊 你的每日目标</h2>
      <div class="goal-values">
        <div class="goal-item">
          <span class="goal-icon">🔥</span>
          <div class="goal-content">
            <span class="goal-label">热量</span>
            <span class="goal-value">{{ currentGoal.calorie_target.toFixed(0) }} kcal</span>
          </div>
        </div>
        <div class="goal-item">
          <span class="goal-icon">💪</span>
          <div class="goal-content">
            <span class="goal-label">蛋白质</span>
            <span class="goal-value">{{ currentGoal.protein_target.toFixed(0) }}g</span>
          </div>
        </div>
      </div>
      <p class="goal-note">
        这是根据你的身体数据和选定的热量缺口计算的。
      </p>
      <button class="btn-secondary" @click="editing = true">
        修改目标
      </button>
    </div>

    <!-- 设置表单 -->
    <div v-else class="goal-form">
      <section class="form-section">
        <h3>关于你的基本信息：</h3>

        <div class="form-group">
          <label>性别</label>
          <div class="gender-options">
            <button
              class="gender-btn"
              :class="{ active: formData.gender === '男' }"
              @click="formData.gender = '男'"
            >
              男
            </button>
            <button
              class="gender-btn"
              :class="{ active: formData.gender === '女' }"
              @click="formData.gender = '女'"
            >
              女
            </button>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>年龄</label>
            <input
              v-model.number="formData.age"
              type="number"
              class="form-input"
              placeholder="28"
            >
            <span class="input-unit">岁</span>
          </div>

          <div class="form-group">
            <label>身高</label>
            <input
              v-model.number="formData.height_cm"
              type="number"
              class="form-input"
              placeholder="170"
            >
            <span class="input-unit">cm</span>
          </div>
        </div>

        <div class="form-group">
          <label>体重</label>
          <input
            v-model.number="formData.weight_kg"
            type="number"
            class="form-input"
            placeholder="70"
          >
          <span class="input-unit">kg</span>
        </div>
      </section>

      <section class="form-section">
        <h3>你想怎么吃？</h3>
        <p class="section-note">每天热量缺口：</p>

        <div class="deficit-options">
          <button
            v-for="option in deficitOptions"
            :key="option.value"
            class="deficit-option"
            :class="{ active: formData.deficit_target === option.value }"
            @click="formData.deficit_target = option.value"
          >
            <span class="option-label">{{ option.label }}</span>
            <span class="option-desc">{{ option.desc }}</span>
          </button>
        </div>
      </section>

      <!-- 警告模态弹窗 -->
      <div v-if="showWarning" class="modal-overlay" @click.self="closeWarning">
        <div class="modal-content">
          <div class="modal-header">
            <h3>⚠️ 健康提醒</h3>
          </div>
          <div class="modal-body">
            <p>你设置的热量缺口（{{ formData.deficit_target }} kcal/天）超过了安全建议值（-500 kcal/天）。</p>
            <p class="warning-text">过大的缺口可能导致：</p>
            <ul>
              <li>肌肉流失</li>
              <li>基础代谢下降</li>
              <li>营养不良</li>
            </ul>
          </div>
          <div class="modal-footer">
            <button class="btn-modal-secondary" @click="closeWarning">
              仍使用 {{ formData.deficit_target }} kcal/天
            </button>
            <button class="btn-modal-primary" @click="useRecommendedDeficit">
              使用安全值 -500 kcal/天
            </button>
          </div>
        </div>
      </div>

      <!-- 计算结果预览 -->
      <div v-if="calculatedTargets && !showWarning" class="preview-card">
        <h3>📊 你的每日目标</h3>
        <div class="preview-values">
          <div class="preview-item">
            <span>🔥 热量：</span>
            <strong>{{ calculatedTargets.calories.toFixed(0) }} kcal</strong>
          </div>
          <div class="preview-item">
            <span>💪 蛋白质：</span>
            <strong>{{ calculatedTargets.protein.toFixed(0) }}g</strong>
          </div>
        </div>
        <p class="preview-note">
          这是根据你的身体数据和选定的热量缺口计算的。
        </p>
      </div>

      <button class="btn-primary" @click="saveGoal" :disabled="!isValid">
        确认并保存
      </button>

      <button v-if="!currentGoal && showGoalRequiredHint" class="btn-skip" @click="skipGoalSetup">
        跳过，稍后设置
      </button>

      <button v-if="currentGoal" class="btn-link" @click="cancelEdit">
        取消
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { api, type GoalResponse } from '@/api'
import { saveGoalToStorage } from '@/composables/useGoal'

const router = useRouter()

const currentGoal = ref<GoalResponse | null>(null)
const editing = ref(false)
const showWarning = ref(false)
const currentStep = ref(1)
const showSuccessMessage = ref(false)
const countdown = ref(3)

// localStorage key for form data
const GOAL_FORM_KEY = 'smartfood_goal_form_draft'

// Check if user was redirected due to missing goal
const showGoalRequiredHint = computed(() => {
  // Show hint if there's a redirect query parameter (user was redirected by router guard)
  // and no current goal exists
  return router.currentRoute.value.query.redirect !== undefined && !currentGoal.value
})

// Load form data from localStorage or use defaults
function loadFormDataFromStorage() {
  try {
    const saved = localStorage.getItem(GOAL_FORM_KEY)
    if (saved) {
      return JSON.parse(saved)
    }
  } catch (e) {
    console.warn('Failed to load form data from localStorage:', e)
  }
  return {
    gender: '男',
    age: 28,
    height_cm: 175,
    weight_kg: 70,
    deficit_target: -500
  }
}

const formData = ref(loadFormDataFromStorage())

// Watch form changes and save to localStorage
watch(formData, (newData) => {
  try {
    localStorage.setItem(GOAL_FORM_KEY, JSON.stringify(newData))

    // Update progress step based on filled data
    if (newData.gender && newData.age && newData.height_cm && newData.weight_kg) {
      currentStep.value = 2
    } else {
      currentStep.value = 1
    }
  } catch (e) {
    console.warn('Failed to save form data to localStorage:', e)
  }
}, { deep: true })

const deficitOptions = [
  { value: 0, label: '维持体重', desc: '无缺口' },
  { value: -300, label: '温和减重', desc: '-300kcal/天' },
  { value: -500, label: '适度减重', desc: '-500kcal/天' },
  { value: -800, label: '积极减重', desc: '-800kcal/天' }
]

// 计算目标
const calculatedTargets = computed(() => {
  const { gender, age, height_cm, weight_kg, deficit_target } = formData.value

  // 计算 BMR (Mifflin-St Jeor 公式)
  let bmr: number
  if (gender === '男') {
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
  } else {
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
  }

  // TDEE (假设久坐，活动系数 1.2)
  const tdee = bmr * 1.2

  // 蛋白质目标 (1.6g/kg)
  const protein = weight_kg * 1.6

  return {
    calories: tdee + deficit_target,
    protein: protein
  }
})

// 表单验证
const isValid = computed(() => {
  const { gender, age, height_cm, weight_kg, deficit_target } = formData.value
  return (
    (gender === '男' || gender === '女') &&
    age > 0 && age < 120 &&
    height_cm > 0 && height_cm < 250 &&
    weight_kg > 0 && weight_kg < 300 &&
    [0, -300, -500, -800].includes(deficit_target)
  )
})

// 监听缺口值变化，显示警告
watch(() => formData.value.deficit_target, (newVal) => {
  if (newVal < -500) {
    showWarning.value = true
  }
})

// 关闭警告弹窗，保留用户选择的值
function closeWarning() {
  showWarning.value = false
}

// 使用推荐的安全值
function useRecommendedDeficit() {
  formData.value.deficit_target = -500
  showWarning.value = false
}

// 加载当前目标
async function loadGoal() {
  try {
    currentGoal.value = await api.getGoal()
    if (currentGoal.value) {
      // 填充表单
      formData.value = {
        gender: currentGoal.value.gender,
        age: currentGoal.value.age,
        height_cm: currentGoal.value.height_cm,
        weight_kg: currentGoal.value.weight_kg,
        deficit_target: currentGoal.value.deficit_target
      }
    }
  } catch (error) {
    console.error('加载目标失败:', error)
  }
}

// 保存目标
async function saveGoal() {
  if (!isValid.value) return

  if (formData.value.deficit_target < -500 && !confirm('您设置的热量缺口较大，确定要继续吗？')) {
    return
  }

  try {
    const savedGoal = await api.setGoal(formData.value)
    currentGoal.value = savedGoal

    // Save to localStorage and update composable state
    saveGoalToStorage(savedGoal)

    // Clear form draft
    localStorage.removeItem(GOAL_FORM_KEY)

    editing.value = false

    // Show success message
    showSuccessMessage.value = true

    // Countdown and redirect
    const countdownInterval = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(countdownInterval)
        performRedirect()
      }
    }, 1000)
  } catch (error) {
    showSuccessMessage.value = false
    alert('保存失败，请重试')
  }
}

// Perform redirect
function performRedirect() {
  // Get redirect URL from query parameter or sessionStorage
  const redirectUrl = router.currentRoute.value.query.redirect as string ||
                      sessionStorage.getItem('smartfood_return_url') ||
                      '/'

  // Clear the stored return URL
  sessionStorage.removeItem('smartfood_return_url')

  // Redirect to the intended page or home
  router.push(redirectUrl)
}

// Skip goal setup
function skipGoalSetup() {
  // Set a flag to disable record button on home page
  localStorage.setItem('smartfood_goal_skipped', 'true')

  // Still redirect to home
  router.push('/')
}

// 取消编辑
function cancelEdit() {
  if (currentGoal.value) {
    formData.value = {
      gender: currentGoal.value.gender,
      age: currentGoal.value.age,
      height_cm: currentGoal.value.height_cm,
      weight_kg: currentGoal.value.weight_kg,
      deficit_target: currentGoal.value.deficit_target
    }
  }
  editing.value = false
  showWarning.value = false
}

onMounted(() => {
  loadGoal()
})
</script>

<style scoped>
.goal-page {
  min-height: 100vh;
  padding: 20px;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Progress Indicator */
.progress-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #ecf0f1;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
  transition: all 0.3s;
}

.progress-step.active .step-number {
  background: #3498db;
  color: white;
  box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3);
}

.progress-step.completed .step-number {
  background: #2ecc71;
  color: white;
}

.step-label {
  font-size: 0.85rem;
  color: #7f8c8d;
  transition: color 0.3s;
}

.progress-step.active .step-label {
  color: #3498db;
  font-weight: 600;
}

.progress-line {
  width: 60px;
  height: 3px;
  background: #ecf0f1;
  transition: background 0.3s;
}

.progress-line.active {
  background: #2ecc71;
}

/* Success Message */
.success-message {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 18px 20px;
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  border-radius: 16px;
  color: white;
  box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.success-content {
  flex: 1;
}

.success-content strong {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.success-content p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.95;
}

.page-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.goal-required-hint {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 18px 20px;
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  border-radius: 16px;
  color: white;
  box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);
  margin-bottom: 20px;
}

.hint-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.hint-content {
  flex: 1;
}

.hint-content strong {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.hint-content p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.95;
}

.current-goal-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.current-goal-card h2 {
  margin: 0 0 25px 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.goal-values {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
}

.goal-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.goal-icon {
  font-size: 2.5rem;
}

.goal-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.goal-label {
  font-size: 0.85rem;
  color: #7f8c8d;
}

.goal-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.goal-note {
  color: #7f8c8d;
  margin-bottom: 20px;
}

.goal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-section {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.form-section h3 {
  margin: 0 0 20px 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.section-note {
  margin: 0 0 15px 0;
  color: #7f8c8d;
}

.form-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.form-group label {
  min-width: 60px;
  font-weight: 500;
  color: #2c3e50;
}

.form-input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #ecf0f1;
  border-radius: 10px;
  font-size: 1rem;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
}

.input-unit {
  color: #7f8c8d;
  min-width: 30px;
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

.gender-options {
  display: flex;
  gap: 10px;
  flex: 1;
}

.gender-btn {
  flex: 1;
  padding: 12px;
  border: 2px solid #ecf0f1;
  background: white;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.gender-btn.active {
  border-color: #3498db;
  background: #f0f9ff;
  color: #3498db;
}

.deficit-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.deficit-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 18px;
  border: 2px solid #ecf0f1;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.deficit-option.active {
  border-color: #3498db;
  background: #f0f9ff;
}

.option-label {
  font-weight: 500;
  color: #2c3e50;
}

.option-desc {
  color: #7f8c8d;
}

/* 模态弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 20px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 25px 25px 15px 25px;
  border-bottom: 1px solid #ecf0f1;
}

.modal-header h3 {
  margin: 0;
  color: #f39c12;
  font-size: 1.3rem;
}

.modal-body {
  padding: 20px 25px;
  color: #2c3e50;
}

.modal-body p {
  margin: 10px 0;
  line-height: 1.6;
}

.warning-text {
  font-weight: 500;
}

.modal-body ul {
  margin: 10px 0;
  padding-left: 25px;
}

.modal-body li {
  margin: 8px 0;
  color: #e74c3c;
}

.modal-footer {
  padding: 15px 25px 25px 25px;
  display: flex;
  gap: 12px;
  flex-direction: column-reverse;
}

.btn-modal-primary,
.btn-modal-secondary {
  padding: 16px;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-modal-primary {
  background: #f39c12;
  color: white;
  order: 1;
}

.btn-modal-primary:hover {
  background: #e67e22;
}

.btn-modal-secondary {
  background: white;
  color: #7f8c8d;
  border: 2px solid #ecf0f1;
  order: 2;
}

.btn-modal-secondary:hover {
  background: #f8f9fa;
  border-color: #bdc3c7;
}

.preview-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  padding: 25px;
}

.preview-card h3 {
  margin: 0 0 20px 0;
  font-size: 1.2rem;
}

.preview-values {
  display: flex;
  justify-content: space-around;
  margin-bottom: 15px;
}

.preview-item {
  font-size: 1.1rem;
}

.preview-item strong {
  font-size: 1.3rem;
}

.preview-note {
  margin: 0;
  opacity: 0.9;
}

.btn-primary,
.btn-secondary,
.btn-link {
  padding: 18px;
  border: none;
  border-radius: 15px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
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

.btn-link {
  background: transparent;
  color: #7f8c8d;
  text-decoration: underline;
}

.btn-skip {
  padding: 18px;
  border: none;
  border-radius: 15px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  background: #95a5a6;
  color: white;
}

.btn-skip:hover {
  background: #7f8c8d;
}
</style>
