# 智能食物记录

一个基于 Vue 3 + Python 的智能食物记录应用，帮助用户追踪饮食营养摄入。

## 项目结构

```
智能食物记录/
├── frontend/                 # Vue 3 前端应用
│   ├── src/
│   │   ├── assets/          # 静态资源
│   │   ├── components/      # 通用组件
│   │   ├── views/           # 页面视图
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # 状态管理
│   │   ├── api/             # API 接口
│   │   ├── utils/           # 工具函数
│   │   └── types/           # TypeScript 类型定义
│   ├── public/              # 公共静态文件
│   └── package.json
├── backend/                 # Python 后端服务
│   ├── app/
│   │   ├── api/             # API 路由
│   │   ├── models/          # 数据模型
│   │   ├── services/        # 业务逻辑
│   │   └── utils/           # 工具函数
│   ├── tests/               # 测试文件
│   ├── migrations/          # 数据库迁移
│   └── requirements.txt
├── docs/                    # 项目文档
└── .github/                 # GitHub Actions 配置
```

## 快速开始

### 前端
```bash
cd frontend
npm install
npm run dev
```

### 后端
```bash
cd backend
pip install -r requirements.txt
python app/main.py
```

## 技术栈

- **前端**: Vue 3 + Vite + Pinia + Vue Router
- **后端**: Python (Flask/FastAPI)
- **数据库**: PostgreSQL / SQLite
