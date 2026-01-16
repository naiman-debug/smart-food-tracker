# 智能食物记录项目 Git更新规范

> Smart Food Tracker - Git工作流与版本管理规范

**项目名称：** 智能食物记录 (Smart Food Tracker)
**文档版本：** v1.0
**创建日期：** 2026-01-16
**仓库地址：** https://github.com/naiman-debug/smart-food-tracker

---

## 📋 一、项目Git状态概览

### 当前配置

| 项目 | 配置 |
|------|------|
| **主分支** | `main`（稳定可部署版本） |
| **远程仓库** | `origin` → `https://github.com/naiman-debug/smart-food-tracker.git` |
| **开发阶段** | 本地部署测试阶段 |
| **更新频率** | 按测试里程碑更新 |
| **分支策略** | 简化策略（暂仅使用main分支） |

### 项目结构

```
智能食物记录/
├── backend/          # FastAPI后端
├── frontend/         # Vue 3前端
├── start_local.bat   # 主启动脚本
├── start_quick.bat   # 快速启动脚本
├── .gitignore        # Git忽略规则
└── *.md              # 项目文档
```

---

## 🚀 二、更新触发条件（何时提交代码）

### ✅ 应该提交的更改

| 触发条件 | 说明 | 提交前检查 |
|----------|------|------------|
| **功能完成** | 完成新功能或模块 | ✅ 功能测试通过 |
| **Bug修复** | 修复测试问题 | ✅ 问题已验证解决 |
| **文档更新** | 重要文档/指南更新 | ✅ 内容准确无误 |
| **配置变更** | 影响运行的配置修改 | ✅ 配置已测试 |
| **测试添加** | 添加自动化测试 | ✅ 测试可正常运行 |

### ❌ 不应提交的内容

| 文件类型 | 示例 | 处理方式 |
|----------|------|----------|
| **临时文件** | `*.tmp`, `*.temp`, `*.bak` | 已在.gitignore中 |
| **个人配置** | `.env.local`, 个人IDE配置 | 使用.env.example |
| **大文件** | `*.db`, `node_modules/`, `venv/` | 已在.gitignore中 |
| **敏感信息** | API密钥、密码 | 使用.env文件 |
| **日志文件** | `*.log`, `logs/` | 已在.gitignore中 |

### 📝 提交前自检清单

```
□ 代码是否测试通过？
□ 是否添加了必要的注释？
□ 是否更新了相关文档？
□ .gitignore是否正确配置？
□ 敏感信息是否已排除？
□ 提交消息是否清晰准确？
```

---

## 💬 三、提交消息规范

### 消息格式

```
<类型>: <简短描述>

[可选的详细描述]

[可选的关联问题]
```

### 类型前缀定义

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加食物拍照识别功能` |
| `fix` | Bug修复 | `fix: 修复手机访问IP获取问题` |
| `docs` | 文档更新 | `docs: 更新用户测试指南` |
| `test` | 测试相关 | `test: 添加API单元测试` |
| `chore` | 维护任务 | `chore: 更新项目依赖版本` |
| `refactor` | 代码重构 | `refactor: 优化前端组件结构` |
| `style` | 代码风格 | `style: 统一代码缩进格式` |
| `perf` | 性能优化 | `perf: 优化数据库查询性能` |

### 提交消息示例

#### 好的提交消息

```bash
# 简洁明了
git commit -m "feat: 添加AI食物识别失败时的手动选择功能"

# 详细说明
git commit -m "fix: 修复路由守卫超时导致的空白页面问题

问题：后端未启动时，路由守卫无限等待API响应
解决：添加3秒超时机制，自动降级到localStorage
影响：提升了用户体验，避免页面卡死"
```

#### 不好的提交消息

```bash
# 太模糊
git commit -m "更新代码"

# 太长
git commit -m "修复了前端页面的一个问题，然后添加了一些新的功能，还更新了文档"

# 无意义
git commit -m "随便提交一下"
```

---

## 🔄 四、更新操作流程（四步法）

### 标准更新流程

```bash
# ============================================
# 步骤1：检查当前状态
# ============================================
git status

# 查看哪些文件已修改或新增
# 确认没有意外文件被追踪

# ============================================
# 步骤2：添加要提交的文件
# ============================================
# 添加所有更改
git add .

# 或选择性添加特定文件
git add backend/app/main.py
git add frontend/src/views/Home.vue

# ============================================
# 步骤3：提交更改
# ============================================
git commit -m "类型: 简要描述"

# 示例：
# git commit -m "feat: 添加用户头像上传功能"
# git commit -m "fix: 修复登录页面响应问题"

# ============================================
# 步骤4：推送到GitHub
# ============================================
git push origin main

# 如果遇到冲突，先拉取远程更改
git pull origin main --rebase
git push origin main
```

### 快速更新（使用脚本）

```bash
# 一键更新脚本
git_update.bat

# 脚本会：
# 1. 显示当前状态
# 2. 提示输入提交消息
# 3. 自动执行add、commit、push
```

---

## 🌳 五、分支管理策略

### 当前策略：简化单分支模式

```
main (主分支)
    │
    ├── 始终保持稳定可部署
    ├── 每次提交都应测试通过
    └── 直接推送到main（暂无开发分支）
```

### 未来扩展：功能分支模式（可选）

```
main (主分支)
    │
    └── feat/add-user-avatar (功能分支)
            │
            ├── 开发新功能
            ├── 测试验证
            └── 合并到main
