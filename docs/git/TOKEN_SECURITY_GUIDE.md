# GitHub Personal Access Token 安全管理指南

> 智能食物记录 App - Token安全最佳实践

**文档版本：** v1.0
**创建日期：** 2026-01-16

---

## 🔐 什么是Personal Access Token (PAT)

GitHub Personal Access Token是用于替代密码的认证凭据。由于GitHub已弃用密码认证，所有Git操作都需要使用Token。

**重要特点：**
- ✅ 比密码更安全（可设置权限范围和过期时间）
- ✅ 可随时撤销
- ⚠️ 泄露后存在安全风险

---

## ✅ 安全使用原则

### 1. 最小权限原则

**仅授予必要的权限范围：**

| 权限范围 | 说明 | 本项目需要 |
|----------|------|------------|
| `repo` | 完整仓库访问（读取/写入） | ✅ 必需 |
| `workflow` | GitHub Actions操作 | ❌ 不需要 |
| `admin:org` | 组织管理 | ❌ 不需要 |
| `gist` | Gist操作 | ❌ 不需要 |
| `user` | 用户信息 | ❌ 不需要 |

**本项目只需 `repo` 权限即可完成推送。**

### 2. 定期更换Token

- **建议过期时间：** 30-90天
- **何时更换：**
  - Token已达到过期时间
  - 怀疑Token已泄露
  - 完成大型项目后

### 3. 绝不存储在代码中

**❌ 错误做法：**
```python
# 永远不要这样做！
API_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

```bash
# 也不要在脚本中硬编码
git push https://user:ghp_xxx@github.com/repo.git
```

**✅ 正确做法：**
- 使用环境变量
- 使用凭据管理器
- 使用安全脚本（如 `secure_token_push.ps1`）

---

## 🛡️ 安全存储方法

### 方法1：Git凭据管理器（推荐）

Windows已内置Git Credential Manager (GCM)：

```bash
# 配置凭据助手
git config --global credential.helper manager-core

# 首次推送时输入Token，之后自动保存
git push -u origin main
```

**优点：**
- Token加密存储在Windows凭据管理器中
- 自动处理认证
- 安全可靠

### 方法2：环境变量（临时）

```bash
# 设置临时环境变量（仅在当前会话有效）
set GITHUB_TOKEN=ghp_your_token_here

# 使用
git -c credential.helper='!f() { echo "username=naiman-debug"; echo "password=%GITHUB_TOKEN%"; }; f' push -u origin main
```

**注意：** 关闭终端后环境变量自动清除。

### 方法3：使用安全脚本

```powershell
# 运行项目提供的安全推送脚本
.\secure_token_push.ps1

# 或提供Token作为参数
.\secure_token_push.ps1 -Token "your_token_here"
```

---

## ⚠️ Token泄露应急处理

### 立即撤销泄露的Token

**步骤：**

1. **访问Token设置页面**
   ```
   https://github.com/settings/tokens
   ```

2. **找到泄露的Token**
   - 查看Token名称（如 "Smart Food Tracker"）
   - 查看最后使用时间
   - 确认是否为泄露的Token

3. **撤销Token**
   - 点击 "Delete" 或 "Revoke"
   - 确认删除

4. **生成新Token**
   - 点击 "Generate new token"
   - 重新设置权限（仅需 `repo`）
   - 复制新Token

5. **更新凭据**
   ```bash
   # 清除旧凭据
   git credential-manager erase

   # 或使用新Token重新推送
   .\secure_token_push.ps1
   ```

### 如何判断Token可能泄露

| 情况 | 风险级别 | 操作 |
|------|----------|------|
| Token出现在代码仓库中 | 🔴 严重 | 立即撤销，更换Token |
| Token在屏幕共享中暴露 | 🟡 中等 | 建议撤销，更换Token |
| Token保存在明文文件中 | 🔴 严重 | 立即撤销，更换Token |
| Token仅存储在凭据管理器 | 🟢 安全 | 无需操作 |

---

## 📋 推送后安全检查清单

### 推送成功后立即检查

- [ ] **Token不在仓库中**
  ```bash
  # 检查是否有Token被意外提交
  git grep "ghp_"
  git log --all --full-history --source -- "*token*"
  ```

- [ ] **环境变量已清除**
  ```bash
  echo %GITHUB_TOKEN%
  # 应显示：%GITHUB_TOKEN%（表示未设置）
  ```

- [ ] **凭据已安全存储**
  ```bash
  # Windows凭据管理器
  # 控制面板 → 用户账户 → 凭据管理器 → Windows凭据
  # 查找: git:https://github.com
  ```

- [ ] **脚本历史已清理**
  ```powershell
  # 清除PowerShell历史
  [Microsoft.PowerShell.PSConsoleReadLine]::ClearHistory()
  ```

---

## 🚫 永远不要做的事

### ❌ 错误操作示例

1. **将Token提交到Git仓库**
   ```bash
   # 错误！Token将被永久记录在Git历史中
   echo "TOKEN=ghp_xxx" > .env
   git add .env
   git commit -m "Add token"
   ```

2. **在聊天工具中发送Token**
   ```
   # 错误！聊天记录可能被泄露
   [Slack/Teams/微信] 这里的Token是：ghp_xxx
   ```

3. **在公开场所输入Token**
   ```
   # 错误！屏幕共享或录屏会暴露Token
   在直播/会议中输入Token
   ```

4. **将Token写入日志文件**
   ```bash
   # 错误！日志文件可能被意外共享
   echo "Using token: ghp_xxx" > debug.log
   ```

---

## ✅ 推荐的安全工作流程

### 工作流程1：使用安全脚本（本项目）

```powershell
# 1. 生成Token（仅一次）
# 访问：https://github.com/settings/tokens
# 权限：repo
# 过期：90天

