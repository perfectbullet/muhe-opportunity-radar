# 📁 项目文件结构说明

## 完整目录树

```
muhe-opportunity-radar/
│
├── 📱 前端相关
│   ├── frontend/                         # Vue3 前端工程
│   │   ├── src/
│   │   │   ├── main.ts                  # 应用入口
│   │   │   ├── App.vue                  # 根组件
│   │   │   ├── style.css                # 全局样式
│   │   │   ├── router/                  # 路由配置
│   │   │   │   └── index.ts
│   │   │   ├── views/                   # 页面组件
│   │   │   │   ├── SingleAnalysis.vue  # 单一视角分析
│   │   │   │   ├── MultiComparison.vue # 多视角对比
│   │   │   │   ├── HistoryRecords.vue  # 历史记录
│   │   │   │   └── Statistics.vue      # 统计信息
│   │   │   ├── components/              # 可复用组件
│   │   │   ├── api/                     # API 客户端
│   │   │   │   ├── client.ts           # Axios 客户端
│   │   │   │   ├── analysis.ts         # 分析 API
│   │   │   │   ├── records.ts          # 记录 API
│   │   │   │   └── investors.ts        # 投资者 API
│   │   │   ├── types/                   # TypeScript 类型
│   │   │   │   └── api.ts
│   │   │   ├── stores/                  # Pinia 状态管理
│   │   │   └── utils/                   # 工具函数
│   │   ├── public/                      # 静态资源
│   │   ├── index.html                   # HTML 模板
│   │   ├── package.json                 # npm 依赖
│   │   ├── vite.config.ts              # Vite 配置
│   │   ├── tsconfig.json               # TypeScript 配置
│   │   ├── tailwind.config.js          # TailwindCSS 配置
│   │   └── postcss.config.js           # PostCSS 配置
│   │
│   └── app.py                           # 🔄 Gradio 应用（保留）
│
├── 🔌 后端相关
│   ├── api/                             # FastAPI 后端
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI 应用入口
│   │   ├── models/                      # Pydantic 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── requests.py             # 请求模型
│   │   │   └── responses.py            # 响应模型
│   │   ├── routers/                     # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py             # 分析接口
│   │   │   ├── records.py              # 历史记录接口
│   │   │   └── investors.py            # 投资者接口
│   │   └── services/                    # 业务逻辑层
│   │       ├── __init__.py
│   │       ├── analysis_service.py     # 分析服务
│   │       ├── record_service.py       # 记录服务
│   │       └── investor_service.py     # 投资者服务
│   │
│   ├── analysis/                        # 核心分析模块
│   │   ├── __init__.py
│   │   ├── investor_profiles.py        # 投资者画像管理
│   │   └── perspective_analyzer.py     # 多视角分析引擎
│   │
│   └── storage/                         # 数据存储模块
│       ├── __init__.py
│       └── db_manager.py                # MongoDB 管理器
│
├── 📊 数据相关
│   └── data/
│       ├── investor_profiles.json       # 投资者配置数据
│       └── (其他数据文件)
│
├── 📚 文档相关
│   └── docs/
│       ├── vue3_migration_guide.md      # Vue3 迁移实施指南（详细）
│       ├── copilot_prompts.md           # Copilot 提示词模板库
│       ├── MIGRATION_COMPLETED.md       # 迁移完成总结
│       ├── gradio_guide.md              # Gradio 使用指南
│       ├── gradio_features.md
│       ├── mongodb_integration.md
│       └── multi_perspective_guide.md
│
├── 🧪 测试相关
│   └── scripts/
│       ├── test_db_integration.py
│       ├── test_gradio_app.py
│       ├── test_mongodb.py
│       └── test_multi_perspective.py
│
├── 🐳 部署相关
│   ├── Dockerfile.api                   # FastAPI 后端镜像
│   ├── Dockerfile.frontend              # Vue3 前端镜像
│   ├── docker-compose.yml               # 容器编排配置
│   └── nginx.conf                       # Nginx 反向代理配置
│
├── 🔧 配置文件
│   ├── .env.example                     # 环境变量模板
│   ├── requirements.txt                 # Python 依赖
│   ├── .gitignore
│   └── __pycache__/                     # Python 缓存
│
├── 🚀 启动脚本
│   ├── start.bat                        # 原 Gradio 启动（Windows）
│   ├── start.sh                         # 原 Gradio 启动（Linux/Mac）
│   ├── start_new.bat                    # 🆕 多模式启动（Windows）
│   └── start_new.sh                     # 🆕 多模式启动（Linux/Mac）
│
├── 📖 README 文档
│   ├── README.md                        # 主说明文档
│   ├── QUICKSTART.md                    # Gradio 快速开始
│   └── QUICKSTART_VUE3.md              # 🆕 Vue3 快速开始
│
└── 📝 其他
    ├── quick_start.py
    └── 重要的投资者.txt
```

