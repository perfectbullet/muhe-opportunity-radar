# 文档管理修复说明

## 🔧 问题诊断

### 原问题
1. ❌ 上传时间显示 "Invalid Date"
2. ❌ 点击查看文档返回 404 错误

### 根本原因
- 文档上传时**仅保存到文件系统**，没有保存到 MongoDB
- 文档列表接口从文件系统读取，字段格式不统一
- 文档查看接口从 MongoDB 查询，导致找不到记录

## ✅ 修复内容

### 1. 上传时保存到 MongoDB
```python
# 在 upload_document 函数中添加
from storage.document_manager import DocumentManager
doc_manager = DocumentManager()
await doc_manager.save_document(
    document_id=document_id,
    filename=file.filename,
    content=content,
    format=parse_result.get("format", "unknown"),
    markdown_content=parse_result.get("markdown_content", content),
    metadata=parse_result.get("metadata")
)
```

### 2. 统一文档列表数据源
**改前**：从文件系统读取（`UPLOAD_DIR.iterdir()`）
**改后**：从 MongoDB 读取（`doc_manager.list_documents()`）

### 3. 统一字段格式
- ✅ `upload_time`（ISO 8601 字符串）
- ✅ `format`（不带点号，如 "pdf"）
- ✅ `size`（从 `content_length` 获取）

## 🧪 测试步骤

### 1. 重新上传文档
```bash
# 后端会自动热重载
# 前端刷新页面后，上传一个新文档
```

### 2. 验证列表显示
- ✅ 文件名正确显示
- ✅ 格式显示为 "pdf"/"word"/"md"
- ✅ 上传时间正常显示（如 "2025-12-25 14:30:00"）

### 3. 验证文档查看
- ✅ 点击"查看"按钮不再 404
- ✅ 能正常显示文档内容、指标、报告

## 📝 数据流程

```
上传文档
  ↓
保存到文件系统（data/uploads/xxx.pdf）
  ↓
解析文档内容
  ↓
保存到 MongoDB（documents 集合）
  ├─ document_id
  ├─ filename
  ├─ content
  ├─ format
  ├─ markdown_content
  └─ created_at
  ↓
返回上传成功响应
```

## 🔄 API 变化

### GET /api/v1/documents
**改前**：扫描文件系统返回
**改后**：从 MongoDB 查询返回

**响应示例**：
```json
{
  "documents": [
    {
      "document_id": "3578c618-55be-464e-b8ae-e92b62d7768d",
      "filename": "财报.pdf",
      "format": "pdf",
      "size": 1024000,
      "upload_time": "2025-12-25T14:30:00"
    }
  ],
  "total": 1
}
```

### GET /api/v1/documents/{document_id}/full
**现在可以正常工作**：
- ✅ 从 MongoDB 查询文档基本信息
- ✅ 关联查询财务指标
- ✅ 关联查询分析报告

## 💡 注意事项

### 旧文档迁移（可选）
如果之前已经上传了一些文档，它们只在文件系统中，没有在 MongoDB 中。有两个选择：

**方案1：删除重新上传（推荐）**
- 点击"删除"按钮清理旧文档
- 重新上传，自动保存到 MongoDB

**方案2：手动迁移脚本**
```python
# scripts/migrate_existing_docs.py
import asyncio
from pathlib import Path
from storage.document_manager import DocumentManager
from analysis.document_parser import DocumentParser

async def migrate():
    doc_manager = DocumentManager()
    parser = DocumentParser()
    upload_dir = Path("data/uploads")
    
    for file_path in upload_dir.iterdir():
        if file_path.is_file():
            document_id = file_path.stem
            parse_result = parser.parse(file_path)
            
            if parse_result.get("success"):
                await doc_manager.save_document(
                    document_id=document_id,
                    filename=file_path.name,
                    content=parse_result.get("content", ""),
                    format=parse_result.get("format", "unknown"),
                    markdown_content=parse_result.get("markdown_content"),
                    metadata=parse_result.get("metadata")
                )
                print(f"✓ 已迁移: {file_path.name}")

if __name__ == "__main__":
    asyncio.run(migrate())
```
