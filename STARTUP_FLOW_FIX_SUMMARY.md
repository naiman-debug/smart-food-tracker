# 启动流程和手机访问指引修复摘要

> 智能食物记录 App - 启动流程与PRD对齐修复

---

## 问题分析

### 1. 启动流程与PRD不符

**问题描述：**
- 应用启动后直接显示首页，未检查用户是否已设置目标
- 用户可以浏览所有页面而不需要先设置目标
- "立刻记录"按钮始终可用，即使没有设置目标

**PRD要求：**
- 应用启动时应检查用户是否已设置目标
- 未设置目标时，应自动重定向到目标设置页
- 显示提示信息："请先设置您的减脂目标"
- 首页的"立刻记录"按钮在未设置目标时应为禁用状态

### 2. 缺少手机访问指引

**问题描述：**
- 应用内没有提供手机访问的IP地址信息
- 用户不知道如何在手机上访问应用

**PRD要求：**
- 在首页显示手机访问指引
- 提示内容："手机连接同一WiFi，访问 http://[您的IP]:5173"

### 3. 目标设置页流程不完善

**问题描述：**
- 目标设置完成后直接显示"目标已保存"弹窗
- 没有自动跳转到用户原本想访问的页面
- 缺少明确的提示告知用户为什么被重定向到目标设置页

---

## 修复方案

### 1. 创建目标状态管理 Composable

**文件路径：** `frontend/src/composables/useGoal.ts` (新增)

**功能说明：**
- 提供全局目标状态管理
- localStorage 缓存目标状态（快速响应）
- API 验证目标状态（确保准确性）
- 提供路由守卫使用的异步检查函数

**关键代码：**

```typescript
// Global goal state
const hasGoal = ref<boolean | null>(null)  // null = not checked yet
const currentGoal = ref<GoalResponse | null>(null)

// localStorage key for goal status
const GOAL_SET_KEY = 'smartfood_goal_set'
const GOAL_DATA_KEY = 'smartfood_goal_data'

// Initialize goal check - first checks localStorage, then verifies with API
async function initializeGoalCheck(): Promise<boolean> {
  // Quick check from localStorage
  if (isGoalSetInStorage()) {
    const storedGoal = getGoalFromStorage()
    if (storedGoal) {
      currentGoal.value = storedGoal
      hasGoal.value = true
      loadGoalFromAPI()  // Verify with API in background
      return true
    }
  }
  const goal = await loadGoalFromAPI()
  return goal !== null
}

// Helper for router guard - async check
export async function checkGoalForRoute(): Promise<boolean> {
  if (hasGoal.value !== null) {
    return hasGoal.value
  }
  const isSet = await initializeGoalCheck()
  return isSet
}
```

---

### 2. 添加路由守卫

**文件路径：** `frontend/src/router/index.ts`

**修改内容：**

| 修改项 | 修改前 | 修改后 |
|--------|--------|--------|
| 路由元数据 | 无 | 添加 `meta: { requiresGoal: true }` |
| 路由守卫 | 无 | 添加 `beforeEach` 守卫检查目标状态 |
| 重定向逻辑 | 无 | 存储目标URL并重定向到目标页 |

**修改代码：**

```typescript
import { checkGoalForRoute } from '@/composables/useGoal'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresGoal: true }  // 添加元数据
  },
  {
    path: '/goal',
    name: 'Goal',
    component: () => import('@/views/Goal.vue'),
    meta: { requiresGoal: false }  // 目标页始终可访问
  },
  // ... 其他路由
]

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const requiresGoal = to.meta?.requiresGoal !== false

  if (requiresGoal) {
    const hasGoalSet = await checkGoalForRoute()

    if (!hasGoalSet) {
      // 存储目标URL
      const returnUrl = to.fullPath !== '/' ? to.fullPath : '/'
      if (returnUrl !== '/') {
        sessionStorage.setItem('smartfood_return_url', returnUrl)
      }
      // 重定向到目标页
      next({ name: 'Goal', query: { redirect: returnUrl === '/' ? undefined : returnUrl } })
      return
    }
  }

  next()
})
```

---

### 3. 更新目标设置页

**文件路径：** `frontend/src/views/Goal.vue`

**修改内容：**

| 修改项 | 修改前 | 修改后 |
|--------|--------|--------|
| 导入 | 无 `useRouter` | 添加 `useRouter`, `saveGoalToStorage` |
| 提示消息 | 无 | 添加"请先设置您的减脂目标"提示条 |
| 保存后行为 | 显示弹窗提示 | 自动跳转到目标页面 |

**新增代码：**

```vue
<!-- 提示消息：需要设置目标 -->
<div v-if="showGoalRequiredHint" class="goal-required-hint">
  <span class="hint-icon">⚠️</span>
  <div class="hint-content">
    <strong>请先设置您的减脂目标</strong>
    <p>设置目标后即可开始记录饮食</p>
  </div>
</div>
```

