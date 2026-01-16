# 部署摘要

> 智能食物记录 App - 本地部署完整指南

---

## 项目结构

```
智能食物记录/
├── start_local.bat              # Windows一键启动脚本
├── start_local.sh               # macOS/Linux启动脚本
├── MOBILE_TEST_GUIDE.md         # 手机测试指南
├── BUILD_APK.md                 # APK打包指南
├── DEPLOYMENT_SUMMARY.md        # 本文档
│
├── backend/                     # 后端服务
│   ├── app/
│   │   ├── api/
│   │   │   └── meal.py         # 核心API接口
│   │   ├── data/
│   │   │   └── extended_food_database.py  # 105种食物数据
│   │   ├── services/
│   │   │   ├── ai_service.py   # AI识别服务
│   │   │   └── portion_service.py  # 份量服务
│   │   └── models/
│   │       ├── visual_portion.py
│   │       ├── meal_record.py
│   │       └── daily_goal.py
│   ├── init_extended_database.py  # 数据库初始化脚本
│   ├── test_e2e.py              # 端到端测试脚本
│   ├── requirements.txt         # Python依赖
│   └── .env                     # 环境变量（需创建）
│
└── frontend/                    # 前端服务
    ├── src/
    │   ├── api/
    │   │   └── index.ts         # API服务层
    │   ├── views/
    │   │   ├── Home.vue         # 首页
    │   │   ├── Record.vue       # 拍照记录页（含备选流程）
    │   │   ├── Progress.vue     # 进度页
    │   │   └── Goal.vue         # 目标设置页
    │   └── router/
    │       └── index.ts         # 路由配置
    ├── package.json             # Node依赖
    └── vite.config.ts           # Vite配置
```

---

## 启动步骤

### 方式1：一键启动（推荐）

**Windows:**
```bash
双击运行 start_local.bat
```

**macOS/Linux:**
```bash
chmod +x start_local.sh
./start_local.sh
```

脚本会自动：
1. 检查Python和Node.js环境
2. 安装依赖
3. 初始化数据库（105种食物）
4. 启动后端服务（端口8000）
5. 启动前端服务（端口5173）

### 方式2：手动启动

**步骤1：配置环境变量**

```bash
cd backend
```

创建 `.env` 文件：
```bash
# GLM API配置（必填）
GLM_API_KEY=your_glm_api_key_here

# 环境模式
ENV_MODE=production
```

**步骤2：安装后端依赖**

```bash
pip install -r requirements.txt
```

**步骤3：初始化数据库**

```bash
python init_extended_database.py
```

预期输出：
```
✓ 数据库表创建完成
✓ 插入 105 条新记录
食物种类: 105
份量选项: 280
```

**步骤4：启动后端服务**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

预期输出：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**步骤5：启动前端服务（新开终端）**

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

预期输出：
```
VITE ready in xxx ms
➜  Local:   http://localhost:5173/
➜  Network: http://192.168.x.x:5173/
```

---

## 手机访问

### 获取电脑IP地址

**Windows:**
```bash
ipconfig
# 查看 "IPv4 地址"，如 192.168.1.100
```

**macOS:**
```bash
ipconfig getifaddr en0
```

**Linux:**
```bash
hostname -I
```

### 手机访问URL

在手机浏览器中输入：

```
http://[你的电脑IP]:5173
```

**示例：**
```
http://192.168.1.100:5173
```

### 重要提示

1. **手机和电脑必须连接同一WiFi**
2. **确保电脑防火墙允许连接**
3. **首次加载可能需要5-10秒**

---

## 预期效果

### 电脑浏览器访问

访问 `http://localhost:5173` 应该看到：

1. **首页**
   - 显示今日热量余额
   - 显示"可以吃这些"智能建议区域
   - 显示3-5个推荐食物

2. **拍照记录页**
   - 拍照按钮
   - AI识别成功 → 显示食物和份量选项
   - AI识别失败 → 显示食物分类选择界面

3. **进度页**
   - 显示累计热量缺口
   - 显示估算减脂重量
   - 显示每日数据曲线

### 手机浏览器访问

与电脑浏览器相同功能，支持触摸操作。

---

## 故障排除

### 问题1：后端启动失败

**症状：**
```
Error: GLM_API_KEY not found
```

