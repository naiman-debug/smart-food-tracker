# 📁 目录结构说明

> 智能食物记录 App - 项目目录导航

**最后更新：** 2026-01-16

---

## 📂 根目录结构

```
智能食物记录/
│
├── 📄 README.md                       # 项目主页（从这里开始）
├── 📄 QUICK_START_AND_TEST_GUIDE.md   # 快速启动指南
├── 📄 DIRECTORY_GUIDE.md              # 本文件：目录说明
├── 📄 CHANGELOG.md                    # 版本更新日志
├── 📄 .gitignore                      # Git忽略配置
│
├── 📁 scripts/                        # 启动和Git工具脚本
├── 📁 docs/                           # 开发文档归档
├── 📁 backend/                        # 后端代码（FastAPI + Python）
├── 📁 frontend/                       # 前端代码（Vue 3 + TypeScript）
├── 📁 tools/                          # 工具和检查脚本
└── 📁 security/                       # 安全相关脚本
```

---

## 📁 详细目录说明

### 🏠 根目录文件

| 文件 | 说明 | 用途 |
|------|------|------|
| **README.md** | 项目主页 | 项目介绍、功能特性、快速开始 |
| **QUICK_START_AND_TEST_GUIDE.md** | 快速启动指南 | 5分钟快速验证和故障排除 |
| **DIRECTORY_GUIDE.md** | 目录说明 | 本文件，说明各目录用途 |
| **CHANGELOG.md** | 版本日志 | 记录每次更新的内容和日期 |

### 🚀 scripts/ - 启动和Git脚本

**用途：** 所有项目启动脚本和Git工具脚本

```
scripts/
├── start_local.bat           # 主启动脚本（完整检查）
├── start_quick.bat           # 快速启动脚本
├── start_local.sh            # Linux/Mac启动脚本
├── git_update.bat            # Git一键更新脚本
├── git_check_status.bat      # Git状态检查脚本
├── git_undo_last.bat         # Git撤销助手脚本
└── test_glm_api.ps1          # GLM API测试脚本
```

**快速操作：**
- 启动项目：`scripts\start_local.bat`
- 提交代码：`scripts\git_update.bat`
- 查看状态：`scripts\git_check_status.bat`

---

### 📚 docs/ - 开发文档归档

**用途：** 项目开发过程中产生的所有文档，按类别组织

#### docs/design/ - 设计文档

```
docs/design/
├── DESIGN_PROPOSALS.md         # 功能设计提案
├── DESIGN_SUMMARY.md           # 设计总结
├── VISUAL_PROTOTYPES.md        # UI原型设计
└── PRD_DRAFT_FOR_REVIEW.md     # 产品需求草案
```

#### docs/development/ - 开发过程记录

```
docs/development/
├── TASK_EXECUTION_SUMMARY.md         # 任务执行总结
├── SUPPLEMENTARY_TASKS_SUMMARY.md    # 补充任务总结
├── FINAL_CONFIRMATION_SUMMARY.md     # 最终确认总结
└── AI_WORK_RULE.md                   # AI工作规则
```

#### docs/fixes/ - 问题修复记录

```
docs/fixes/
├── ENCODING_FIX_SUMMARY.md               # 编码问题修复
├── DATABASE_FIX_SUMMARY.md               # 数据库修复
├── DATABASE_VERIFICATION_REPORT.md       # 数据库验证报告
├── AI_FAILURE_OPTIMIZATION_SUMMARY.md    # AI失败优化
├── STARTUP_FLOW_FIX_SUMMARY.md           # 启动流程修复
├── STARTUP_MOBILE_OPTIMIZATION_SUMMARY.md # 启动移动优化
├── FRONTEND_DEPS_FIX_SUMMARY.md          # 前端依赖修复
└── CRITICAL_FIXES_SUMMARY.md             # 关键问题修复
```

#### docs/git/ - Git工作流文档

```
docs/git/
├── GIT_WORKFLOW_GUIDE.md          # Git工作流规范
├── PROJECT_STATUS_SYNC.md         # 项目状态同步表
├── GITHUB_DEPLOYMENT_GUIDE.md     # GitHub部署指南
├── GITHUB_PUSH_EXECUTION_LOG.md   # GitHub推送执行日志
├── GITHUB_PUSH_FINAL_REPORT.md    # GitHub推送最终报告
├── FIREWALL_PUSH_REPORT.md        # 防火墙推送报告
└── TOKEN_SECURITY_GUIDE.md        # Token安全指南
```

#### docs/glm/ - GLM集成文档

