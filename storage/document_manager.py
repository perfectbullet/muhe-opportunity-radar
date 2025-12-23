"""
MongoDB 文档和报告管理扩展
用于保存和查询文档解析、财务指标、分析报告
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from bson import ObjectId

from storage.db_manager import AnalysisRecordManager


class DocumentManager:
    """文档管理器 - 扩展 AnalysisRecordManager"""
    
    def __init__(self):
        """初始化管理器"""
        self.db_manager = AnalysisRecordManager()
        self.documents_collection = self.db_manager.db["documents"]
        self.metrics_collection = self.db_manager.db["financial_metrics"]
        self.reports_collection = self.db_manager.db["analysis_reports"]
    
    # ==================== 文档相关 ====================
    
    async def save_document(
        self,
        document_id: str,
        filename: str,
        content: str,
        format: str,
        markdown_content: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        保存解析后的文档
        
        Args:
            document_id: 文档唯一ID
            filename: 文件名
            content: 原始文本内容
            format: 文档格式（pdf/word/markdown）
            markdown_content: 转换后的 Markdown 内容
            metadata: 元数据
            
        Returns:
            MongoDB 记录ID
        """
        document = {
            "document_id": document_id,
            "filename": filename,
            "content": content,
            "format": format,
            "markdown_content": markdown_content or content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "content_length": len(content),
            "status": "parsed"
        }
        
        result = await self.documents_collection.insert_one(document)
        return str(result.inserted_id)
    
    async def get_document(self, document_id: str) -> Optional[Dict]:
        """获取文档详情"""
        document = await self.documents_collection.find_one({"document_id": document_id})
        
        if document:
            document["_id"] = str(document["_id"])
            return document
        return None
    
    async def get_document_markdown(self, document_id: str) -> Optional[str]:
        """获取文档的 Markdown 内容"""
        document = await self.get_document(document_id)
        return document.get("markdown_content") if document else None
    
    async def list_documents(
        self,
        limit: int = 50,
        skip: int = 0,
        format_filter: Optional[str] = None
    ) -> List[Dict]:
        """列出所有文档"""
        query = {}
        if format_filter:
            query["format"] = format_filter
        
        cursor = self.documents_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        
        return documents
    
    async def update_document_status(self, document_id: str, status: str) -> bool:
        """更新文档状态"""
        result = await self.documents_collection.update_one(
            {"document_id": document_id},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    # ==================== 财务指标相关 ====================
    
    async def save_metrics(
        self,
        document_id: str,
        metrics: Dict[str, Any],
        summary: Optional[Dict] = None
    ) -> str:
        """保存计算的财务指标"""
        metrics_record = {
            "document_id": document_id,
            "metrics": metrics,
            "summary": summary or {},
            "created_at": datetime.utcnow(),
            "metrics_count": sum(1 for v in metrics.values() if v is not None)
        }
        
        result = await self.metrics_collection.insert_one(metrics_record)
        return str(result.inserted_id)
    
    async def get_metrics(self, document_id: str) -> Optional[Dict]:
        """获取文档的财务指标"""
        metrics = await self.metrics_collection.find_one(
            {"document_id": document_id},
            sort=[("created_at", -1)]
        )
        
        if metrics:
            metrics["_id"] = str(metrics["_id"])
            return metrics
        return None
    
    async def list_metrics(
        self,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """列出所有财务指标记录"""
        cursor = self.metrics_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        metrics_list = await cursor.to_list(length=limit)
        
        for metrics in metrics_list:
            metrics["_id"] = str(metrics["_id"])
        
        return metrics_list
    
    # ==================== 分析报告相关 ====================
    
    async def save_report(
        self,
        document_id: str,
        investor_id: str,
        investor_name: str,
        report_markdown: str,
        structured_data: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """保存分析报告"""
        report = {
            "document_id": document_id,
            "investor_id": investor_id,
            "investor_name": investor_name,
            "report_markdown": report_markdown,
            "structured_data": structured_data or {},
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "report_length": len(report_markdown)
        }
        
        result = await self.reports_collection.insert_one(report)
        return str(result.inserted_id)
    
    async def get_report(self, report_id: str) -> Optional[Dict]:
        """获取报告详情（通过报告ID）"""
        try:
            report = await self.reports_collection.find_one({"_id": ObjectId(report_id)})
            if report:
                report["_id"] = str(report["_id"])
                return report
        except:
            pass
        return None
    
    async def get_report_by_document(
        self,
        document_id: str,
        investor_id: Optional[str] = None
    ) -> Optional[Dict]:
        """获取文档的分析报告"""
        query = {"document_id": document_id}
        if investor_id:
            query["investor_id"] = investor_id
        
        report = await self.reports_collection.find_one(
            query,
            sort=[("created_at", -1)]
        )
        
        if report:
            report["_id"] = str(report["_id"])
            return report
        return None
    
    async def list_reports(
        self,
        limit: int = 50,
        skip: int = 0,
        investor_filter: Optional[str] = None,
        document_filter: Optional[str] = None
    ) -> List[Dict]:
        """列出所有报告"""
        query = {}
        if investor_filter:
            query["investor_id"] = investor_filter
        if document_filter:
            query["document_id"] = document_filter
        
        cursor = self.reports_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        reports = await cursor.to_list(length=limit)
        
        for report in reports:
            report["_id"] = str(report["_id"])
        
        return reports
    
    async def search_reports(
        self,
        keyword: str,
        limit: int = 20
    ) -> List[Dict]:
        """搜索报告（全文搜索）"""
        query = {
            "$or": [
                {"report_markdown": {"$regex": keyword, "$options": "i"}},
                {"investor_name": {"$regex": keyword, "$options": "i"}}
            ]
        }
        
        cursor = self.reports_collection.find(query).sort("created_at", -1).limit(limit)
        reports = await cursor.to_list(length=limit)
        
        for report in reports:
            report["_id"] = str(report["_id"])
        
        return reports
    
    # ==================== 综合查询 ====================
    
    async def get_document_full_info(self, document_id: str) -> Optional[Dict]:
        """获取文档的完整信息（文档+指标+报告）"""
        document = await self.get_document(document_id)
        if not document:
            return None
        
        metrics = await self.get_metrics(document_id)
        reports = await self.list_reports(document_filter=document_id, limit=10)
        
        return {
            "document": document,
            "metrics": metrics,
            "reports": reports
        }
    
    async def get_statistics(self) -> Dict:
        """获取统计信息"""
        documents_count = await self.documents_collection.count_documents({})
        metrics_count = await self.metrics_collection.count_documents({})
        reports_count = await self.reports_collection.count_documents({})
        
        # 按投资者统计报告数
        pipeline = [
            {"$group": {"_id": "$investor_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        by_investor = await self.reports_collection.aggregate(pipeline).to_list(length=100)
        
        # 按格式统计文档数
        pipeline = [
            {"$group": {"_id": "$format", "count": {"$sum": 1}}}
        ]
        by_format = await self.documents_collection.aggregate(pipeline).to_list(length=10)
        
        return {
            "documents_count": documents_count,
            "metrics_count": metrics_count,
            "reports_count": reports_count,
            "by_investor": {item["_id"]: item["count"] for item in by_investor},
            "by_format": {item["_id"]: item["count"] for item in by_format}
        }
