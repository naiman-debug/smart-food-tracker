<template>
  <div class="home-page">
    <!-- 服务连接错误提示 -->
    <div v-if="goalError" class="error-card">
      <span class="error-icon">⚠️</span>
      <div class="error-content">
        <strong>无法连接到服务器</strong>
        <p>{{ goalError }}</p>
      </div>
      <button class="error-close-btn" @click="clearGoalError">×</button>
    </div>

    <!-- 今日余额卡片 -->
    <div class="balance-card">
      <h2 class="card-title">📊 今日余额</h2>

      <div class="balance-item">
        <div class="balance-icon">🔥</div>
        <div class="balance-content">
          <span class="balance-label">剩余热量</span>
          <span class="balance-value">{{ balance.remaining_calories.toFixed(0) }} 大卡</span>
        </div>
      </div>

      <div class="balance-item">
        <div class="balance-icon">💪</div>
        <div class="balance-content">
          <span class="balance-label">剩余蛋白质</span>
          <span class="balance-value">{{ balance.remaining_protein.toFixed(0) }}g</span>
        </div>
      </div>

      <div class="balance-progress">
        <div class="progress-bar">
          <div class="progress-fill calories" :style="{ width: caloriesPercent + '%' }"></div>
        </div>
        <div class="progress-text">
          已用 {{ balance.consumed_calories.toFixed(0) }} / {{ balance.target_calories.toFixed(0) }} 大卡
        </div>
      </div>
    </div>

    <!-- 智能建议 -->
    <div class="suggestions-card" v-if="suggestions.length > 0">
      <h3 class="card-subtitle">🧠 可以吃这些：</h3>
      <div class="suggestion-list">
        <button
          v-for="item in suggestions"
          :key="item.id"
          class="suggestion-item"
          :disabled="item.adding"
          @click="quickAdd(item)"
        >
          <span class="suggestion-icon">{{ item.adding ? '⏳' : '➕' }}</span>
          <span class="suggestion-name">{{ item.food_name }}</span>
          <span class="suggestion-calories">{{ item.calories }} 大卡</span>
          <span class="suggestion-reason">{{ item.reason }}</span>
        </button>
      </div>
    </div>

    <!-- 手机访问提示 -->
    <div v-if="showMobileHint" class="mobile-access-card">
      <div class="mobile-access-header">
        <span class="mobile-icon">📱</span>
        <span class="mobile-title">手机访问</span>
        <button class="close-hint-btn" @click="closeMobileHint">×</button>
      </div>

      <!-- 多个IP地址显示 -->
      <div v-if="multipleIPs.length > 1" class="mobile-ips-list">
        <p class="mobile-access-text">检测到多个IP地址，请选择可用的：</p>
        <div
          v-for="ip in multipleIPs"
          :key="ip"
          class="mobile-url-item"
          :class="{ active: localIP === ip }"
          @click="localIP = ip"
        >
          http://{{ ip }}:5173
        </div>
      </div>

      <!-- 单个IP或选定IP显示 -->
      <p class="mobile-access-text" v-else>
        手机连接同一WiFi，访问以下地址：
      </p>

      <div v-if="multipleIPs.length <= 1" class="mobile-url-container">
        <div class="mobile-url">
          http://{{ localIP }}:5173
        </div>
        <button class="copy-url-btn" @click="copyMobileUrl" title="复制链接">
          📋 复制
        </button>
      </div>

      <!-- WiFi连接指引 -->
      <div class="wifi-guide">
        <details>
          <summary class="wifi-guide-toggle">
            🔍 手机无法连接？
          </summary>
          <div class="wifi-guide-content">
            <p><strong>检查清单：</strong></p>
            <ol>
              <li>确保手机和电脑连接同一个WiFi</li>
              <li>检查电脑防火墙是否允许5173端口</li>
              <li>Windows: 控制面板 → 系统和安全 → Windows防火墙 → 允许应用通过防火墙</li>
              <li>尝试在手机浏览器手动输入上方地址</li>
            </ol>
            <p class="faq-link">
              <a href="#" @click.prevent>查看详细故障排除 →</a>
            </p>
          </div>
        </details>
      </div>
    </div>

    <!-- 立刻记录按钮 -->
    <router-link to="/record" class="record-btn">
      <span class="record-icon">📷</span>
      <span class="record-text">立刻记录</span>
    </router-link>

    <!-- 今日记录状态 -->
    <div class="meals-status">
      <span class="meals-label">📅 今日</span>
      <span class="meals-checks">
        <span v-for="n in balance.meals_count" :key="n" class="check">✔</span>
        <span v-if="balance.meals_count === 0" class="check-empty">暂无记录</span>
      </span>
    </div>

    <!-- 查看进度按钮 -->
    <router-link to="/progress" class="progress-link">
      📈 查看进度
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api, type DailyBalanceResponse, type SuggestionItem } from '@/api'
import { useGoal } from '@/composables/useGoal'