---

## 目录说明

### 🎨 前端工程 (`frontend/`)

Vue3 + TypeScript 单页应用（SPA），使用 Vite 构建。

**关键文件：**
- `src/main.ts` - 应用入口，注册插件（Vue Router、Pinia、Naive UI）
- `src/App.vue` - 根组件，配置深色主题
- `src/router/index.ts` - 路由配置，4个主要页面
- `src/views/` - 页面组件（单一视角、多视角、历史、统计）
- `src/api/` - API 调用封装，统一错误处理
- `vite.config.ts` - Vite 配置，包含 API 代理设置

**技术栈：**
- **构建工具**: Vite 5.0
- **UI 框架**: Naive UI 2.38 (深色主题)
- **可视化**: ECharts 5.4
- **CSS**: TailwindCSS 3.4
- **状态管理**: Pinia 2.1
- **路由**: Vue Router 4.2

### 🔌 后端 API (`api/`)

FastAPI 现代 Web 框架，提供 RESTful API。

**关键文件：**
- `main.py` - FastAPI 应用入口
  - CORS 配置
  - 路由注册
  - 全局异常处理
  - 健康检查端点

- `routers/` - API 路由层
  - `analysis.py` - 分析接口（单一、对比、流式）
  - `records.py` - 历史记录接口（列表、详情、搜索、统计）
  - `investors.py` - 投资者接口（列表、详情）

- `services/` - 业务逻辑层
  - `analysis_service.py` - 封装 PerspectiveAnalyzer
  - `record_service.py` - 封装 AnalysisRecordManager
  - `investor_service.py` - 封装 InvestorProfileManager

- `models/` - Pydantic 数据模型
  - `requests.py` - 请求验证模型
  - `responses.py` - 响应格式模型

**设计模式：**
- 三层架构（Router → Service → Data）
- 依赖注入（单例 Service）
- 统一响应格式
- 异步编程（async/await）

### 💾 核心业务逻辑

**`analysis/` - 分析模块**
- `investor_profiles.py` - 管理 10 位投资大师画像
- `perspective_analyzer.py` - 多视角分析引擎，调用 LLM

**`storage/` - 存储模块**
- `db_manager.py` - MongoDB CRUD 操作
  - 保存分析记录
  - 查询历史记录
  - 统计信息生成

**`data/` - 数据文件**
- `investor_profiles.json` - 投资者配置（JSON）
  - 10 位投资大师的详细画像
  - 投资哲学、决策标准、分析焦点

### 📚 文档系统 (`docs/`)

**核心文档：**
1. **vue3_migration_guide.md** - 完整实施指南（9000+ 字）
   - 架构设计说明
   - API 接口文档
   - 技术栈详解
   - 开发最佳实践
   - 常见问题解答

2. **copilot_prompts.md** - Copilot 提示词模板库
   - 后端开发模板
   - 前端开发模板
   - 全栈功能模板
   - DevOps 模板

3. **MIGRATION_COMPLETED.md** - 迁移完成总结
   - 已完成工作清单
   - 新增文件列表
   - 快速启动指南

**历史文档：**
- Gradio 相关文档（保留作为参考）
- MongoDB 集成文档
- 多视角分析指南

### 🐳 Docker 部署

**镜像构建：**
- `Dockerfile.api` - Python 后端镜像
  - 基于 python:3.10-slim
  - 多阶段构建（优化体积）
  - 非 root 用户运行

- `Dockerfile.frontend` - Node.js 前端镜像
  - 构建阶段：node:18-alpine
  - 运行阶段：nginx:alpine
  - 体积 < 50MB

**容器编排：**
- `docker-compose.yml` - 定义 4 个服务
  - `mongodb` - 数据库（数据持久化）
  - `api` - FastAPI 后端
  - `frontend` - Vue3 前端 + Nginx
  - `gradio` - Gradio 应用（备用）

- `nginx.conf` - Nginx 配置
  - 前端静态文件服务
  - API 反向代理 (`/api` → `http://api:8000`)
  - SSE 流式输出支持（禁用缓冲）
  - Gzip 压缩

### 🚀 启动脚本

**新启动脚本（推荐）：**
- `start_new.bat` / `start_new.sh`
  - 多模式选择：
    1. 仅后端
    2. 仅前端
    3. 同时启动
    4. Gradio 备用
    5. Docker 部署
  - 自动检查 `.env` 文件
  - 友好的交互式菜单

