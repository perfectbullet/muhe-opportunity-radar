# 已有材料重新分析功能

## 功能概述

该功能允许用户从历史记录中选择已经分析过的材料，使用不同的投资者视角或分析模式重新进行分析，无需重新输入材料内容。

## 主要特性

### 1. 灵活的重新分析模式
- **单一视角分析**：选择一位投资者的视角重新分析
- **多视角对比分析**：同时选择 2-10 位投资者进行对比分析

### 2. 上下文信息管理
- 保留原始分析的上下文信息
- 支持添加新的上下文信息
- 自动合并新旧上下文

### 3. 分析溯源
- 新生成的分析记录中包含原始记录ID
- 可追踪分析历史和演变过程

## 使用方法

### 方式一：从历史记录列表
1. 打开 **历史记录** 页面
2. 找到想要重新分析的记录
3. 点击 **"重新分析 🔄"** 按钮
4. 在弹出的对话框中：
   - 选择分析模式（单一视角 / 多视角对比）
   - 选择投资者
   - 可选：添加额外上下文信息
5. 点击 **"开始分析"** 按钮

### 方式二：从详情页面
1. 打开 **历史记录** 页面
2. 点击记录的 **"查看详情 →"**
3. 在详情对话框底部点击 **"使用此材料重新分析"** 按钮
4. 按照相同步骤选择投资者和分析模式

## API 端点

### POST `/api/v1/records/{record_id}/reanalyze`

重新分析已有材料

**路径参数**：
- `record_id` (string, required): 原始记录ID

**请求体**：
```json
{
  "investor_id": "lynch",
  "additional_context": "当前市场环境说明",
  "use_comparison": false,
  "investor_ids": ["buffett", "lynch", "graham"]
}
```

**请求参数说明**：
- `investor_id` (string, required): 投资者ID
- `additional_context` (string, optional): 额外的上下文信息
- `use_comparison` (boolean, optional): 是否使用多视角对比，默认 false
- `investor_ids` (array, optional): 多视角对比时的投资者ID列表（2-10个）

**响应示例（单一视角）**：
```json
{
  "record_id": "new_record_id",
  "investor_id": "lynch",
  "investor_name": "彼得·林奇",
  "analysis": "分析结果内容...",
  "created_at": "2024-01-01T12:00:00",
  "metadata": {
    "reanalyzed_from": "original_record_id",
    "original_investor": "buffett"
  }
}
```

**响应示例（多视角对比）**：
```json
{
  "record_id": "comparison_record_id",
  "investor_ids": ["buffett", "lynch", "graham"],
  "analyses": [
    {
      "investor_id": "buffett",
      "investor_name": "沃伦·巴菲特",
      "analysis": "分析内容..."
    },
    // ... 更多投资者分析
  ],
  "comparison_summary": "综合对比总结...",
  "created_at": "2024-01-01T12:00:00"
}
```

## 使用场景

### 场景 1：市场环境变化
当市场环境发生变化（如从牛市转为熊市），可以重新分析同一材料，添加新的市场环境信息：

```python
# 原分析：牛市环境
# 重新分析：添加熊市环境上下文
reanalyze_request = {
    "investor_id": "buffett",
    "additional_context": "当前市场已转为熊市，估值大幅下降"
}
```

### 场景 2：多角度对比
首次使用单一投资者视角分析后，想要了解其他投资者的看法：

```python
# 原分析：巴菲特视角
# 重新分析：多视角对比
reanalyze_request = {
    "investor_id": "buffett",  # 保留主要视角
    "use_comparison": True,
    "investor_ids": ["buffett", "lynch", "graham", "soros"]
}
```

### 场景 3：不同投资风格评估
使用完全不同的投资风格重新评估同一标的：

```python
# 原分析：价值投资视角（buffett）
# 重新分析：成长股视角（lynch）
reanalyze_request = {
    "investor_id": "lynch",
    "additional_context": "关注公司的成长性和市场空间"
}
```

## 代码示例

### Python 客户端
```python
import requests

# 重新分析（单一视角）
response = requests.post(
    "http://localhost:8080/api/v1/records/{record_id}/reanalyze",
    json={
        "investor_id": "lynch",
        "additional_context": "新的市场环境说明"
    }
)

result = response.json()
print(f"新分析记录ID: {result['record_id']}")
print(f"分析结果: {result['analysis']}")
```

### JavaScript/TypeScript 客户端
```typescript
import { reanalyzeMaterial } from '@/api'

// 重新分析（多视角对比）
const result = await reanalyzeMaterial(recordId, {
  investor_id: 'buffett',
  use_comparison: true,
  investor_ids: ['buffett', 'lynch', 'graham'],
  additional_context: '新的市场环境说明'
})

console.log('新分析记录:', result)
```

## 技术实现细节

### 后端实现
1. **获取原始记录**：通过 `RecordService.get_record_detail()` 获取原始分析记录
2. **提取材料**：从原始记录中提取 `material` 字段
3. **合并上下文**：将原始上下文与新上下文合并
4. **调用分析服务**：
   - 单一视角：调用 `AnalysisService.analyze_single()`
   - 多视角：调用 `AnalysisService.compare_perspectives()`
5. **元数据标记**：在返回结果中添加 `reanalyzed_from` 和 `original_investor` 标记

### 前端实现
1. **历史记录列表**：每项添加重新分析按钮
2. **重新分析对话框**：
   - 单一/多视角模式切换
   - 投资者选择器（单选/多选）
   - 上下文输入框
3. **结果处理**：分析完成后刷新列表，可选择查看新结果

## 注意事项

1. **记录必须存在**：重新分析的记录ID必须在数据库中存在
2. **材料必须完整**：原始记录必须包含完整的材料内容
3. **投资者ID有效**：所选投资者ID必须在系统配置的投资者列表中
4. **多视角限制**：多视角对比最少2位、最多10位投资者
5. **上下文合并**：新旧上下文会自动合并，避免信息丢失

## 常见问题

### Q: 重新分析会覆盖原记录吗？
A: 不会。重新分析会创建一个新的分析记录，原记录保持不变。

### Q: 可以多次重新分析同一材料吗？
A: 可以。每次重新分析都会生成独立的新记录。

### Q: 上下文信息如何处理？
A: 原始上下文会被保留，新添加的上下文会追加到原上下文后面。

### Q: 如何追踪分析历史？
A: 新记录的 `metadata.reanalyzed_from` 字段包含原记录ID，可通过此字段追溯。

### Q: 多视角分析的结果如何展示？
A: 多视角分析会包含每位投资者的独立分析结果和一个综合对比总结。

## 未来改进方向

1. **批量重新分析**：支持选择多个记录批量重新分析
2. **分析链可视化**：图形化展示材料的分析历史和演变
3. **智能推荐**：根据材料特点自动推荐合适的投资者视角
4. **差异对比**：高亮显示不同分析结果之间的差异
5. **分析版本管理**：为同一材料的多次分析建立版本管理系统
