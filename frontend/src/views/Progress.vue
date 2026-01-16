<template>
  <div class="progress-page">
    <header class="page-header">
      <h1>📈 进度追踪</h1>
      <router-link to="/" class="back-link">返回首页</router-link>
    </header>

    <!-- 时间范围选择 -->
    <div class="range-tabs">
      <button
        v-for="range in ranges"
        :key="range.value"
        class="range-tab"
        :class="{ active: currentRange === range.value }"
        @click="switchRange(range.value)"
      >
        {{ range.label }}
      </button>
    </div>

    <!-- 核心数据 -->
    <div class="stats-card">
      <div class="deficit-display">
        <span class="deficit-value" :class="{ surplus: progress.total_calorie_deficit > 0 }">
          {{ progress.total_calorie_deficit.toFixed(0) }}
        </span>
        <span class="deficit-unit">kcal</span>
      </div>
      <p class="fat-lost">
        {{ progress.total_calorie_deficit < 0 ? '累计热量缺口' : '累计热量盈余' }}
      </p>
      <p class="fat-lost">
        相当于约{{ progress.total_calorie_deficit < 0 ? '减脂' : '增脂' }} {{ Math.abs(progress.estimated_fat_lost).toFixed(2) }} kg
      </p>
    </div>

    <!-- 简易趋势图 -->
    <div class="chart-card" v-if="progress.data_points.length > 0">
      <h3>热量缺口趋势</h3>
      <div class="simple-chart">
        <div class="chart-bars">
          <div
            v-for="(point, index) in progress.data_points"
            :key="index"
            class="chart-bar-wrapper"
          >
            <div
              class="chart-bar"
              :class="{ positive: point.calorie_deficit > 0, negative: point.calorie_deficit < 0 }"
              :style="{
                height: getBarHeight(point.calorie_deficit) + '%'
              }"
            ></div>
            <span class="bar-label">{{ formatDate(point.date) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 鼓励语 -->
    <div class="encouragement-card">
      <p>{{ progress.encouragement }}</p>
    </div>

    <!-- 记录天数 -->
    <div class="days-tracked">
      已记录 <strong>{{ progress.days_tracked }}</strong> 天
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type ProgressResponse } from '@/api'

const ranges = [
  { label: '本周', value: 'week' },
  { label: '本月', value: 'month' },
  { label: '全部', value: 'all' }
]

const currentRange = ref<'week' | 'month' | 'all'>('all')
const progress = ref<ProgressResponse>({
  total_calorie_deficit: 0,
  estimated_fat_lost: 0,
  days_tracked: 0,
  data_points: [],
  encouragement: '好的开始，继续保持！'
})

const loading = ref(false)
const maxDeficit = ref(500) // 用于计算图表高度

// 加载进度数据
async function loadProgress() {
  loading.value = true
  try {
    progress.value = await api.getProgress(currentRange.value)

    // 计算最大缺口值（用于图表缩放）
    if (progress.value.data_points.length > 0) {
      const maxValue = Math.max(
        ...progress.value.data_points.map(p => Math.abs(p.calorie_deficit))
      )
      maxDeficit.value = Math.max(maxValue, 500)
    }
  } catch (error) {
    console.error('加载进度失败:', error)
  } finally {
    loading.value = false
  }
}

// 切换时间范围
function switchRange(range: 'week' | 'month' | 'all') {
  currentRange.value = range
  loadProgress()
}

// 计算柱状图高度
function getBarHeight(deficit: number) {
  return Math.min(Math.abs(deficit) / maxDeficit.value * 100, 100)
}

// 格式化日期
function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

onMounted(() => {
  loadProgress()
})
</script>

<style scoped>
.progress-page {
  min-height: 100vh;
  padding: 20px;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.back-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.range-tabs {
  display: flex;
  gap: 10px;
  background: white;
  padding: 8px;
  border-radius: 15px;
}

.range-tab {
  flex: 1;
  padding: 12px;
  border: none;
  background: transparent;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 500;
  color: #7f8c8d;
  transition: all 0.2s;
}

.range-tab.active {
  background: #3498db;
  color: white;
}

.stats-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.deficit-display {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 8px;
}

.deficit-value {
  font-size: 3rem;
  font-weight: bold;
  color: #2ecc71;
}

.deficit-value.surplus {
  color: #e74c3c;
}

.deficit-unit {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.fat-lost {
  margin: 15px 0 0 0;
  color: #7f8c8d;
}

.chart-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.chart-card h3 {
  margin: 0 0 20px 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.simple-chart {
  height: 150px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 120px;
  gap: 8px;
}

.chart-bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.chart-bar {
  width: 100%;
  min-height: 4px;
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

.chart-bar.positive {
  background: #e74c3c;
}

.chart-bar.negative {
  background: #2ecc71;
}

.bar-label {
  font-size: 0.7rem;
  color: #7f8c8d;
}

.encouragement-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.encouragement-card p {
  margin: 0;
  font-size: 1.1rem;
}

.days-tracked {
  text-align: center;
  padding: 15px;
  color: #7f8c8d;
}

.days-tracked strong {
  color: #2c3e50;
}
</style>
