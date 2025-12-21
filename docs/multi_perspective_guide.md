# 多投资理念分析功能使用指南

## 快速开始

### 1. 安装依赖
```bash
pip install langchain langchain-openai langchain-community
```

### 2. 配置环境变量
在项目根目录创建 `.env` 文件：
```
DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 运行测试
```bash
# 测试投资者画像管理
python analysis/investor_profiles.py

# 运行完整测试套件
python scripts/test_multi_perspective.py
```

## 使用示例

### 示例1：单一视角分析
```python
from analysis.perspective_analyzer import PerspectiveAnalyzer

# 初始化分析器
analyzer = PerspectiveAnalyzer(llm_provider="deepseek")

# 分析材料
material = """
【投资标的】贵州茅台
- 市值：2.3万亿
- 市盈率：32倍
- ROE：30%
- 负债率：15%
- 毛利率：91%
"""

# 从巴菲特的视角分析
result = analyzer.analyze_from_perspective(
    material=material,
    investor_id='buffett'
)

print(f"投资者：{result['investor_name']}")
print(f"分析：{result['analysis']}")
```

### 示例2：多视角对比分析
```python
from analysis.perspective_analyzer import PerspectiveAnalyzer

analyzer = PerspectiveAnalyzer(llm_provider="deepseek")

material = """
【新能源汽车】比亚迪
- 营收增长：38%
- 销量：80万辆
- 海外收入占比：15%
- 技术突破：新一代电池
"""

# 从三位大师的视角对比分析
comparison = analyzer.compare_perspectives(
    material=material,
    investor_ids=['buffett', 'lynch', 'fisher']
)

# 查看各投资者的分析
for analysis in comparison['analyses']:
    print(f"\n{'='*60}")
    print(f"{analysis['investor_name']} 的观点：")
    print(analysis['analysis'])

# 查看综合对比
print(f"\n{'='*60}")
print("综合对比：")
print(comparison['comparison_summary'])
```

### 示例3：快速分析
```python
from analysis.perspective_analyzer import quick_analyze

# 一行代码完成分析
result = quick_analyze(
    material="某科技公司营收增长30%，但利润率下降...",
    investor_id="lynch",  # 使用彼得·林奇的视角
    llm_provider="deepseek"
)

print(result)
```

### 示例4：查看可用投资者
```python
from analysis.investor_profiles import InvestorProfileManager

manager = InvestorProfileManager()

# 显示所有投资者
manager.print_profiles_summary()

# 搜索特定风格的投资者
value_investors = manager.search_profiles('价值投资')
for investor in value_investors:
    print(investor)

# 按风险偏好筛选
low_risk = manager.get_profiles_by_risk('低')
for investor in low_risk:
    print(f"{investor.name} - {investor.holding_period}")
```

### 示例5：自定义分析
```python
from analysis.perspective_analyzer import PerspectiveAnalyzer

analyzer = PerspectiveAnalyzer(llm_provider="deepseek")

material = "..."
additional_context = """
行业背景：
- 行业增速放缓
- 竞争加剧
- 政策支持
"""

# 添加额外上下文信息
result = analyzer.analyze_from_perspective(
    material=material,
    investor_id='dalio',  # 达利欧擅长宏观分析
    additional_context=additional_context
)
```

## 支持的投资者列表

| ID | 名称 | 风格 | 适用场景 |
|----|------|------|---------|
| `buffett` | 沃伦·巴菲特 | 价值投资 | 优质企业长期持有 |
| `graham` | 本杰明·格雷厄姆 | 量化价值 | 严格财务筛选 |
| `soros` | 乔治·索罗斯 | 宏观对冲 | 趋势转折判断 |
| `lynch` | 彼得·林奇 | 成长价值 | 成长股投资 |
| `livermore` | 杰西·利弗莫尔 | 技术交易 | 短期交易 |
| `dalio` | 雷·达利欧 | 全天候策略 | 资产配置 |
| `neff` | 约翰·聂夫 | 低市盈率 | 低估值股票 |
| `bogle` | 约翰·博格 | 指数投资 | 被动投资 |
| `icahn` | 卡尔·伊坎 | 激进投资 | 价值释放 |
| `fisher` | 菲利普·费雪 | 成长股 | 长期成长股 |

## 支持的LLM提供商

```python
# DeepSeek（推荐，性价比高）
analyzer = PerspectiveAnalyzer(llm_provider="deepseek")

