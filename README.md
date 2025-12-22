# Muhe Opportunity Radar

> 🎯 **快速开始？** 
> - Gradio 版本：查看 [快速启动指南 QUICKSTART.md](QUICKSTART.md)
> - **🆕 Vue3 版本（推荐）**：查看 [Vue3 快速开始 QUICKSTART_VUE3.md](QUICKSTART_VUE3.md)

## 项目简介
Muhe Opportunity Radar（炑禾机会雷达）是一款基于信息聚合与AI分析的投资机会挖掘工具，核心功能为聚合多源投资相关数据，通过AI模型分析识别潜在投资机会并进行风险提示。

## 🆕 架构升级：Vue3 + FastAPI

**项目已完成前后端分离架构升级！** 现提供两种部署方式：

| 版本 | 技术栈 | 特点 | 推荐场景 |
|------|--------|------|---------|
| **Gradio 版** | Python Gradio | 快速部署，简单易用 | 快速测试、个人使用 |
| **Vue3 版（推荐）** | Vue3 + FastAPI | 炫酷 UI、高性能、可扩展 | 生产环境、团队开发 |

### Vue3 版本亮点 ✨
- 🎨 **Naive UI 深色主题** - 科技感十足的现代化界面
- 📊 **ECharts 数据可视化** - 丰富的图表展示
- ⚡ **流式输出** - 打字机效果的实时分析
- 🚀 **前后端分离** - 独立开发和部署
- 📡 **RESTful API** - 标准化接口，自动生成文档
- 🐳 **Docker 部署** - 一键启动所有服务

**[查看完整迁移指南 →](docs/vue3_migration_guide.md)**

## 核心特性
1. **多源数据聚合**：支持股票数据、行业新闻、财务报表等结构化/非结构化数据采集
2. **AI智能分析**：基于大模型实现趋势识别、机会筛选、风险预警
3. **🎯 多投资理念视角**：模拟10位投资大师的思维方式，从不同角度分析同一投资标的
   - 巴菲特（价值投资）、格雷厄姆（量化价值）、索罗斯（宏观对冲）
   - 彼得·林奇（成长股）、利弗莫尔（技术分析）、达利欧（全天候策略）
   - 约翰·聂夫（低市盈率）、博格（指数投资）、伊坎（激进投资）、费雪（成长股）
4. **📊 Gradio 前端界面**：炫酷的 Web UI，支持：
   - 单一视角分析
   - 多视角对比分析
   - 历史记录查询和搜索
   - 统计信息展示
5. **💾 历史记录管理**：MongoDB 存储分析历史，支持回溯和趋势分析
## 快速启动

### 环境依赖
- Python 3.8+
- 依赖包：requirements.txt
- MongoDB（可选，用于历史记录）

### 安装步骤
1. 克隆仓库：`git clone <远程仓库地址>`
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # 或
   .venv\Scripts\activate     # Windows
   ```
3. 安装依赖：`pip install -r requirements.txt`
4. 配置环境变量：创建 `.env` 文件，配置API密钥
   ```bash
   # LLM 配置（选择一个或多个）
   SILICONFLOW_API_KEY=your_siliconflow_key
   DEEPSEEK_API_KEY=your_deepseek_key
   QWEN_API_KEY=your_qwen_key
   
   # 数据源
   TUSHARE_TOKEN=your_tushare_token
   
   # MongoDB（可选）
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_DB_NAME=muhe_opportunity_radar
   ```
5. 启动服务：
   ```bash
   # 方法1：使用启动脚本（推荐）
   start.bat          # Windows
   ./start.sh         # Linux/Mac
   
   # 方法2：直接运行
   python app.py
   ```
6. 访问界面：浏览器打开 http://localhost:7860

## 多投资理念分析功能 🎯

### 功能介绍
本项目支持从10位传奇投资大师的视角分析投资标的，让AI模拟不同的投资理念和决策思路：

| 投资者 | 投资风格 | 核心理念 | 适用场景 |
|--------|---------|---------|---------|
| **沃伦·巴菲特** | 价值投资 | 护城河+安全边际 | 寻找长期优质企业 |
| **本杰明·格雷厄姆** | 量化价值 | 严格财务指标筛选 | 寻找低估股票 |
| **乔治·索罗斯** | 宏观对冲 | 反身性理论 | 判断趋势转折点 |
| **彼得·林奇** | 成长价值 | PEG指标+生活发现 | 中小成长股 |
| **杰西·利弗莫尔** | 技术投机 | 趋势交易 | 短期交易机会 |
| **雷·达利欧** | 全天候策略 | 经济周期+风险平价 | 资产配置 |
| **约翰·聂夫** | 低市盈率 | 高股息+低估值 | 价值回归 |
| **约翰·博格** | 指数投资 | 低成本+分散化 | 长期投资 |
| **卡尔·伊坎** | 激进投资 | 价值释放 | 低效企业 |
| **菲利普·费雪** | 成长股 | 优秀管理层+创新 | 长期成长股 |

### 使用方法

#### 1. Web 界面（推荐）
```bash
# 启动 Gradio 应用
python app.py
# 或使用启动脚本
start.bat  # Windows
./start.sh # Linux/Mac