**原启动脚本（保留）：**
- `start.bat` / `start.sh`
  - 直接启动 Gradio 应用

### 🔧 配置文件

**环境变量：**
- `.env.example` - 配置模板
  - LLM API 密钥
  - MongoDB 连接
  - Tushare Token
  - API 配置

**Python 依赖：**
- `requirements.txt`
  - FastAPI + Uvicorn（新增）
  - LangChain 系列
  - MongoDB 驱动
  - Gradio（保留）

**前端配置：**
- `frontend/package.json` - npm 依赖
- `frontend/vite.config.ts` - Vite 配置（代理、别名）
- `frontend/tsconfig.json` - TypeScript 配置

---

## 文件数量统计

```
总计文件数：约 80+ 个

分类统计：
- 前端源码：30+ 个 (.vue, .ts, .css)
- 后端源码：20+ 个 (.py)
- 配置文件：15+ 个 (.json, .yml, .conf)
- 文档文件：10+ 个 (.md)
- 脚本文件：5+ 个 (.bat, .sh)
```

---

## 新增文件列表（本次迁移）

### 后端 (10 个文件)
```
api/main.py
api/__init__.py
api/models/__init__.py
api/models/requests.py
api/models/responses.py
api/routers/__init__.py
api/routers/analysis.py
api/routers/records.py
api/routers/investors.py
api/services/__init__.py
api/services/analysis_service.py
api/services/record_service.py
api/services/investor_service.py
```

### 前端 (20+ 个文件)
```
frontend/package.json
frontend/vite.config.ts
frontend/tsconfig.json
frontend/tailwind.config.js
frontend/postcss.config.js
frontend/index.html
frontend/src/main.ts
frontend/src/App.vue
frontend/src/style.css
frontend/src/router/index.ts
frontend/src/views/SingleAnalysis.vue
frontend/src/views/MultiComparison.vue
frontend/src/views/HistoryRecords.vue
frontend/src/views/Statistics.vue
frontend/src/api/client.ts
frontend/src/api/analysis.ts
frontend/src/api/records.ts
frontend/src/api/investors.ts
frontend/src/api/index.ts
frontend/src/types/api.ts
frontend/.env.example
```

### Docker 和配置 (5 个文件)
```
Dockerfile.api
Dockerfile.frontend
docker-compose.yml
nginx.conf
.env.example
```

### 文档 (3 个文件)
```
docs/vue3_migration_guide.md
docs/copilot_prompts.md
docs/MIGRATION_COMPLETED.md
QUICKSTART_VUE3.md
```

### 启动脚本 (2 个文件)
```
start_new.bat
start_new.sh
```

**总计新增：40+ 个文件**

---

## 目录大小估算

```
frontend/           # ~10-20 MB (含 node_modules 约 200 MB)
api/                # ~1 MB
analysis/           # ~500 KB
storage/            # ~200 KB
data/               # ~500 KB
docs/               # ~1 MB
scripts/            # ~100 KB
```

---

## 依赖项统计

### Python 依赖（requirements.txt）
- 总计：约 20 个包
- 核心依赖：
  - fastapi, uvicorn（新增）
  - langchain 系列（5个包）
  - gradio, streamlit（保留）
  - pymongo, chromadb
  - pandas, scrapy

### Node.js 依赖（package.json）
- 总计：约 30 个包
- 生产依赖：10 个
- 开发依赖：20 个
- node_modules 大小：约 200 MB

---

## 使用频率

### 核心文件（高频使用）
- `api/main.py` - FastAPI 入口
- `frontend/src/views/*.vue` - 前端页面
- `analysis/perspective_analyzer.py` - 分析引擎
- `storage/db_manager.py` - 数据库管理
- `data/investor_profiles.json` - 投资者配置

### 配置文件（中频使用）
- `.env` - 环境变量
- `docker-compose.yml` - 容器配置
- `vite.config.ts` - 前端配置

### 文档文件（低频查阅）
- `docs/*.md` - 开发文档
- `README.md` - 项目说明

---

## 访问路径

### 开发环境
```
前端应用：http://localhost:5173
后端 API：http://localhost:8000
API 文档：http://localhost:8000/api/docs
Gradio 备用：http://localhost:7860
```

### 生产环境（Docker）
```
前端应用：http://localhost
后端 API：http://localhost:8000
API 文档：http://localhost:8000/api/docs
Gradio 备用：http://localhost:7860
MongoDB：localhost:27017
```

---

**本文档由 GitHub Copilot 辅助生成 🤖**
