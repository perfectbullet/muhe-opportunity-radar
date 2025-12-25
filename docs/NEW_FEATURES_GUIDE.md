# 📦 新功能使用指南

## 🎉 已实现的三大功能

### 1️⃣ 文档解析器模块
**位置**: `analysis/document_parser.py`

**支持格式**:
- PDF（`.pdf`）- 使用 pdfplumber 或 PyPDF2
- Word（`.doc`, `.docx`）- 使用 python-docx
- Markdown（`.md`, `.markdown`）- 原生支持

**基本用法**:
```python
from analysis.document_parser import parse_document

# 解析文档
result = parse_document("财报.pdf")

if result["success"]:
    print(f"内容: {result['content']}")
    print(f"页数: {result.get('pages')}")
    print(f"元数据: {result.get('metadata')}")
else:
    print(f"错误: {result['error']}")
```

### 2️⃣ LangGraph 数据分析工作流
**位置**: `analysis/graph_workflow.py`

**工作流程**:
```
解析文档 → 计算指标 → AI分析 → 结果汇总
```

**功能**:
- 📊 自动提取财务指标（PE、PB、ROE、PEG、毛利率等）
- 🔢 计算衍生指标（PEG = PE / 增长率）
- 📈 估值评估（低估/合理/高估）
- ⭐ 企业质量评分（优秀/良好/一般/较差）
- 🤖 结合投资者画像进行 AI 深度分析

**基本用法**:
```python
from analysis.graph_workflow import DataAnalysisWorkflow

# 创建工作流
workflow = DataAnalysisWorkflow(llm_provider="siliconflow")

# 执行分析
result = workflow.run(
    material="""
    公司：贵州茅台
    PE：35倍
    ROE：30%
    营收增长：15%
    """,
    investor_id="buffett"
)

# 查看结果
if result["final_report"]:
    print(result["final_report"]["markdown"])
```

**异步用法**:
```python
# 在 FastAPI 中使用
result = await workflow.run_async(
    material=material,
    investor_id="buffett"
)
```

### 3️⃣ 文件上传 API 接口
**位置**: `api/routers/documents.py`

**核心接口**:

#### 📤 上传文档
```bash
POST /api/v1/documents/upload
Content-Type: multipart/form-data

参数:
- file: 文档文件（必需）
- investor_id: 投资者ID（可选，默认 buffett）
- auto_analyze: 是否自动分析（可选，默认 false）

响应:
{
  "success": true,
  "document_id": "uuid-xxx",
  "filename": "财报.pdf",
  "format": "pdf",
  "size": 1024000,
  "content_preview": "...",
  "metadata": {...}
}
```

#### 🔄 工作流分析
```bash
POST /api/v1/documents/analyze-workflow
Content-Type: application/json

{
  "material": "公司：茅台\nPE：35\nROE：30%",
  "investor_id": "buffett",
  "use_workflow": true
}

响应:
{
  "success": true,
  "final_report": {
    "markdown": "# 投资分析报告\n...",
    "structured_data": {...}
  },
  "workflow_result": {...}
}
```

#### 📄 分析已上传文档
```bash
POST /api/v1/documents/analyze-document
Content-Type: application/json

{
  "document_id": "uuid-xxx",
  "investor_id": "buffett"
}
```

#### 📋 列出所有文档
```bash
GET /api/v1/documents/documents
```

#### 🗑️ 删除文档
```bash
DELETE /api/v1/documents/documents/{document_id}
```

---

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install langgraph pdfplumber python-docx python-multipart
```

### 2. 启动 API 服务
```bash
python -m uvicorn api.main:app --reload --port 8080
```

### 3. 访问 API 文档
打开浏览器: http://localhost:8080/api/docs

### 4. 测试工作流
```bash
python scripts/test_workflow.py
```

---

## 📁 新增文件结构

```
analysis/
├── document_parser.py        # 文档解析器
├── graph_workflow.py          # LangGraph 工作流
└── nodes/                     # 工作流节点
    ├── __init__.py
    ├── parse_node.py         # 文档解析节点
    ├── calculate_node.py     # 指标计算节点
    ├── analyze_node.py       # AI 分析节点
    └── summarize_node.py     # 结果汇总节点

api/
├── routers/
│   └── documents.py           # 文档管理 API
├── services/
│   └── workflow_service.py    # 工作流服务层
└── models/
    ├── requests.py            # 新增请求模型
    └── responses.py           # 新增响应模型

data/
└── uploads/                   # 上传文件存储目录

scripts/
└── test_workflow.py           # 测试脚本
```

---

## 🎯 使用示例

### 示例 1: 上传并分析财报 PDF

**使用 curl**:
```bash
curl -X POST "http://localhost:8080/api/v1/documents/upload" \
  -F "file=@财报.pdf" \
  -F "investor_id=buffett" \
  -F "auto_analyze=true"
```

**使用 Python**:
```python
import requests

files = {'file': open('财报.pdf', 'rb')}
data = {'investor_id': 'buffett', 'auto_analyze': 'true'}

response = requests.post(
    'http://localhost:8080/api/v1/documents/upload',
    files=files,
    data=data
)