```typescript
// 检查是否显示提示
const showGoalRequiredHint = computed(() => {
  return router.currentRoute.value.query.redirect !== undefined && !currentGoal.value
})

// 保存目标后自动跳转
async function saveGoal() {
  const savedGoal = await api.setGoal(formData.value)
  currentGoal.value = savedGoal
  saveGoalToStorage(savedGoal)  // 保存到 localStorage

  // 获取目标URL
  const redirectUrl = router.currentRoute.value.query.redirect as string ||
                      sessionStorage.getItem('smartfood_return_url') ||
                      '/'

  // 清除存储的URL
  sessionStorage.removeItem('smartfood_return_url')

  // 跳转到目标页面
  router.push(redirectUrl)
}
```

---

### 4. 更新首页组件

**文件路径：** `frontend/src/views/Home.vue`

**修改内容：**

| 修改项 | 修改前 | 修改后 |
|--------|--------|--------|
| 导入 | 无 `useGoal` | 添加 `useGoal` composable |
| 手机访问提示 | 无 | 添加IP地址检测和显示卡片 |
| IP获取 | 无 | 使用WebRTC获取本地IP |

**新增代码：**

```vue
<!-- 手机访问提示 -->
<div v-if="showMobileHint" class="mobile-access-card">
  <div class="mobile-access-header">
    <span class="mobile-icon">📱</span>
    <span class="mobile-title">手机访问</span>
    <button class="close-hint-btn" @click="closeMobileHint">×</button>
  </div>
  <p class="mobile-access-text">
    手机连接同一WiFi，访问以下地址：
  </p>
  <div class="mobile-url">
    http://{{ localIP }}:5173
  </div>
</div>
```

```typescript
// Mobile access - IP address
const localIP = ref<string>('获取中...')
const showMobileHint = ref(true)

// Get local IP address for mobile access (using WebRTC)
async function getLocalIP() {
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

    setTimeout(() => {
      if (localIP.value === '获取中...') {
        localIP.value = window.location.hostname
      }
      rtc.close()
    }, 1000)
  } catch {
    localIP.value = window.location.hostname
  }
}

onMounted(() => {
  loadBalance()
  getLocalIP()  // 获取本地IP
})
```

---

## 完整文件路径

### 新增文件

| 文件路径 | 说明 |
|----------|------|
| `frontend/src/composables/useGoal.ts` | 目标状态管理 composable |

### 修改文件

| 文件路径 | 修改内容 |
|----------|----------|
| `frontend/src/router/index.ts` | 添加路由守卫和元数据 |
| `frontend/src/views/Goal.vue` | 添加提示消息和自动跳转逻辑 |
| `frontend/src/views/Home.vue` | 添加手机访问提示和IP地址检测 |

---

## 修复效果对比

### 修复前

**启动流程：**
```
用户打开应用
    └─→ 直接显示首页
        └─→ 可以点击"立刻记录"
            └─→ 可以记录饮食
```

**问题：**
- ❌ 未设置目标也能使用所有功能
- ❌ 没有提示用户需要设置目标
- ❌ 不支持手机访问指引

### 修复后

**启动流程：**
```
用户打开应用
    └─→ 路由守卫检查目标状态
        ├─→ 已设置目标
        │   └─→ 显示首页（含手机访问提示）
        │
        └─→ 未设置目标
            └─→ 重定向到目标设置页
                └─→ 显示提示："请先设置您的减脂目标"
                    └─→ 用户设置目标
                        └─→ 自动跳转到首页
```

**效果：**
- ✅ 必须先设置目标才能使用核心功能
- ✅ 清晰的提示告知用户为何需要设置目标
- ✅ 目标设置后自动返回原本想访问的页面
- ✅ 首页显示手机访问IP地址

---

## 启动流程详细步骤

### 首次使用（无目标）

```
1. 用户访问 http://localhost:5173
   ↓
2. 路由守卫检查目标状态
   ├─→ 检查 localStorage (无数据)
   ├─→ 调用 GET /api/goals (返回 null)
   └─→ hasGoal = false
   ↓
3. 重定向到 /goal?redirect=/
   ↓
4. 目标页面显示
   ┌─────────────────────────────────┐
   │ ⚠️ 请先设置您的减脂目标        │
   │ 设置目标后即可开始记录饮食      │
   └─────────────────────────────────┘
   ↓
5. 用户填写信息并保存
   ↓
6. 调用 POST /api/goals
   ↓
7. 保存目标到 localStorage
   ↓
8. 跳转到首页 /
   ↓
9. 显示今日余额 + 手机访问提示
```

### 已有目标