# 千问
analyzer = PerspectiveAnalyzer(llm_provider="qwen")

# 智谱
analyzer = PerspectiveAnalyzer(llm_provider="zhipu")

# OpenAI
analyzer = PerspectiveAnalyzer(llm_provider="openai")
```

需要在 `.env` 中配置对应的API密钥：
```
DEEPSEEK_API_KEY=...
QWEN_API_KEY=...
ZHIPU_API_KEY=...
OPENAI_API_KEY=...
```

## 常见问题

### Q1: 如何添加新的投资者？
编辑 `data/investor_profiles.json`，按照现有格式添加新的投资者画像。

### Q2: 如何调整分析的详细程度？
修改 `PerspectiveAnalyzer` 的 `temperature` 参数：
```python
analyzer = PerspectiveAnalyzer(
    llm_provider="deepseek",
    temperature=0.3  # 更确定性，0.7更有创造性
)
```

### Q3: 分析失败怎么办？
1. 检查API密钥是否正确配置
2. 检查网络连接
3. 查看错误信息：`result['error']`

### Q4: 如何批量分析多个标的？
```python
stocks = ['茅台', '比亚迪', '宁德时代']
for stock in stocks:
    material = f"分析{stock}..."
    result = quick_analyze(material, 'buffett')
    print(f"{stock}: {result}")
```

## 进阶用法

### 自定义提示词模板
```python
from analysis.investor_profiles import InvestorProfile

# 获取投资者画像
profile = analyzer.profile_manager.get_profile('buffett')

# 修改系统提示词
custom_prompt = profile.get_system_prompt()
custom_prompt += "\n请特别关注ESG因素..."

# 使用自定义提示词（需要直接调用LLM）
```

### 结果保存和导出
```python
import json

comparison = analyzer.compare_perspectives(...)

# 保存为JSON
with open('analysis_result.json', 'w', encoding='utf-8') as f:
    json.dump(comparison, f, ensure_ascii=False, indent=2)

# 生成Markdown报告
with open('report.md', 'w', encoding='utf-8') as f:
    f.write(f"# 投资分析报告\n\n")
    for analysis in comparison['analyses']:
        f.write(f"## {analysis['investor_name']}\n\n")
        f.write(f"{analysis['analysis']}\n\n")
```

## 性能优化

### 并行分析（适用于多标的）
```python
from concurrent.futures import ThreadPoolExecutor

def analyze_stock(stock_data):
    analyzer = PerspectiveAnalyzer(llm_provider="deepseek")
    return analyzer.analyze_from_perspective(
        material=stock_data,
        investor_id='buffett'
    )

stocks = [stock1_data, stock2_data, stock3_data]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(analyze_stock, stocks))
```

### 缓存结果
```python
import hashlib
import pickle

def get_cache_key(material, investor_id):
    content = f"{material}_{investor_id}"
    return hashlib.md5(content.encode()).hexdigest()

def cached_analyze(material, investor_id):
    cache_key = get_cache_key(material, investor_id)
    cache_file = f"cache/{cache_key}.pkl"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    result = analyzer.analyze_from_perspective(material, investor_id)
    
    with open(cache_file, 'wb') as f:
        pickle.dump(result, f)
    
    return result
```

## 贡献指南

欢迎贡献新的投资者画像！请确保包含：
- 投资哲学描述
- 核心投资原则（至少5条）
- 分析关注点（至少7个）
- 买入/避免信号
- 提示词模板

提交PR到项目仓库即可。