```
docs/glm/
├── GLM_CONFIG.md            # GLM配置说明
├── GLM_TEST_GUIDE.md        # GLM测试指南
└── GLM_INTEGRATION_LOG.md   # GLM集成日志
```

#### docs/reports/ - 项目报告

```
docs/reports/
├── DEPLOYMENT_SUMMARY.md                # 部署总结
├── MANUAL_INSTALL_GUIDE.md              # 手动安装指南
├── BUILD_APK.md                         # APK构建指南
├── MOBILE_TEST_GUIDE.md                 # 移动端测试指南
├── MOBILE_TEST_PLAN_TEMPLATE.md         # 移动端测试计划
├── FINAL_LAUNCH_READINESS_REPORT.md     # 最终发布准备报告
└── STARTUP_AND_PRD_VERIFICATION.md      # 启动和PRD验证
```

---

### 🔧 backend/ - 后端代码

**用途：** FastAPI + Python 后端服务

```
backend/
├── app/
│   ├── main.py              # FastAPI主应用
│   ├── api/                 # API路由
│   ├── models/              # 数据模型
│   ├── services/            # 业务服务
│   ├── config/              # 配置文件
│   └── data/                # 数据文件
├── requirements.txt         # Python依赖
├── .env                     # 环境变量（不提交）
├── .env.example             # 环境变量模板
└── smart_food.db            # SQLite数据库（不提交）
```

**启动后端：**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

### 🎨 frontend/ - 前端代码

**用途：** Vue 3 + TypeScript + Vite 前端应用

```
frontend/
├── src/
│   ├── main.ts              # 应用入口
│   ├── App.vue              # 根组件
│   ├── views/               # 页面组件
│   ├── router/              # 路由配置
│   ├── api/                 # API服务
│   └── composables/         # 组合式函数
├── public/                  # 静态资源
├── package.json             # NPM依赖
├── vite.config.ts           # Vite配置
└── tsconfig.json            # TypeScript配置
```

**启动前端：**
```bash
cd frontend
npm run dev
```

---

### 🛠️ tools/ - 工具脚本

**用途：** 环境检查和辅助工具

```
tools/
└── check_environment.py     # 环境检查脚本
```

---

### 🔐 security/ - 安全脚本

**用途：** 安全相关的脚本（如Token处理）

```
security/
└── secure_token_push.ps1    # 安全Token推送脚本
```

---

## 🎯 快速导航

### 我想...

| 目标 | 操作 |
|------|------|
| **启动项目** | 运行 `scripts\start_local.bat` |
| **了解项目** | 阅读 `README.md` |
| **快速上手** | 阅读 `QUICK_START_AND_TEST_GUIDE.md` |
| **提交代码** | 运行 `scripts\git_update.bat` |
| **查看更新** | 阅读 `CHANGELOG.md` |
| **查看文档** | 进入 `docs/` 目录 |
| **修改后端** | 进入 `backend/app/` 目录 |
| **修改前端** | 进入 `frontend/src/` 目录 |

### 遇到问题...

| 问题类型 | 查看文档 |
|----------|----------|
| **启动失败** | `QUICK_START_AND_TEST_GUIDE.md` |
| **数据库问题** | `docs/fixes/DATABASE_FIX_SUMMARY.md` |
| **Git推送问题** | `docs/git/GITHUB_DEPLOYMENT_GUIDE.md` |
| **AI识别失败** | `docs/glm/GLM_TEST_GUIDE.md` |

---

## 📝 文档更新说明

### 需要添加新文档？

1. **用户文档** → 放在根目录
2. **开发文档** → 放入 `docs/` 对应子目录
3. **新脚本** → 放入 `scripts/`
4. **更新日志** → 编辑 `CHANGELOG.md`

### 文档命名规范

| 文档类型 | 命名格式 | 示例 |
|----------|----------|------|
| 功能设计 | `DESIGN_*.md` | `DESIGN_PROPOSALS.md` |
| 问题修复 | `*_FIX_SUMMARY.md` | `DATABASE_FIX_SUMMARY.md` |
| 工作流程 | `*_GUIDE.md` | `GIT_WORKFLOW_GUIDE.md` |
| 测试相关 | `*_TEST_*.md` | `GLM_TEST_GUIDE.md` |

---

## 🔗 相关链接

- **GitHub仓库：** https://github.com/naiman-debug/smart-food-tracker
- **项目主页：** `README.md`
- **快速启动：** `QUICK_START_AND_TEST_GUIDE.md`
- **版本日志：** `CHANGELOG.md`

---

*目录说明版本: v1.0*
*最后更新: 2026-01-16*