**解决方案：**
1. 检查 `backend/.env` 文件是否存在
2. 确认 `GLM_API_KEY` 已正确填写
3. 重启后端服务

### 问题2：数据库初始化失败

**症状：**
```
Error: no module named 'xxx'
```

**解决方案：**
```bash
pip install -r requirements.txt
```

### 问题3：手机无法访问

**症状：**
- "无法访问此网站"
- "连接超时"

**解决方案：**

**Windows防火墙：**
1. Windows安全中心 → 防火墙
2. 允许应用通过防火墙
3. 勾选 Python 的专用和公用

**macOS防火墙：**
1. 系统偏好设置 → 安全性与隐私
2. 防火墙选项 → 允许传入连接

### 问题4：前端API请求失败

**症状：**
- 网络请求返回404/500错误

**检查清单：**
- [ ] 后端服务是否正常运行（访问 http://localhost:8000/docs）
- [ ] API地址配置是否正确（`frontend/src/api/index.ts`）
- [ ] 数据库是否已初始化

### 问题5：图片识别失败

**症状：**
- 选择图片后显示错误

**解决方案：**
1. 检查 `GLM_API_KEY` 是否有效
2. 查看后端日志确认错误原因
3. 识别失败会自动显示食物选择界面（正常行为）

---

## 端口占用问题

### 检查端口占用

**Windows:**
```bash
netstat -ano | findstr :8000
netstat -ano | findstr :5173
```

**macOS/Linux:**
```bash
lsof -i :8000
lsof -i :5173
```

### 解决方案

**方法1：结束占用进程**
```bash
# Windows
taskkill /PID [进程ID] /F

# macOS/Linux
kill -9 [进程ID]
```

**方法2：更换端口**
```bash
# 后端更换端口
uvicorn app.main:app --host 0.0.0.0 --port 8001

# 前端更换端口
npm run dev -- --host 0.0.0.0 --port 5174
```

---

## API文档

启动后端服务后，访问以下地址查看完整API文档：

```
http://localhost:8000/docs
```

包含接口：
- `POST /api/analyze` - 单食物识别
- `POST /api/analyze-multi` - 多食物识别
- `GET /api/balance` - 获取今日余额
- `POST /api/records` - 创建记录
- `GET /api/food-categories` - 获取食物分类
- `GET /api/foods-by-category/{key}` - 获取分类下的食物
- `GET /api/food-search` - 搜索食物
- `GET /api/portions/{food_name}` - 获取食物份量

---

## 数据验证

### 验证数据库初始化

访问 `http://localhost:8000/docs`，尝试：

1. `GET /api/food-categories` - 应返回10个分类
2. `GET /api/foods-by-category/meat` - 应返回肉类食物列表
3. `GET /api/food-search?q=鸡` - 应返回含"鸡"的食物

### 运行端到端测试

```bash
cd backend
python test_e2e.py
```

预期输出：
```
✓ 测试1：API健康检查
✓ 测试2：食物分类API
✓ 测试3：按分类获取食物API
✓ 测试4：食物搜索API
✓ 测试5：按食物名称获取份量API
✓ 测试6：AI识别失败备选流程

✓ 所有测试通过！
```

---

## 生产环境部署

### 后端部署建议

1. 使用云服务器（阿里云、腾讯云）
2. 配置域名和SSL证书
3. 使用 Gunicorn + Nginx 部署

### 前端部署建议

1. 构建静态文件：`npm run build`
2. 部署到 CDN 或 Nginx 静态服务
3. 或打包为 APK（参考 BUILD_APK.md）

---

## 文件路径汇总

### 启动脚本

| 文件 | 说明 |
|------|------|
| `start_local.bat` | Windows一键启动脚本 |
| `start_local.sh` | macOS/Linux启动脚本 |

### 文档

| 文件 | 说明 |
|------|------|
| `MOBILE_TEST_GUIDE.md` | 手机测试指南 |
| `BUILD_APK.md` | APK打包指南 |
| `DEPLOYMENT_SUMMARY.md` | 本文档 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `backend/.env` | 后端环境变量（需创建） |
| `frontend/src/api/index.ts` | 前端API配置 |

---

*文档版本: v1.0*
*生成日期: 2026-01-16*
*状态: ✅ 上线就绪*
