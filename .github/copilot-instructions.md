# Muhe Opportunity Radar - AI 编码指南

## 项目概览
AI 投资机会分析工具，模拟10位投资大师（巴菲特、格雷厄姆、索罗斯等）的投资理念，对投资标的进行多视角分析。

**实际技术栈**：
- **前端**: Vue3 + Naive UI + ECharts（生产推荐）/ Gradio（快速测试）
- **后端**: FastAPI + Motor（MongoDB 异步驱动）
- **AI 框架**: LangChain（提示词模板）+ 多 LLM 支持
- **数据库**: MongoDB（历史记录）
- **部署**: Docker Compose（Nginx + FastAPI + Vue3 + MongoDB）

## 🏗️ 架构理解（三层分离 + 数据分析工作流）

```
Vue3 前端 (5173)  ←→  FastAPI API (8000)  ←→  MongoDB (27017)
     ↓                      ↓
 流式打字机效果      异步分析服务层              
                    (asyncio.to_thread)           LangGraph 工作流
                                                 (数据分析/计算/统计)
```

### 核心数据流
1. **用户输入** → Vue3 前端发送 POST `/api/v1/analyze`
2. **API 路由** → `api/routers/analysis.py` 调用 `AnalysisService`
3. **服务层** → `asyncio.to_thread` 调用同步的 `PerspectiveAnalyzer`
4. **分析引擎** → 根据投资者画像（`data/investor_profiles.json`）构造 Prompt
5. **LLM 调用** → LangChain 客户端请求 SiliconFlow/DeepSeek/Qwen 等
6. **数据持久化** → Motor 异步保存到 MongoDB
7. **流式返回** → Server-Sent Events (SSE) 返回打字机效果

### 数据导入流（规划中）
```
文档上传 (PDF/Word/Markdown) → 文档解析器 → 结构化数据提取 
                                              ↓
                                     MongoDB 存储 + 向量化（可选）
                                              ↓
                                     LangGraph 数据分析工作流
```

### 关键设计模式
- **投资者画像驱动**: 所有分析基于 `InvestorProfile` Pydantic 模型（`analysis/investor_profiles.py`）
- **同步转异步**: `AnalysisService` 用 `asyncio.to_thread` 包装同步的 LangChain 调用
- **前后端分离**: FastAPI 提供标准 RESTful API，支持 Swagger 文档（`/api/docs`）
- **LangGraph 工作流**: 用于复杂数据分析、计算、统计任务（规划中）

## 📂 目录结构（实际已实现）

```
api/                    # FastAPI 后端
├── main.py            # 应用入口 (uvicorn)
├── models/            # Pydantic 数据模型
│   ├── requests.py   # AnalysisRequest, ComparisonRequest
│   └── responses.py  # AnalysisResponse, RecordResponse
├── routers/          # API 路由（按功能分模块）
│   ├── analysis.py   # /analyze, /compare (支持 SSE 流式)
│   ├── records.py    # /records, /search, /statistics
│   └── investors.py  # /investors
└── services/         # 业务逻辑层（隔离核心分析逻辑）
    ├── analysis_service.py    # 封装 PerspectiveAnalyzer
    ├── record_service.py      # MongoDB 查询封装
    └── investor_service.py    # 投资者画像查询

analysis/             # AI 分析核心
├── perspective_analyzer.py  # 多视角分析引擎（同步）
└── investor_profiles.py     # 投资者画像管理（Pydantic）

storage/
└── db_manager.py     # MongoDB 异步操作（Motor + AsyncIOMotorClient）

frontend/src/         # Vue3 前端
├── api/             # Axios 客户端（按模块拆分）
├── views/           # 4 个页面：单一分析、多视角对比、历史记录、统计
├── components/      # 可复用组件
└── router/          # Vue Router 配置

app.py               # Gradio 备用界面（保留用于快速测试）
```

## 🚀 开发工作流

### 启动服务（Windows）
```cmd
REM 方式1：使用启动脚本（推荐）
start_new.bat
REM 选择 [3] 同时启动后端和前端

REM 方式2：手动启动
REM 终端1 - 后端
python -m uvicorn api.main:app --reload --port 8000

REM 终端2 - 前端
cd frontend
npm run dev
```

### 访问地址
- **Vue3 界面**: http://localhost:5173
- **API 文档**: http://localhost:8000/api/docs（Swagger UI，自动生成）
- **Gradio 备用**: `python app.py` → http://localhost:7860

