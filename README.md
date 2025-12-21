# Muhe Opportunity Radar
## 项目简介
Muhe Opportunity Radar（穆和机会雷达）是一款基于信息聚合与AI分析的投资机会挖掘工具，核心功能为聚合多源投资相关数据，通过AI模型分析识别潜在投资机会并进行风险提示。

## 核心特性
1. **多源数据聚合**：支持股票数据、行业新闻、财务报表等结构化/非结构化数据采集
2. **AI智能分析**：基于大模型实现趋势识别、机会筛选、风险预警
3. **🎯 多投资理念视角**：模拟10位投资大师的思维方式，从不同角度分析同一投资标的
   - 巴菲特（价值投资）、格雷厄姆（量化价值）、索罗斯（宏观对冲）
   - 彼得·林奇（成长股）、利弗莫尔（技术分析）、达利欧（全天候策略）
   - 约翰·聂夫（低市盈率）、博格（指数投资）、伊坎（激进投资）、费雪（成长股）
4. **可视化展示**：提供投资机会清单、数据趋势图等可视化功能
## 快速启动

### 环境依赖
- Python 3.8+
- 依赖包：requirements.txt

### 安装步骤
1. 克隆仓库：`git clone <远程仓库地址>`
2. 安装依赖：`pip install -r requirements.txt`
3. 配置环境变量：创建 `.env` 文件，配置API密钥
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key
   TUSHARE_TOKEN=your_tushare_token
   ```
4. 启动服务：`streamlit run app.py` 或 `python app.py`

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

#### 1. 命令行测试
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

### 功能特点
- ✅ **10位投资大师画像**：每位大师都有详细的投资理念、决策标准、分析焦点
- ✅ **智能提示词工程**：根据投资者特点自动生成专业分析提示词
- ✅ **多视角对比**：同时从多个角度分析，识别共识与分歧
- ✅ **灵活LLM支持**：支持DeepSeek、千问、智谱、GPT、Claude
- ✅ **可扩展架构**：易于添加新的投资者画像

### 文件结构
```
├── data/
│   └── investor_profiles.json      # 投资者画像配置库
├── analysis/
│   ├── investor_profiles.py        # 投资者画像管理模块
│   └── perspective_analyzer.py     # 多视角分析引擎
└── scripts/
    └── test_multi_perspective.py   # 测试脚本
```