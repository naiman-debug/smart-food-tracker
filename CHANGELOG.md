# 📋 更新日志 (Changelog)

> 智能食物记录 App - 版本更新记录

**项目名称：** 智能食物记录 (Smart Food Tracker)
**仓库地址：** https://github.com/naiman-debug/smart-food-tracker

---

## 📌 版本说明

本文档记录项目的所有重要变更。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，

版本号格式：`主版本.次版本.修订版本`

---

## [Unreleased]

### 待发布

- ⬜ 用户测试反馈修复
- ⬜ 性能优化
- ⬜ 新功能开发

---

## [1.1.0] - 2026-01-16

### 新增 (Added)

- ✨ **项目结构重组**
  - 添加 `scripts/` 目录 - 所有启动和Git脚本
  - 添加 `docs/` 目录 - 开发文档归档
  - 添加 `tools/` 目录 - 工具脚本
  - 添加 `security/` 目录 - 安全相关脚本

- 📚 **新增文档**
  - `DIRECTORY_GUIDE.md` - 目录结构说明
  - `CHANGELOG.md` - 版本更新日志（本文件）
  - `GIT_WORKFLOW_GUIDE.md` - Git工作流规范
  - `PROJECT_STATUS_SYNC.md` - 项目状态同步表
  - `TOKEN_SECURITY_GUIDE.md` - Token安全管理指南

- 🔧 **新增工具脚本**
  - `git_update.bat` - 一键Git更新脚本
  - `git_check_status.bat` - Git状态检查脚本
  - `git_undo_last.bat` - Git撤销助手脚本

### 优化 (Changed)

- 🗂️ **文件组织**
  - 将30+个散落的文档文件按类别整理到 `docs/` 目录
  - 脚本文件统一移至 `scripts/` 目录
  - 提升项目可维护性

### 修复 (Fixed)

- 🐛 修复根目录文件混乱问题
- 🐛 提升项目结构清晰度

### 文档 (Documentation)

- 📖 添加完整的目录导航说明
- 📖 更新项目结构文档

---

## [1.0.0] - 2026-01-16

### 新增 (Added)

- ✨ **核心功能**
  - 🎯 目标设置 - 性别、年龄、身高、体重、减脂目标
  - 📷 食物拍照 - AI识别食物类型
  - 📏 份量选择 - 视觉化份量描述（如"掌心大小"）
  - 📊 今日余额 - 热量和蛋白质实时追踪
  - 🧠 智能建议 - AI推荐适合的食物
  - 📈 进度统计 - 周/月/全部趋势图表
  - 📱 手机访问 - 局域网内手机访问支持

- 🎨 **前端功能** (Vue 3 + TypeScript)
  - 响应式设计，支持手机和桌面
  - 路由守卫 - 强制目标设置流程
  - 表单持久化 - localStorage自动保存
  - 错误处理 - 友好的错误提示
  - 超时机制 - API请求5秒超时
  - 降级策略 - 后端故障时使用缓存数据

- 🔧 **后端功能** (FastAPI + Python)
  - RESTful API设计
  - SQLite数据库存储
  - GLM-4 AI模型集成（食物识别）
  - 视觉份量数据库
  - 扩展食物数据库（100+种食物）

- 📚 **文档体系**
  - `README.md` - 项目主页和功能介绍
  - `QUICK_START_AND_TEST_GUIDE.md` - 快速启动和验证
  - `CRITICAL_FIXES_SUMMARY.md` - 关键问题修复记录
  - `MOBILE_TEST_PLAN_TEMPLATE.md` - 移动端测试计划

- 🚀 **启动脚本**
  - `start_local.bat` - 完整启动脚本（含依赖检查）
  - `start_quick.bat` - 快速启动脚本
  - `start_local.sh` - Linux/Mac启动脚本

### 优化 (Changed)

- ⚡ **性能优化**
  - API调用超时控制
  - localStorage缓存策略
  - 后台验证机制

- 🔒 **安全优化**
  - 环境变量分离（`.env`文件）
  - `.gitignore` 配置
  - Token安全使用指南

### 修复 (Fixed)

- 🐛 **前端空白页面问题**
  - 添加3秒路由守卫超时
  - 实现API调用5秒超时
  - 自动降级到localStorage

- 🐛 **启动脚本可靠性**
  - 智能依赖检查
  - 数据库存在性检查
  - 端口占用检测

- 🐛 **编码问题**
  - 统一使用UTF-8编码
  - 修复中文显示问题

---

## 🔍 版本对比

| 版本 | 发布日期 | 主要变更 | 文档数 | 提交数 |
|------|----------|----------|--------|--------|
| 1.1.0 | 2026-01-16 | 项目结构重组 | 35+ | 3 |
| 1.0.0 | 2026-01-16 | 初始版本 | 30+ | 2 |

---

## 📊 统计信息

### 代码统计

| 类别 | 文件数 | 代码行数 |
|------|--------|----------|
| 后端代码 | 25+ | ~8,000 |
| 前端代码 | 15+ | ~5,000 |
| 脚本工具 | 8 | ~1,500 |
| 文档 | 35+ | ~10,000 |
| **总计** | **83+** | **~24,500** |

### 功能完成度

| 模块 | 完成度 | 说明 |
|------|--------|------|
| 目标设置 | ✅ 100% | 完整实现 |
| 食物记录 | ✅ 100% | 含AI识别 |
| 份量选择 | ✅ 100% | 视觉化描述 |
| 今日余额 | ✅ 100% | 实时追踪 |
| 智能建议 | ✅ 100% | AI推荐 |
| 进度统计 | ✅ 100% | 图表展示 |
| 手机访问 | ✅ 100% | 局域网支持 |

---

## 🔮 未来计划

### v1.2.0 - 计划中

- ⬜ 用户数据导出功能
- ⬜ 多语言支持（英文）
- ⬜ 深色模式
- ⬜ 离线模式支持

### v1.3.0 - 计划中

- ⬜ 社交分享功能
- ⬜ 饮食建议AI优化
- ⬜ 运动数据集成
- ⬜ 云端数据同步

### v2.0.0 - 长期计划

- ⬜ 移动端原生应用
- ⬜ 语音记录功能
- ⬜ 营养师咨询服务
- ⬜ 社区功能

---

## 📞 反馈与支持

### 问题反馈

- 🐛 **Bug报告：** https://github.com/naiman-debug/smart-food-tracker/issues
- 💡 **功能建议：** https://github.com/naiman-debug/smart-food-tracker/issues
- 📧 **邮件联系：** naiman.zc@gmail.com

### 更新订阅

- 🌟 **Watch仓库：** https://github.com/naiman-debug/smart-food-tracker
- 📢 **关注发布：** https://github.com/naiman-debug/smart-food-tracker/releases

---

## 📝 贡献指南

欢迎贡献代码、文档或测试结果！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

详见：`docs/git/GIT_WORKFLOW_GUIDE.md`

---

*本文档遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范*
*最后更新：2026-01-16*
