# Muhe Opportunity Radar - AI 编码指南

## 项目概览
这是一个基于 AI 的投资机会挖掘工具，聚合多源数据（股票、新闻、财报）并通过大模型分析识别投资机会。

**技术栈核心**：
- **AI 框架**: LangChain + LangGraph（工作流编排）
- **LLM**: 多模型支持（DeepSeek、千问、智谱、GPT、Claude）通过统一接口切换
- **数据采集**: Scrapy（爬虫）+ Tushare（股票数据）
- **数据存储**: ChromaDB（向量数据库）+ SQLite（结构化数据）
- **前端**: Gradio（推荐，AI 原生）或 Next.js + React（高定制化）
- **数据处理**: Pandas
- **部署**: Docker + Docker Compose

## 架构设计原则

### 数据流设计
1. **数据采集层** → Scrapy 爬虫 + Tushare API
2. **数据存储层** → SQLite（事实数据）+ ChromaDB（语义检索）
3. **分析层** → LangChain/LangGraph 编排 AI 分析流程
4. **展示层** → Streamlit 可视化

### 目录结构规范
推荐创建以下模块结构：
```
muhe-opportunity-radar/
├── app.py                 # 主应用入口（Gradio 或 Streamlit）
├── config.py              # 配置管理（API 密钥、数据库连接）
├── Dockerfile             # Docker 镜像构建
├── docker-compose.yml     # 容器编排配置
├── data_collection/       # 数据采集模块
│   ├── scrapers/         # Scrapy 爬虫
│   └── stock_api.py      # Tushare 股票数据接口
├── storage/              # 数据存储
│   ├── vector_store.py   # ChromaDB 操作
│   └── db_manager.py     # SQLite 操作
├── analysis/             # AI 分析模块
│   ├── chains.py         # LangChain 链定义
│   ├── graph_workflow.py # LangGraph 工作流
│   └── llm_client.py     # 多模型统一接口
├── ui/                   # 前端组件
│   └── components.py     # UI 组件定义
└── scripts/              # 测试/工具脚本
    └── test_*.py         # 功能测试脚本
```

## 关键开发约
  - `LLM_PROVIDER` (deepseek/qwen/zhipu/openai/claude)
  - `LLM_API_KEY` (根据 provider 动态加载)
  - `TUSHARE_TOKEN`
  -

### 配置管理
- **API 密钥**存储在 `.env` 文件（已在 `.gitignore` 中）
- 使用 `config.py` 集中管理配置，避免硬编码
- 必需配置项：`OPENAI_API_KEY`, `TUSHARE_TOKEN`, `DB_PATH`, `CHROMADB_PATH`

### LangChain/LangGraph 使用
- 使用 **LangGraph** 构建复杂的多步分析流程（如：数据获取→趋势分析→机会筛选→风险评估）
- 使用 **LangChain** 的 Prompt 模板标准化 AI 交互
- 示例流程节点：
  ```python
  from langgraph.graph import StateGraph
  # 定义状态机：数据输入 → AI 分析 → 结果输出
  workflow = StateGraph(state_schema)
  workflow.add_node("fetch_data", fetch_node)
  workflow.add_node("analyze", analyze_node)
  workflow.add_edge("fetch_data", "analyze")
  ```

### 数据存储策略
- **前端开发
**推荐方案：Gradio（AI 原生，炫酷组件丰富）**
- 使用 `gr.Blocks()` 自定义布局，结合 `gr.Tab`, `gr.Row`, `gr.Column`
- 数据可视化：`gr.LinePlot`, `gr.BarPlot`（支持 Plotly JSON）
- 实时更新：`gr.Progress()` + 流式输出
- 主题定制：使用 `theme` 参数打造科技感 UI

**备选方案：Next.js + React（高定制化）**
- 使用 Tailwind CSS + Framer Motion 实现动画效果
- 数据图表：Recharts 或 D3.js
- 后端 API：FastAPI（替换 Streamlit）

**通用原则**：
- 使用深色主题 + 渐变色增强科技感
- 数据加载使用骨架屏（Skeleton Loading）
- 关键指标用卡片 + 动画强调
# 本地开发
python app.py  # Gradio 默认端口 7860