# 访问 http://localhost:7860
```

**界面功能**：
- **单一视角分析**：选择一位投资大师，输入材料，获得分析
- **多视角对比**：同时从多位大师角度分析，生成对比总结
- **历史记录**：查看所有分析历史，支持搜索和筛选
- **统计信息**：查看分析统计数据

详细使用说明见 [Gradio 界面使用指南](docs/gradio_guide.md)

#### 2. 命令行测试
```python
# 测试投资者画像管理
python analysis/investor_profiles.py

# 运行完整测试套件
python scripts/test_multi_perspective.py
```

#### 2. Python代码调用
```python
from analysis.perspective_analyzer import PerspectiveAnalyzer

# 初始化分析器
analyzer = PerspectiveAnalyzer(llm_provider="deepseek")

# 准备分析材料
material = """
公司：XX科技
市盈率：35倍
ROE：18%
营收增长：30%
...
"""

# 单一视角分析
result = analyzer.analyze_from_perspective(
    material=material,
    investor_id='buffett'  # 使用巴菲特的视角
)
print(result['analysis'])

# 多视角对比分析
comparison = analyzer.compare_perspectives(
    material=material,
    investor_ids=['buffett', 'lynch', 'graham']
)
print(comparison['comparison_summary'])
```

#### 3. 快速分析接口
```python
from analysis.perspective_analyzer import quick_analyze

# 一行代码完成分析
result = quick_analyze(
    material="茅台营收增长15%，ROE 30%...",
    investor_id="buffett"
)
```

#### 4. 历史记录查询
```python
from storage.db_manager import AnalysisRecordManager

# 初始化管理器
manager = AnalysisRecordManager()

# 查询最近10条记录
recent = manager.get_recent_analyses(limit=10)

# 搜索包含关键词的记录
results = manager.search_analyses("茅台", limit=20)

# 获取统计信息
stats = manager.get_statistics()
print(f"总分析次数: {stats['total_count']}")
```

### 功能特点
- ✅ **10位投资大师画像**：每位大师都有详细的投资理念、决策标准、分析焦点
- ✅ **智能提示词工程**：根据投资者特点自动生成专业分析提示词
- ✅ **多视角对比**：同时从多个角度分析，识别共识与分歧
- ✅ **灵活LLM支持**：支持DeepSeek、千问、智谱、GPT、Claude
- ✅ **可扩展架构**：易于添加新的投资者画像

### 文件结构
```
├── 🆕 api/                         # FastAPI 后端 API
│   ├── main.py                     # 应用入口
│   ├── routers/                    # API 路由（分析、记录、投资者）
│   ├── services/                   # 业务逻辑层
│   └── models/                     # 数据模型
├── 🆕 frontend/                    # Vue3 前端工程
│   ├── src/                        # 源代码
│   │   ├── views/                  # 页面组件
│   │   ├── api/                    # API 客户端
│   │   └── components/             # 可复用组件
│   ├── package.json                # npm 依赖
│   └── vite.config.ts             # Vite 配置
├── app.py                          # Gradio 应用（保留）
├── analysis/                       # 核心分析模块
│   ├── investor_profiles.py        # 投资者画像管理
│   └── perspective_analyzer.py     # 多视角分析引擎
├── storage/                        # 数据存储模块
│   └── db_manager.py              # MongoDB 管理器
├── data/
│   └── investor_profiles.json      # 投资者配置数据
├── docs/                           # 项目文档
│   ├── vue3_migration_guide.md    # 🆕 Vue3 迁移指南
│   ├── copilot_prompts.md         # 🆕 Copilot 提示词模板
│   └── PROJECT_STRUCTURE.md       # 🆕 文件结构详解
├── 🆕 docker-compose.yml          # 容器编排配置
├── 🆕 start_new.bat/sh            # 多模式启动脚本
└── scripts/                        # 测试脚本
    └── test_multi_perspective.py
```

**[查看完整文件结构说明 →](docs/PROJECT_STRUCTURE.md)**