### 测试新分析逻辑
```bash
# 在 scripts/ 下创建独立测试脚本
python scripts/test_multi_perspective.py

# 或使用 API 测试
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"material": "贵州茅台 PE=35", "investor_id": "buffett"}'
```

## ⚙️ 配置管理（环境变量）

`.env` 文件（必须配置，已在 `.gitignore`）：
```bash
# LLM 配置（至少配置一个）
SILICONFLOW_API_KEY=sk-xxx        # 推荐：性价比高
DEEPSEEK_API_KEY=sk-xxx
QWEN_API_KEY=sk-xxx

# MongoDB（Docker 自动配置，本地开发需手动）
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=muhe_opportunity_radar

# 可选：数据源
TUSHARE_TOKEN=xxx
```

### LLM Provider 切换
在 `PerspectiveAnalyzer` 初始化时指定（默认：siliconflow）：
```python
analyzer = PerspectiveAnalyzer(
    llm_provider="siliconflow",  # 默认推荐：性价比高
    # 其他选项：deepseek/qwen/zhipu/openai
    temperature=0.7
)
```

**推荐 LLM 选择**：
- **SiliconFlow**（默认）：性价比高，速度快，适合生产环境
- **DeepSeek V3**：推理能力强，适合复杂分析（0.14元/M tokens）
- **Qwen-Max**：中文理解优秀，适合财经文本分析
- **Zhipu GLM-4**：长文本处理能力强（128K context）

## 🎯 添加新投资者画像

1. **编辑 `data/investor_profiles.json`**，添加新对象：
```json
{
  "id": "munger",
  "name": "查理·芒格",
  "name_en": "Charlie Munger",
  "title": "伯克希尔副董事长",
  "investment_philosophy": "多元思维模型...",
  "core_principles": ["反向思考", "心理学应用"],
  "analysis_focus": ["认知偏差", "商业护城河"],
  "risk_tolerance": "低",
  "holding_period": "超长期",
  "prompt_template": "作为查理·芒格..."
}
```

2. **重启服务** - `InvestorProfileManager` 会自动加载新配置
3. **前端自动更新** - `/api/v1/investors` 接口返回最新列表

## 🔄 API 开发模式

### 添加新接口
1. **定义 Pydantic 模型** → `api/models/requests.py` 和 `responses.py`
2. **创建路由** → `api/routers/xxx.py`
```python
from fastapi import APIRouter
from api.models.requests import MyRequest
from api.models.responses import MyResponse

router = APIRouter()

@router.post("/my-endpoint", response_model=MyResponse)
async def my_endpoint(request: MyRequest):
    # 业务逻辑
    return MyResponse(...)
```
3. **注册路由** → `api/main.py` 中 `app.include_router(xxx.router)`
4. **访问文档** → http://localhost:8000/api/docs 验证接口

### 流式输出（SSE）
```python
from fastapi.responses import StreamingResponse

@router.post("/analyze-stream")
async def analyze_stream(request: AnalysisRequest):
    async def event_generator():
        async for chunk in service.analyze_single_stream(...):
            yield f"data: {chunk}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

## 🗄️ MongoDB 数据操作

### 异步查询模式（Motor）
```python
from storage.db_manager import AnalysisRecordManager

# 初始化
db_manager = AnalysisRecordManager()

# 查询（异步）
records = await db_manager.get_recent_records(limit=20)
result = await db_manager.search_records(keyword="茅台")

# 保存（异步）
record_id = await db_manager.save_record({
    "investor_id": "buffett",
    "material": "...",
    "analysis": "...",
    "created_at": datetime.utcnow()
})
```

### 索引策略
已创建索引（`db_manager.ensure_indexes()`）：
- `created_at` (降序) - 时间查询
- `investor_id` - 按投资者筛选
- 复合索引 `(investor_id, created_at)` - 组合查询

## 🐳 Docker 部署

### 本地测试
```bash
# 一键启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f api      # 后端日志
docker-compose logs -f frontend # 前端日志

# 停止服务
docker-compose down
```

### 服务访问
- **前端**: http://localhost (Nginx 端口 80)
- **API**: http://localhost:8000
- **MongoDB**: localhost:27017

### 数据持久化
`docker-compose.yml` 已配置卷：
- `mongodb_data:/data/db` - MongoDB 数据持久化
- `./data:/app/data` - 本地 data 目录挂载

## 🔧 常见调试场景

### MongoDB 连接失败
```bash
# 检查 MongoDB 服务
docker-compose ps mongodb