const balance = ref<DailyBalanceResponse>({
  remaining_calories: 2000,
  remaining_protein: 120,
  consumed_calories: 0,
  consumed_protein: 0,
  target_calories: 2000,
  target_protein: 120,
  meals_count: 0,
  suggestions: []
})

const loading = ref(false)

// Get goal state and error from composable
const { goalError, isLoadingGoal, clearError: clearGoalError } = useGoal()

// Mobile access - IP address
const localIP = ref<string>('获取中...')
const showMobileHint = ref(true)
const multipleIPs = ref<string[]>([])

/**
 * Multi-tier IP fetching strategy:
 * 1. Backend API (most reliable)
 * 2. Static config file (fallback)
 * 3. WebRTC (client-side detection)
 * 4. Window.location (final fallback)
 */
async function getLocalIP() {
  // Tier 1: Try backend API
  try {
    const backendIp = await api.getLocalIp()
    if (backendIp && backendIp.primary_ip) {
      localIP.value = backendIp.primary_ip
      multipleIPs.value = backendIp.ips || []
      return
    }
  } catch (error) {
    console.warn('Backend API IP fetch failed:', error)
  }

  // Tier 2: Try static config file
  try {
    const configIp = await api.getIpFromConfig()
    if (configIp && configIp.primary_ip) {
      localIP.value = configIp.primary_ip
      multipleIPs.value = configIp.ips || []
      return
    }
  } catch (error) {
    console.warn('Config file IP fetch failed:', error)
  }

  // Tier 3: WebRTC fallback
  try {
    const rtc = new RTCPeerConnection({ iceServers: [] })
    rtc.createDataChannel('')
    rtc.createOffer().then(offer => rtc.setLocalDescription(offer))

    rtc.onicecandidate = (evt) => {
      if (evt.candidate) {
        const ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3})/
        const match = ipRegex.exec(evt.candidate.candidate)
        if (match && match[1] && !match[1].startsWith('127.')) {
          localIP.value = match[1]
          rtc.close()
        }
      }
    }

    // Fallback after timeout
    setTimeout(() => {
      if (localIP.value === '获取中...') {
        // Tier 4: Final fallback
        localIP.value = window.location.hostname
      }
      rtc.close()
    }, 1000)
  } catch {
    // Tier 4: Final fallback
    localIP.value = window.location.hostname
  }
}

// Copy URL to clipboard
async function copyMobileUrl() {
  const url = `http://${localIP.value}:5173`
  try {
    await navigator.clipboard.writeText(url)
    // Could add a toast notification here
    alert('链接已复制到剪贴板')
  } catch {
    // Fallback for older browsers
    const textArea = document.createElement('textarea')
    textArea.value = url
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    alert('链接已复制到剪贴板')
  }
}

// Close mobile hint
function closeMobileHint() {
  showMobileHint.value = false
}

const caloriesPercent = computed(() => {
  return (balance.value.consumed_calories / balance.value.target_calories) * 100
})

// 智能建议（从后端API获取）
const suggestions = ref<{ id: number; food_name: string; portion_name: string; calories: number; protein: number; reason: string; adding: boolean }[]>([])

function updateSuggestions() {
  // 将后端返回的suggestions转换为前端需要的格式
  suggestions.value = balance.value.suggestions.map(s => ({
    ...s,
    adding: false
  }))
}

// 加载余额数据
async function loadBalance() {
  loading.value = true
  try {
    balance.value = await api.getBalance()
    updateSuggestions()
  } catch (error) {
    console.error('加载余额失败:', error)
  } finally {
    loading.value = false
  }
}

// 快速加餐 - 调用后端quick-record接口
async function quickAdd(item: { id: number; food_name: string; adding: boolean }) {
  item.adding = true

  try {
    await api.quickRecord(item.id)

    // 记录成功后重新加载余额
    await loadBalance()
  } catch (error) {
    console.error('快速添加失败:', error)
    alert('添加失败，请重试')
  } finally {
    item.adding = false
  }
}