# 2. 使用安全脚本推送
cd "C:\Users\Administrator\智能食物记录"
.\secure_token_push.ps1

# 3. 脚本会提示输入Token
# 4. 推送完成后，Token自动清除

# 5. 验证推送成功
# 访问：https://github.com/naiman-debug/smart-food-tracker
```

### 工作流程2：使用Git凭据管理器

```bash
# 1. 生成Token
# https://github.com/settings/tokens

# 2. 配置凭据管理器
git config --global credential.helper manager-core

# 3. 推送（首次会要求输入Token）
git push -u origin main
# 用户名：naiman-debug
# 密码：[粘贴Token]

# 4. 后续推送无需再次输入Token
```

---

## 🔍 安全审计命令

### 检查Token是否泄露到仓库

```bash
# 方法1：搜索Token格式
git grep "ghp_[a-zA-Z0-9]\{36\}"

# 方法2：搜索敏感文件
git log --all --oneline -- "*token*" "*secret*" "*password*"

# 方法3：检查环境变量文件
git grep -i token .env .env.local config/*.ini 2>/dev/null
```

### 检查凭据存储

```bash
# 列出Git凭据
git credential-manager version

# 清除所有Git凭据（如需重置）
git credential-manager erase
```

---

## 📞 安全事件响应

### 如果Token已泄露到公共仓库

**紧急步骤：**

1. **立即撤销Token**
   - 访问：https://github.com/settings/tokens
   - 找到并删除泄露的Token

2. **生成新Token**
   - 使用新的描述名（如 "Smart Food Tracker v2"）
   - 设置相同的权限范围（`repo`）

3. **从Git历史中移除Token**
   ```bash
   # 使用git-filter-repo或BFG Repo-Cleaner
   # 这会从整个Git历史中移除敏感信息

   # 简单方法：重置仓库（如果Token仅在最近提交中）
   git reset --hard HEAD~1
   git push --force
   ```

4. **通知GitHub支持**
   - 如果仓库是公开的，考虑联系GitHub支持
   - 他们可以帮助从缓存中移除敏感信息

5. **审查其他安全风险**
   - 检查是否有其他泄露的凭据
   - 审查仓库的访问权限
   - 考虑启用双因素认证（2FA）

---

## 📚 参考资源

- **GitHub官方文档：** https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
- **Token最佳实践：** https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github
- **凭据管理器：** https://github.com/GitCredentialManager/git-credential-manager

---

## ✅ 快速参考卡

### 推送Token安全检查

| 检查项 | 通过标准 |
|--------|----------|
| Token权限 | 仅 `repo` 范围 |
| Token存储 | 仅在Windows凭据管理器中 |
| 仓库中无Token | `git grep "ghp_"` 无结果 |
| 环境变量 | `%GITHUB_TOKEN%` 未设置 |
| 过期时间 | 设置为30-90天 |

### 应急命令速查

```bash
# 撤销Token（网页操作）
https://github.com/settings/tokens

# 清除本地凭据
git credential-manager erase

# 清除PowerShell历史
[Microsoft.PowerShell.PSConsoleReadLine]::ClearHistory()

# 验证Token不在仓库中
git grep "ghp_"
```

---

*文档版本: v1.0*
*创建日期: 2026-01-16*
*下次审查: 2026-04-16*