# 本地 MongoDB 未启动
mongod --dbpath ./data/db  # 本地启动 MongoDB
```

### LLM API 超时
```python
# 在 PerspectiveAnalyzer._init_llm() 中增加超时配置
llm = ChatOpenAI(
    timeout=60,  # 增加超时时间
    max_retries=2
)
```

### 前端跨域问题
`api/main.py` 已配置 CORS：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"]
)
```

## 📝 代码风格约定

- *📄 数据导入功能（规划中）

### 支持格式
- **PDF** - 财报、研究报告
- **Word (.docx)** - 分析文档、投资备忘录
- **Markdown** - 结构化投资笔记

### 实现建议
```python
# 推荐库
# PDF: PyPDF2 或 pdfplumber（表格提取更好）
# Word: python-docx
# Markdown: markdown 或直接读取文本

from pdfplumber import open as pdf_open
from docx import Document

async def import_document(file_path: str, doc_type: str):
    """
    导入文档并提取文本
    
    Args:
        file_path: 文件路径
        doc_type: pdf/word/markdown
    """
    if doc_type == "pdf":
        with pdf_open(file_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages])
    elif doc_type == "word":
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif doc_type == "markdown":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    
    # 存储到 MongoDB
    await db_manager.save_document({"content": text, "type": doc_type})
```

### API 接口建议
```python
# api/routers/documents.py
@router.post("/upload")
async def upload_document(file: UploadFile):
    """上传并解析文档"""
    # 1. 保存文件到临时目录
    # 2. 根据扩展名调用对应解析器
    # 3. 提取结构化数据并存储
    # 4. 返回文档 ID 供后续分析使用
```

## 🔄 LangGraph 数据分析工作流（规划中）

### 应用场景
- **数据计算**: 财务指标计算（PE、PB、ROE、PEG）
- **统计分析**: 历史数据趋势分析、行业对比
- **多步推理**: 结合多个数据源的综合分析

### 工作流设计示例
```python
from langgraph.graph import StateGraph, END

# 定义状态
class AnalysisState:
    material: str          # 原始材料
    parsed_data: dict      # 解析后的结构化数据
    calculated_metrics: dict  # 计算指标
    analysis_result: str   # 分析结果

# 创建工作流
workflow = StateGraph(AnalysisState)

# 添加节点
workflow.add_node("parse", parse_document_node)      # 文档解析
workflow.add_node("calculate", calculate_metrics_node)  # 指标计算
workflow.add_node("analyze", llm_analyze_node)       # LLM 分析
workflow.add_node("summarize", summarize_node)       # 结果汇总

# 定义边
workflow.add_edge("parse", "calculate")
workflow.add_edge("calculate", "analyze")
workflow.add_edge("analyze", "summarize")
workflow.add_edge("summarize", END)

# 设置入口
workflow.set_entry_point("parse")

# 编译
app = workflow.compile()
```

### 集成到现有架构
```python
# analysis/graph_workflow.py（新建文件）
class DataAnalysisWorkflow:
    """LangGraph 数据分析工作流"""
    
    def __init__(self, llm_provider="siliconflow"):
        self.llm = self._init_llm(llm_provider)
        self.workflow = self._build_workflow()
    
    async def run_analysis(self, document_id: str):
        """执行完整分析流程"""
        result = await asyncio.to_thread(
            self.workflow.invoke,
            {"document_id": document_id}
        )
        return result

# 在 AnalysisService 中调用
async def analyze_with_workflow(self, document_id: str):
    workflow = DataAnalysisWorkflow()
    return await workflow.run_analysis(document_id)
```

## 🎓 项目特色理解

1. **投资者画像系统** - 核心创新点，通过 JSON 配置即可扩展新投资风格
2. **同步到异步适配** - `AnalysisService` 作为适配层，避免重写 LangChain 同步代码
3. **双前端架构** - Gradio 用于快速原型，Vue3 用于生产，共享后端 API
4. **流式打字机效果** - SSE 流式输出提升用户体验（见 `analysis.py` 的 `/analyze-stream`）
5. **文档导入 + LangGraph 工作流** - 支持 PDF/Word/Markdown 导入，结合 LangGraph 进行复杂数据分析

## 🎓 项目特色理解

1. **投资者画像系统** - 核心创新点，通过 JSON 配置即可扩展新投资风格
2. **同步到异步适配** - `AnalysisService` 作为适配层，避免重写 LangChain 同步代码
3. **双前端架构** - Gradio 用于快速原型，Vue3 用于生产，共享后端 API
4. **流式打字机效果** - SSE 流式输出提升用户体验（见 `analysis.py` 的 `/analyze-stream`）