onMounted(() => {
  loadBalance()
  getLocalIP()
})
</script>

<style scoped>
.home-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.balance-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-title {
  margin: 0 0 20px 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.balance-item {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.balance-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 12px;
}

.balance-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.balance-label {
  font-size: 0.85rem;
  color: #7f8c8d;
}

.balance-value {
  font-size: 1.4rem;
  font-weight: bold;
  color: #2c3e50;
}

.balance-progress {
  margin-top: 10px;
}

.progress-bar {
  height: 8px;
  background: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.suggestions-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-subtitle {
  margin: 0 0 15px 0;
  font-size: 1rem;
  color: #2c3e50;
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 15px;
  background: #f8f9fa;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.suggestion-item:hover:not(:disabled) {
  background: #e9ecef;
}

.suggestion-item:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.suggestion-icon {
  font-size: 1.2rem;
}

.suggestion-name {
  flex: 1;
  text-align: left;
  font-weight: 500;
  color: #2c3e50;
}

.suggestion-calories {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.suggestion-reason {
  font-size: 0.75rem;
  color: #95a5a6;
  margin-left: auto;
}

.record-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 25px;
  background: linear-gradient(135deg, #3498db, #2ecc71);
  color: white;
  border: none;
  border-radius: 20px;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: bold;
  box-shadow: 0 4px 20px rgba(52, 152, 219, 0.3);
  transition: transform 0.2s;
}

.record-btn:hover {
  transform: scale(1.02);
}

.record-icon {
  font-size: 2.5rem;
}

.meals-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #f8f9fa;
  border-radius: 15px;
}

.meals-label {
  font-weight: 500;
  color: #2c3e50;
}

.meals-checks {
  display: flex;
  gap: 8px;
}

.check {
  color: #2ecc71;
  font-weight: bold;
}

.check-empty {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.progress-link {
  text-align: center;
  padding: 15px;
  background: white;
  color: #3498db;
  text-decoration: none;
  border-radius: 15px;
  font-weight: 500;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
}

.progress-link:hover {
  background: #f8f9fa;
}

.mobile-access-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 18px 20px;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.mobile-access-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.mobile-icon {
  font-size: 1.3rem;
}

.mobile-title {
  flex: 1;
  margin-left: 10px;
  font-weight: 600;
  font-size: 1rem;
}

.close-hint-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.close-hint-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.mobile-access-text {
  margin: 0 0 10px 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

.mobile-ips-list {
  margin-bottom: 12px;
}

.mobile-url-item {
  background: rgba(255, 255, 255, 0.15);
  padding: 10px 15px;
  border-radius: 10px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.95rem;
  text-align: center;
  word-break: break-all;
  cursor: pointer;
  margin-bottom: 8px;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.mobile-url-item:hover {
  background: rgba(255, 255, 255, 0.25);
}

.mobile-url-item.active {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
}

.mobile-url-container {
  display: flex;
  gap: 10px;
  align-items: stretch;
  margin-bottom: 12px;
}

.mobile-url {
  flex: 1;
  background: rgba(255, 255, 255, 0.2);
  padding: 10px 15px;
  border-radius: 10px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 1rem;
  text-align: center;
  word-break: break-all;
  user-select: all;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-url:hover {
  background: rgba(255, 255, 255, 0.25);
}

.copy-url-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 10px 15px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  white-space: nowrap;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.copy-url-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.wifi-guide {
  margin-top: 8px;
}

.wifi-guide-toggle {
  cursor: pointer;
  font-size: 0.85rem;
  opacity: 0.9;
  user-select: none;
  padding: 8px 0;
}

.wifi-guide-toggle:hover {
  opacity: 1;
}

.wifi-guide-content {
  margin-top: 10px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  font-size: 0.85rem;
}

.wifi-guide-content p {
  margin: 8px 0;
}

.wifi-guide-content ol {
  margin: 8px 0;
  padding-left: 20px;
}

.wifi-guide-content li {
  margin: 6px 0;
  line-height: 1.4;
}

.faq-link {
  margin-top: 8px;
}

.faq-link a {
  color: white;
  text-decoration: underline;
  opacity: 0.9;
}

.faq-link a:hover {
  opacity: 1;
}

/* Error Card Styles */
.error-card {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 18px 20px;
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  border-radius: 16px;
  color: white;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
  margin-bottom: 20px;
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

.error-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.error-content {
  flex: 1;
}

.error-content strong {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.error-content p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.95;
}

.error-close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  flex-shrink: 0;
}

.error-close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