```

### 分支命名规范

| 分支类型 | 命名格式 | 示例 |
|----------|----------|------|
| 功能分支 | `feat/<功能名>` | `feat/user-avatar` |
| 修复分支 | `fix/<问题描述>` | `fix/login-bug` |
| 发布分支 | `release/<版本号>` | `release/v1.1.0` |

### 何时创建新分支

- ✅ 开发大型新功能（预计超过1天）
- ✅ 实验性功能（可能不会合并）
- ✅ 需要多人协作
- ❌ 小型Bug修复（直接在main修复）
- ❌ 文档更新（直接在main更新）

---

## ⚠️ 六、特殊情况处理

### 6.1 推送冲突解决

**症状：**
```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/...'
```

**解决方案：**

```bash
# 方案A：拉取并合并
git pull origin main
# 解决可能的冲突后
git push origin main

# 方案B：拉取并变基（保持提交历史清晰）
git pull origin main --rebase
git push origin main

# 方案C：强制推送（危险！仅确认本地正确时使用）
git push origin main --force
```

### 6.2 大文件处理

**问题：** Git警告文件过大（>100MB）

**解决方案：**

```bash
# 检查大文件
git rev-list --objects --all |
git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
awk '/^blob/ {print substr($0,6)}' |
sort -nk2 |
tail -10

# 从历史中移除大文件
git filter-branch --tree-filter 'rm -rf path/to/large/file' HEAD

# 或使用BFG Repo-Cleaner（更快）
bfg --delete-files large-file.zip
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**预防：** 在`.gitignore`中添加大文件模式

```gitignore
# 数据库文件
*.db
*.sqlite
*.sqlite3

# 依赖包
node_modules/
venv/

# 日志文件
*.log
logs/

# 临时文件
*.tmp
temp/
```

### 6.3 敏感信息泄露处理

**问题：** 意外提交了API密钥或密码

**紧急处理：**

```bash
# 1. 立即撤销敏感信息提交
git revert HEAD

# 2. 或从历史中完全删除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all

# 3. 强制推送（⚠️ 会覆盖远程历史）
git push origin main --force

# 4. 通知所有协作者重新克隆仓库
```

**预防措施：**

```bash
# 提交前检查敏感信息
git diff --cached | grep -i "password\|token\|api_key\|secret"

# 或使用git-secrets工具
git secrets --install
git secrets --register-aws
```

### 6.4 撤销错误提交

#### 撤销最近的提交（保留更改）

```bash
git reset --soft HEAD~1
# 文件保留在暂存区，可重新编辑

git reset --mixed HEAD~1
# 文件保留在工作区，未暂存

git reset --hard HEAD~1
# ⚠️ 完全删除提交和更改
```

#### 撤销已推送的提交

```bash
# 创建新提交来撤销（推荐）
git revert HEAD
git push origin main

# 或使用回滚脚本
git_undo_last.bat
```

---

## 📊 七、提交历史查看

### 查看提交历史

```bash
# 简洁查看
git log --oneline -10

# 详细查看
git log -p -2

# 按作者查看
git log --author="Naiman.zc"

# 查看某个文件的修改历史
git log --follow -- path/to/file

# 图形化查看
git log --graph --oneline --all
```

### 查看文件差异

```bash
# 查看工作区与暂存区差异
git diff

# 查看暂存区与上次提交差异
git diff --staged

# 查看两次提交之间的差异
git diff commit1 commit2

# 查看某个文件的修改
git diff path/to/file
```

---

## 🛠️ 八、辅助工具使用

### 8.1 状态检查脚本

```bash
git_check_status.bat
```

**功能：**
- 快速查看当前更改状态
- 显示已修改文件列表
- 显示未跟踪文件列表
- 提供下一步操作建议

### 8.2 一键更新脚本

```bash
git_update.bat
```

**功能：**
- 交互式提交消息输入
- 自动执行add、commit、push
- 推送前显示将要更改的文件
- 操作失败时提供错误提示

### 8.3 回滚助手脚本

```bash
git_undo_last.bat
```

**功能：**
- 安全地撤销最后一次提交
- 提供撤销选项选择
- 保护重要的提交不被误删
- 确认后执行撤销操作

---

## 📝 九、团队协作规范

### 代码审查检查点

```
□ 代码符合项目风格
□ 没有引入新的Bug
□ 添加了必要的测试
□ 更新了相关文档
□ 没有硬编码敏感信息
□ 提交消息清晰准确
```

### 更新前同步

```bash
# 每次开始工作前先同步
git pull origin main

# 查看远程有哪些新提交
git fetch origin
git log HEAD..origin/main
```

---

## 🎯 十、最佳实践总结

### DO ✅

- ✅ 提交前测试代码
- ✅ 写清晰的提交消息
- ✅ 频繁提交、小步快跑
- ✅ 定期推送到远程
- ✅ 使用.gitignore排除临时文件
- ✅ 提交前检查敏感信息

### DON'T ❌

- ❌ 提交未测试的代码
- ❌ 写模糊的提交消息
- ❌ 将大文件提交到Git
- ❌ 提交敏感信息
- ❌ 强制推送（除非绝对必要）
- ❌ 提交编译后的文件

---

## 📞 十一、问题排查

### 常见问题速查

| 问题 | 解决方案 |
|------|----------|
| 推送被拒绝 | `git pull origin main` 后再推送 |
| 找不到命令 | 检查Git是否安装：`git --version` |
| 认证失败 | 更新Personal Access Token |
| 提交太慢 | 检查是否有大文件 |
| 冲突无法解决 | 使用`git mergetool`或手动编辑 |

---

## 📚 十二、相关资源

- **Git官方文档：** https://git-scm.com/doc
- **GitHub帮助：** https://docs.github.com/
- **项目仓库：** https://github.com/naiman-debug/smart-food-tracker
- **.gitignore模板：** https://github.com/github/gitignore

---

*规范版本: v1.0*
*生效日期: 2026-01-16*
*下次审查: 2026-04-16*
