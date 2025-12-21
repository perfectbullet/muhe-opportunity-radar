# MongoDB 集成说明

## 功能概述

项目已集成 MongoDB 数据库，用于保存和管理投资分析历史记录。这使得你可以：

- 📊 保存所有分析历史
- 🔍 搜索和查询过往分析
- 📈 查看分析统计和趋势
- 🕐 追踪分析时间线
- 🎯 按投资者筛选历史记录

## 工作模式

### 1. 完整模式（推荐）
当 MongoDB 服务运行时：
- ✅ 自动保存所有分析记录
- ✅ 支持历史查询和搜索
- ✅ 提供统计分析功能

### 2. 降级模式（默认）
当 MongoDB 未运行时：
- ✅ 核心分析功能正常工作
- ⚠️ 分析记录不会持久化
- ℹ️ 会显示友好提示信息

**系统会自动检测 MongoDB 状态并选择合适的模式，无需手动配置。**

## MongoDB 安装（可选）

### Windows

1. **下载 MongoDB Community Server**
   - 访问：https://www.mongodb.com/try/download/community
   - 选择：Windows 版本
   - 下载并安装

2. **启动服务**
   ```powershell
   # 以管理员身份运行 PowerShell
   net start MongoDB
   ```

3. **验证安装**
   ```powershell
   mongosh --version
   ```

### macOS

```bash
# 使用 Homebrew 安装
brew tap mongodb/brew
brew install mongodb-community

# 启动服务
brew services start mongodb-community

# 验证
mongosh --version
```

### Linux (Ubuntu/Debian)

```bash
# 导入 MongoDB 公钥
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# 添加源
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# 安装
sudo apt-get update
sudo apt-get install -y mongodb-org

# 启动
sudo systemctl start mongod
sudo systemctl enable mongod

# 验证
mongosh --version
```

## 配置说明

MongoDB 连接配置在 `.env` 文件中：

```env
# MongoDB 配置
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=muhe_opportunity_radar
MONGODB_MAX_POOL_SIZE=100
MONGODB_MIN_POOL_SIZE=10
```

**默认配置已经可以正常工作，通常无需修改。**

## 使用示例

### 1. 基本使用（自动保存）

```python
from analysis.perspective_analyzer import PerspectiveAnalyzer

# 创建分析器（默认启用数据库）
analyzer = PerspectiveAnalyzer(llm_provider='siliconflow')

# 分析会自动保存到数据库
result = analyzer.analyze_from_perspective(
    material="某公司财报...",
    investor_id="buffett"
)
```

### 2. 禁用数据库保存

```python
# 如果不想保存到数据库
analyzer = PerspectiveAnalyzer(
    llm_provider='siliconflow',
    enable_db=False  # 禁用数据库
)
```

### 3. 查询历史记录

```python
from storage.db_manager import AnalysisRecordManager

manager = AnalysisRecordManager()

# 获取最近10条记录
recent = manager.get_recent_analyses(limit=10)

# 按投资者筛选
buffett_analyses = manager.get_recent_analyses(
    limit=20,
    investor_id="buffett"
)

# 搜索关键词
results = manager.search_analyses("茅台", limit=10)

# 获取统计信息
stats = manager.get_statistics()
print(f"总记录数: {stats['total_count']}")
```

## 数据结构

### 单次分析记录
```json
{
  "_id": "...",
  "material": "投资材料内容",
  "investor_id": "buffett",
  "investor_name": "沃伦·巴菲特",
  "analysis_result": "分析结果...",
  "additional_context": "额外上下文",
  "metadata": {
    "investor_title": "股神、价值投资代表",
    "risk_tolerance": "低",
    "holding_period": "超长期",
    "llm_provider": "siliconflow",
    "temperature": 0.7
  },
  "created_at": "2024-12-21T10:30:00Z",
  "material_length": 1234,
  "analysis_length": 5678
}
```

### 对比分析记录
```json
{
  "_id": "...",
  "type": "comparison",
  "material": "投资材料内容",
  "investor_ids": ["buffett", "graham", "lynch"],
  "investor_count": 3,
  "analyses": [...],
  "comparison_summary": "综合对比总结...",
  "created_at": "2024-12-21T10:30:00Z"
}
```

## 测试命令

```bash
# 测试 MongoDB 连接和功能
python scripts/test_mongodb.py

# 测试集成功能（降级模式）
python scripts/test_db_integration.py

# 运行完整的多视角分析测试
python scripts/test_multi_perspective.py
```

## 常见问题

### Q: MongoDB 未安装，能用吗？
**A:** 完全可以！系统会自动切换到降级模式，核心功能不受影响。

### Q: 如何知道数据库是否连接？
**A:** 启动时会显示提示信息：
- `✓ 已连接到 MongoDB` - 数据库已连接
- `⚠️ MongoDB 未连接，跳过保存` - 降级模式

### Q: 数据保存在哪里？
**A:** 
- 数据库：`muhe_opportunity_radar`
- 集合：`analysis_records`
- 默认位置：`localhost:27017`

### Q: 如何备份数据？
**A:** 使用 MongoDB 工具：
```bash
# 备份
mongodump --db=muhe_opportunity_radar --out=backup/

# 恢复
mongorestore --db=muhe_opportunity_radar backup/muhe_opportunity_radar/
```

### Q: 如何清空历史记录？
**A:** 使用 mongosh：
```bash
mongosh
use muhe_opportunity_radar
db.analysis_records.deleteMany({})
```

## 性能优化

数据库已自动创建以下索引以提高查询性能：
- `created_at` (降序) - 快速获取最新记录
- `investor_id` - 按投资者筛选
- `investor_id + created_at` - 复合查询

## 未来功能

计划中的功能：
- 📊 分析结果可视化面板
- 📈 投资观点趋势分析
- 🔄 分析结果对比工具
- 📤 导出分析报告（PDF/Excel）
- 🤖 基于历史的 AI 推荐

## 技术支持

如有问题，请检查：
1. MongoDB 服务是否运行
2. 端口 27017 是否被占用
3. `.env` 配置是否正确
4. 防火墙设置

更多信息请参考：
- [MongoDB 官方文档](https://docs.mongodb.com/)
- [PyMongo 文档](https://pymongo.readthedocs.io/)
