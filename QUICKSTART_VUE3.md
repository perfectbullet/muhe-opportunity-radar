# 🚀 Vue3 + FastAPI 架构快速开始

## 🎯 架构概览

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│   Vue3      │ ───► │   FastAPI    │ ───► │   MongoDB    │
│  前端界面    │ HTTP │   后端 API    │      │   数据存储    │
│ (Port 5173) │ ◄─── │  (Port 8000) │      │ (Port 27017) │
└─────────────┘      └──────────────┘      └──────────────┘
```

## 📦 快速开始

### 1. 安装依赖

```bash
# Python 后端依赖
pip install -r requirements.txt

# Vue3 前端依赖
cd frontend
npm install
cd ..
```

### 2. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，配置你的 API 密钥
# 至少需要配置一个 LLM Provider 的 API Key
```

### 3. 启动服务

#### 方式A：使用启动脚本（推荐）

**Windows:**
```bash
start_new.bat
```

**Linux/Mac:**
```bash
chmod +x start_new.sh
./start_new.sh
```

选择选项 `[3]` 同时启动后端和前端

#### 方式B：分别启动

**终端 1 - 启动后端:**
```bash
python -m uvicorn api.main:app --reload --port 8000
```

**终端 2 - 启动前端:**
```bash
cd frontend
npm run dev
```

### 4. 访问应用

- **前端界面**: http://localhost:5173
- **API 文档**: http://localhost:8000/api/docs
- **备用 Gradio**: http://localhost:7860 (运行 `python app.py`)

## 🐳 Docker 部署

### 快速部署

```bash
# 一键启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 访问地址

- **前端**: http://localhost
- **API**: http://localhost:8000
- **Gradio**: http://localhost:7860
- **MongoDB**: localhost:27017

## 📚 核心功能

### 1. 单一视角分析
访问 `/analysis` 页面，选择投资大师，输入分析材料

### 2. 多视角对比
访问 `/comparison` 页面，选择多位投资大师进行对比

### 3. 历史记录
访问 `/history` 页面，查看和搜索所有分析记录

### 4. 统计信息
访问 `/statistics` 页面，查看数据可视化统计

## 🔧 开发指南

详细文档：
- [迁移实施指南](docs/vue3_migration_guide.md)
- [Copilot 提示词模板](docs/copilot_prompts.md)
- [原 Gradio 指南](docs/gradio_guide.md)

## 📡 API 端点

### 分析接口
- `POST /api/v1/analyze` - 单一视角分析
- `POST /api/v1/analyze/stream` - 流式分析（SSE）
- `POST /api/v1/compare` - 多视角对比
- `POST /api/v1/compare/stream` - 流式对比

### 记录接口
- `GET /api/v1/records` - 获取最近记录
- `GET /api/v1/records/{id}` - 获取详情
- `GET /api/v1/records/search/{keyword}` - 搜索

### 投资者接口
- `GET /api/v1/investors` - 获取所有投资者
- `GET /api/v1/investors/{id}` - 获取投资者详情

### 统计接口
- `GET /api/v1/statistics` - 获取统计数据

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代 Web 框架
- **LangChain** - AI 编排框架
- **MongoDB** - 数据存储
- **Uvicorn** - ASGI 服务器

### 前端
- **Vue3** - 渐进式框架
- **Naive UI** - 炫酷组件库
- **ECharts** - 数据可视化
- **TailwindCSS** - 样式框架
- **Pinia** - 状态管理
- **Vite** - 构建工具

## 🐛 常见问题

### Q: CORS 错误
确保后端 CORS 配置包含前端地址 `http://localhost:5173`

### Q: MongoDB 连接失败
检查 MongoDB 是否已启动，端口是否正确

### Q: 前端请求 404
确保后端已启动，Vite 代理配置正确

## 📝 下一步

1. ✅ 基础架构已搭建完成
2. 🔄 根据需求添加新功能
3. 🎨 优化 UI/UX 体验
4. 🚀 部署到生产环境

**祝开发顺利！🎉**