# Docker 部署
docker-compose up -d  # 后台运行
docker-compose logs -f  # 查看日志
docker-compose down  # 停止服务
```

### 数据采集调试
```bash
# 运行单个 Scrapy 爬虫
cd data_collection/scrapers
scrapy crawl news_spider -o output.json
```

### 多模型 LLM 集成
**统一接口设计**（`analysis/llm_client.py`）：
```python
class LLMClient:
    def __init__(self, provider: str):
        # 根据 provider 初始化对应客户端
        # deepseek, qwen, zhipu, openai, claude
    
    def chat(self, messages: list) -> str:
        # 统一的对话接口
```

**推荐模型选择**：
- **DeepSeek V3**: 性价比高，推理能力强（0.14元/M tokens）
- **千问 Qwen-Max**: 中文理解好，适合财经文本
- **智谱 GLM-4**: 长文本处理优秀（128K context）
- **GPT-4o-mini**: 稳定性高，适合生产环境
- **Claude 3.5 Sonnet**: 分析能力强，适合复杂推理

### 数据源推荐


### 开发相关
- **ChromaDB 持久化**：使用 `chromadb.Client(Settings(persist_directory="./data/chroma"))`
- **多模型切换**：通过 `config.py` 的 `LLM_PROVIDER` 环境变量切换
- **Gradio 实时更新**：使用 `gr.update()` 动态更新组件
- **测试脚本编写**：在 `scripts/` 下创建独立脚本，直接 `python scripts/test_xxx.py` 运行

### Docker 相关
- **数据持久化**：确保 `docker-compose.yml` 挂载 `./data` 卷
- **环境变量**：`.env` 文件需与 `docker-compose.yml` 同级
- **容器调试**：`docker-compose exec app bash` 进入容器
- **日志查看**：`docker-compose logs -f app` 实时查看应用日志
  import tushare as ts
  ts.set_token('YOUR_TOKEN')
  pro = ts.pro_api()
  df = pro.daily(ts_code='000001.SZ', start_date='20230101')
  ```
- **AKShare**（https://akshare.akfamily.xyz）- 无需 Token，数据源丰富

**财经新闻**：
- **东方财富网**（https://www.eastmoney.com）- 实时资讯
- **新浪财经**（https://finance.sina.com.cn）- 行情数据
- **雪球**（https://xueqiu.com）- 用户讨论（需处理反爬）

**财报数据**：
- **巨潮资讯网**（http://www.cninfo.com.cn）- 官方公告
- **Tushare 财务数据接口** - 结构化财报

**反爬策略**：
- 使用 `scrapy-user-agents` 随机 UA
- 设置 `DOWNLOAD_DELAY = 2`（Scrapy settings）
- 使用代理池（可选，如快代理）

### Docker 部署配置

**Dockerfile 示例结构**：
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD ["python", "app.py"]
```

**docker-compose.yml 关键配置**：
```yaml
services:
  app:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./data:/app/data  # 持久化数据
    env_file:
      - .env  # 环境变量
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
``` 8501
```

### 数据采集调试
```bash
# 运行单个 Scrapy 爬虫
cd data_collection/scrapers
scrapy crawl news_spider -o output.json
```

## 外部依赖注意事项

### Tushare API
- 需要注册获取 Token：https://tushare.pro/register
- 免费账号有调用频率限制（200次/分钟）
- 示例调用：
  ```python
  import tushare as ts
  ts.set_token('YOUR_TOKEN')
  pro = ts.pro_api()
  df = pro.daily(ts_code='000001.SZ', start_date='20230101')
  ```

### OpenAI API
- 使用 `gpt-4o-mini` 模型平衡成本与效果
- 实现 Token 计数和成本跟踪（参考 LangChain 的回调机制）

## 新功能开发指南
1. **数据源集成**：在 `data_collection/` 添加新采集器，更新 `config.py` 配置
2. **AI 分析逻辑**：在 `analysis/` 中创建新的 LangGraph 节点或 LangChain 链
3. **前端展示**：在 `ui/components.py` 添加 Streamlit 组件，在 `app.py` 中集成

## 常见问题
- **ChromaDB 持久化**：确保 `chromadb.Client(Settings(persist_directory="path"))` 指定存储路径
- **Streamlit 热重载**：修改代码后，Streamlit 会自动检测并提示重新运行
- **Scrapy 反爬**：实现随机 User-Agent 和请求延迟（见 `settings.py`）