```
1. 用户访问 http://localhost:5173
   ↓
2. 路由守卫检查目标状态
   ├─→ 检查 localStorage (有数据) ✓
   └─→ hasGoal = true (快速返回)
   ↓
3. 直接显示首页
   ┌─────────────────────────────────┐
   │ 📊 今日余额                     │
   │ 📱 手机访问                     │
   │    http://192.168.1.100:5173    │
   └─────────────────────────────────┘
```

---

## 验证测试

### 测试方法 1: 清除 localStorage

```javascript
// 在浏览器控制台执行
localStorage.removeItem('smartfood_goal_set')
localStorage.removeItem('smartfood_goal_data')
location.reload()
```

**预期结果：**
1. 页面重定向到 `/goal?redirect=/`
2. 显示"请先设置您的减脂目标"提示条
3. 设置目标后自动跳转回首页

### 测试方法 2: 直接访问受保护路由

```
直接访问: http://localhost:5173/record
```

**预期结果：**
1. 重定向到 `/goal?redirect=/record`
2. 设置目标后自动跳转到 `/record`

### 测试方法 3: 模拟已有目标

```javascript
// 在浏览器控制台执行
localStorage.setItem('smartfood_goal_set', 'true')
localStorage.setItem('smartfood_goal_data', JSON.stringify({
  id: 1,
  gender: '男',
  age: 28,
  height_cm: 175,
  weight_kg: 70,
  deficit_target: -500,
  calorie_target: 2000,
  protein_target: 120
}))
location.reload()
```

**预期结果：**
1. 直接显示首页
2. 显示今日余额数据
3. 显示手机访问提示

---

## 文件结构

```
frontend/src/
├── composables/
│   └── useGoal.ts              # 新增：目标状态管理
│
├── router/
│   └── index.ts                # 修改：添加路由守卫
│
├── views/
│   ├── Home.vue                # 修改：添加手机访问提示
│   ├── Goal.vue                # 修改：添加提示消息和自动跳转
│   ├── Record.vue              # 受路由守卫保护
│   └── Progress.vue            # 受路由守卫保护
│
├── api/
│   └── index.ts                # API 服务层（无需修改）
│
├── App.vue
└── main.ts
```

---

## 样式预览

### 目标页提示条

```
┌──────────────────────────────────────────────┐
│ ⚠️  请先设置您的减脂目标                     │
│    设置目标后即可开始记录饮食                 │
└──────────────────────────────────────────────┘
```

### 手机访问提示卡片

```
┌──────────────────────────────────────────────┐
│ 📱  手机访问                      ×          │
│                                              │
│ 手机连接同一WiFi，访问以下地址：              │
│                                              │
│    http://192.168.1.100:5173                 │
└──────────────────────────────────────────────┘
```

---

## 技术实现细节

### localStorage 缓存策略

| 数据项 | Key | 说明 |
|--------|-----|------|
| 目标状态 | `smartfood_goal_set` | 布尔值，快速判断是否已设置 |
| 目标数据 | `smartfood_goal_data` | JSON字符串，存储完整目标信息 |

### IP地址获取方式

**WebRTC 方法（优先）：**
- 创建 RTCPeerConnection
- 监听 onicecandidate 事件
- 从候选地址中提取IP地址
- 过滤掉 127.0.0.1（本地回环）

**降级方案：**
- 如果 WebRTC 失败，使用 `window.location.hostname`
- 对于 localhost 访问，显示 "localhost"

### 路由守卫流程

```
beforeEach(to, from, next)
    │
    ├─→ to.meta.requiresGoal === false
    │   └─→ next()  // 目标页，直接通过
    │
    └─→ to.meta.requiresGoal !== false
        └─→ checkGoalForRoute()
            ├─→ hasGoal === true
            │   └─→ next()
            │
            └─→ hasGoal === false
                └─→ next({ name: 'Goal', query: { redirect: to.fullPath } })
```

---

## 常见问题

### Q1: 为什么使用 localStorage 而不是只依赖 API？

**A:** localStorage 提供：
- 快速响应（无需等待 API）
- 离线场景下的基本功能
- 减少不必要的 API 调用

### Q2: WebRTC 获取 IP 有什么限制？

**A:**
- 需要在本地网络中访问（localhost 或局域网IP）
- 某些浏览器可能需要权限
- 在 HTTPS 环境下更可靠

### Q3: 如果目标在后台被修改了怎么办？

**A:** 路由守卫会在每次导航时调用 API 验证，确保数据最新。

### Q4: 手机访问提示可以永久关闭吗？

**A:** 可以添加 `showMobileHint` 到 localStorage：
```javascript
localStorage.setItem('smartfood_hide_mobile_hint', 'true')
```

---

*文档版本: v1.0*
*生成日期: 2026-01-16*
*状态: ✅ 启动流程和手机访问指引已修复*