print(response.json())
```

### 示例 2: 使用工作流分析文本材料

```python
import requests

payload = {
    "material": """
    公司：宁德时代
    市盈率：45倍
    市净率：8倍
    ROE：25%
    营收增长：80%
    毛利率：28%
    """,
    "investor_id": "lynch",  # 使用彼得·林奇的视角（成长股专家）
    "use_workflow": True
}

response = requests.post(
    'http://localhost:8080/api/v1/documents/analyze-workflow',
    json=payload
)

result = response.json()

# 打印最终报告
if result['success']:
    print(result['final_report']['markdown'])
    
    # 查看提取的指标
    metrics = result['workflow_result']['calculated_metrics']['metrics']
    print(f"\nPEG 比率: {metrics.get('peg_ratio')}")
```

### 示例 3: 在 Gradio 中集成工作流

```python
import gradio as gr
from analysis.graph_workflow import DataAnalysisWorkflow

workflow = DataAnalysisWorkflow()

def analyze_with_workflow(material, investor_id):
    result = workflow.run(material=material, investor_id=investor_id)
    
    if result.get("final_report"):
        return result["final_report"]["markdown"]
    else:
        return f"分析失败: {result.get('error')}"

# Gradio 界面
demo = gr.Interface(
    fn=analyze_with_workflow,
    inputs=[
        gr.Textbox(label="分析材料", lines=10),
        gr.Dropdown(choices=["buffett", "graham", "lynch"], label="投资者")
    ],
    outputs=gr.Markdown(label="分析报告")
)

demo.launch()
```

---

## 🔧 配置说明

### 环境变量
确保 `.env` 文件包含以下配置：

```bash
# LLM Provider（默认 siliconflow）
SILICONFLOW_API_KEY=sk-xxx
DEEPSEEK_API_KEY=sk-xxx  # 可选
QWEN_API_KEY=sk-xxx       # 可选

# MongoDB（可选）
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=muhe_opportunity_radar
```

### 自定义工作流节点

如果需要添加新的分析节点：

1. 在 `analysis/nodes/` 创建新节点文件
2. 实现节点函数（接收 `state` 字典，返回更新后的 `state`）
3. 在 `graph_workflow.py` 中添加节点并连接

```python
# 示例：添加风险评估节点
def risk_assessment_node(state):
    # 实现风险评估逻辑
    return {
        **state,
        "risk_score": calculate_risk(state)
    }

# 在工作流中添加
workflow.add_node("risk_assessment", risk_assessment_node)
workflow.add_edge("analyze", "risk_assessment")
workflow.add_edge("risk_assessment", "summarize")
```

---

## 📊 工作流可视化

LangGraph 工作流的执行流程：

```mermaid
graph LR
    A[开始] --> B[解析文档]
    B --> C[计算指标]
    C --> D[AI 分析]
    D --> E[结果汇总]
    E --> F[结束]
    
    B -.提取文本.-> C
    C -.计算PE/ROE/PEG.-> D
    D -.投资者视角分析.-> E
    E -.生成Markdown报告.-> F
```

---

## ⚠️ 注意事项

1. **PDF 解析**: 需要安装 `pdfplumber`（推荐）或 `PyPDF2`
2. **LangGraph**: 必须安装 `pip install langgraph`
3. **文件上传**: 上传的文件保存在 `data/uploads/` 目录
4. **LLM 调用**: 确保配置了有效的 API Key
5. **异步处理**: 工作流在后端使用 `asyncio.to_thread` 避免阻塞

---

## 🐛 常见问题

### Q1: LangGraph 未安装
```bash
pip install langgraph
```

### Q2: PDF 解析失败
```bash
pip install pdfplumber
# 或
pip install PyPDF2
```

### Q3: Word 文档解析失败
```bash
pip install python-docx
```

### Q4: 文件上传 413 错误（文件过大）
在 `uvicorn` 启动时设置：
```python
uvicorn.run(app, limit_max_size=100*1024*1024)  # 100MB
```

---

## 🎓 进阶用法

### 添加自定义财务指标

修改 `analysis/nodes/calculate_node.py`：

```python
def calculate_metrics_node(state):
    # 添加新指标提取
    metrics = {
        "pe_ratio": _extract_metric(text, r"PE[：:=\s]*(\d+\.?\d*)"),
        # 添加自定义指标
        "debt_ratio": _extract_metric(text, r"负债率[：:=\s]*(\d+\.?\d*)%?"),
        "quick_ratio": _extract_metric(text, r"速动比率[：:=\s]*(\d+\.?\d*)"),
    }
    
    # 自定义评估逻辑
    if metrics["debt_ratio"] and metrics["debt_ratio"] < 30:
        # 低负债率加分
        pass
    
    return {**state, "calculated_metrics": metrics}
```

---

## 📚 相关文档

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [FastAPI 文件上传](https://fastapi.tiangolo.com/tutorial/request-files/)
- [pdfplumber 文档](https://github.com/jsvine/pdfplumber)

---

✅ **所有功能已完整实现，可以开始使用！**
