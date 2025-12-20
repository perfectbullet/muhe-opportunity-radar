# Muhe Opportunity Radar
## 项目简介
Muhe Opportunity Radar（穆和机会雷达）是一款基于信息聚合与AI分析的投资机会挖掘工具，核
心功能为聚合多源投资相关数据，通过AI模型分析识别潜在投资机会并进行风险提示。
## 核心特性
1. 多源数据聚合：支持股票数据、行业新闻、财务报表等结构化/非结构化数据采集
2. AI智能分析：基于大模型实现趋势识别、机会筛选、风险预警
3. 可视化展示：提供投资机会清单、数据趋势图等可视化功能
## 快速启动
### 环境依赖
- Python 3.8+
- 依赖包：requirements.txt
### 安装步骤
1. 克隆仓库：git clone <远程仓库地址>
2. 安装依赖：pip install -r requirements.txt
3. 配置数据源：修改config.py中的API密钥、数据库连接信息
4. 启动服务：streamlit run app.py