# Gradio 前端界面使用指南

## 界面概览

Muhe Opportunity Radar 现已集成 Gradio 前端界面，提供以下功能：

### 1. 📝 单一视角分析
从单个投资大师的视角分析投资标的。

**功能特点**：
- 输入投资材料（财报、新闻、基本面数据等）
- 可选添加额外上下文信息
- 从10位投资大师中选择一位
- 获得该投资者风格的专业分析

**使用场景**：
- 想了解巴菲特会如何评价这家公司
- 想知道索罗斯会看到什么宏观趋势
- 想听听彼得·林奇对成长性的看法

### 2. 🔄 多视角对比分析
同时从多位投资大师的视角分析同一标的，并生成对比总结。

**功能特点**：
- 支持同时选择多位投资者
- 展示每位投资者的独立分析
- AI 自动生成对比总结，包括：
  - 共识观点
  - 分歧观点
  - 互补视角
  - 综合建议

**使用场景**：
- 全面评估一个投资标的
- 发现不同视角的盲点
- 平衡激进与保守观点

### 3. 📚 历史记录
查看和管理所有历史分析记录。

**功能特点**：
- 显示最近的分析记录
- 按投资者筛选记录
- 关键词搜索功能
- 查看材料摘要和分析长度

**使用场景**：
- 回顾之前的分析
- 查找特定公司的历史分析
- 追踪分析频率

### 4. 📊 统计信息
展示分析记录的统计数据。

**功能特点**：
- 总记录数统计
- 按投资者分类统计
- 按分析类型统计

**使用场景**：
- 了解使用习惯
- 发现常用投资者
- 追踪分析数量

## 快速启动

### 方法1：使用启动脚本（推荐）

**Windows**:
```bash
start.bat
```

**Linux/Mac**:
```bash
chmod +x start.sh
./start.sh
```

### 方法2：直接运行

```bash
# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 启动应用
python app.py
```

### 方法3：不使用虚拟环境

```bash
python app.py
```

## 访问地址

启动成功后，在浏览器中访问：
- **本地访问**: http://localhost:7860
- **局域网访问**: http://your-ip:7860

## 界面预览

### 单一视角分析页面
```
┌─────────────────────────────────────┐
│  投资材料输入框                      │
│  (多行文本输入)                      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  额外上下文（可选）                  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  选择投资者 ▼                        │
│  沃伦·巴菲特 - 价值投资之父          │
└─────────────────────────────────────┘

        [ 🚀 开始分析 ]

┌─────────────────────────────────────┐
│  分析结果展示区                      │
│  (Markdown 格式)                     │
└─────────────────────────────────────┘
```

### 多视角对比页面
```
┌─────────────────────────────────────┐
│  投资材料输入框                      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  选择投资者（可多选）                │
│  ☑ 沃伦·巴菲特                       │
│  ☑ 彼得·林奇                         │
│  ☐ 乔治·索罗斯                       │
│  ...                                 │
└─────────────────────────────────────┘

      [ 🚀 开始对比分析 ]

┌─────────────────────────────────────┐
│  对比分析结果                        │
│  1. 巴菲特的分析                     │
│  2. 林奇的分析                       │
│  3. 综合对比总结                     │
└─────────────────────────────────────┘
```

## 使用示例

### 示例1：分析茅台
```
投资材料：
茅台酒业：市值2.3万亿，PE 32倍，ROE 30%，
毛利率91%，品牌护城河强，供不应求。
风险：估值偏高，消费降级影响。

选择投资者：沃伦·巴菲特

结果：巴菲特会关注护城河、高ROE和定价权...
```

### 示例2：对比分析科技公司
```
投资材料：
某AI公司Q3营收增长50%，但亏损扩大，
烧钱抢市场，技术领先但竞争激烈。

选择投资者：
☑ 巴菲特（价值投资）
☑ 彼得·林奇（成长股）
☑ 卡尔·伊坎（激进投资）

结果：
- 巴菲特：担心盈利模式不清晰
- 林奇：看好成长性，关注PEG
- 伊坎：建议催化剂事件
- 综合：各有侧重，需权衡风险
```

## 技术特性

### 1. 自动保存
- 所有分析自动保存到 MongoDB（如已启动）
- 支持降级模式（MongoDB 未启动时仍可使用）

### 2. 实时分析
- 流式输出（LLM 支持时）
- 即时反馈分析进度

### 3. 响应式设计
- 适配桌面和移动端
- 深色/浅色主题切换

### 4. 错误处理
- 友好的错误提示
- 详细的调试信息（开发模式）

## 配置说明

### 环境变量配置

确保 `.env` 文件包含必要配置：

```bash
# LLM 配置
SILICONFLOW_API_KEY=your_key_here
SILICONFLOW_MODEL=deepseek-ai/DeepSeek-V3.1-Terminus
SILICONFLOW_API_BASE_URL=https://api.siliconflow.cn/v1

# MongoDB 配置（可选）
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=muhe_opportunity_radar

# 其他 LLM 提供商
DEEPSEEK_API_KEY=your_key
QWEN_API_KEY=your_key
ZHIPU_API_KEY=your_key
```

### 修改默认 LLM 提供商

编辑 `app.py` 第33行：

```python
def init_analyzer(provider: str = "siliconflow"):  # 修改这里
```

可选值：`deepseek`, `qwen`, `zhipu`, `openai`, `claude`, `siliconflow`

### 修改端口号

编辑 `app.py` 最后几行：

```python
app.launch(
    server_name="0.0.0.0",
    server_port=7860,  # 修改这里
    share=False,
    show_error=True
)
```

### 启用公网访问

将 `share=False` 改为 `share=True`，Gradio 会生成临时公网链接。

## 常见问题

### Q1: 启动时提示 MongoDB 连接失败？
**A**: 这是正常的，应用会自动降级到无数据库模式。如需历史记录功能，请启动 MongoDB 服务。

### Q2: 分析速度慢？
**A**: 
- 检查网络连接
- 尝试切换到更快的 LLM 提供商
- 减少分析材料长度

### Q3: 如何添加新的投资者？
**A**: 编辑 `data/investor_profiles.json` 文件，参考现有格式添加。

### Q4: 历史记录在哪里？
**A**: 存储在 MongoDB 的 `analysis_records` 集合中。

### Q5: 可以同时运行多个实例吗？
**A**: 可以，但需要修改端口号避免冲突。

## 性能优化建议

### 1. 使用本地 LLM（可选）
- 部署 Ollama 本地模型
- 修改配置使用本地 API

### 2. MongoDB 索引优化
- 系统已自动创建索引
- 大量数据时考虑分片

### 3. 缓存机制
- 相同材料+投资者的分析结果可缓存
- 减少重复 API 调用

## 开发扩展

### 添加新功能

1. **导出PDF报告**
```python
def export_to_pdf(analysis_result):
    # 使用 reportlab 生成 PDF
    pass
```

2. **数据可视化**
```python
import plotly.graph_objects as go
# 添加图表展示
```

3. **对比多个时间点的分析**
```python
def compare_historical_analyses(company, dates):
    # 对比不同时期的分析变化
    pass
```

## 部署建议

### Docker 部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["python", "app.py"]
```

### docker-compose.yml

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./data:/app/data
    env_file:
      - .env
    depends_on:
      - mongodb
  
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

启动：
```bash
docker-compose up -d
```

## 反馈与支持

如有问题或建议，请通过以下方式反馈：
- 提交 Issue
- Pull Request
- 邮件联系

---

**享受使用炑禾机会雷达！** 🎯✨
