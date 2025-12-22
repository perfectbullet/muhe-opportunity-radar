"""记录服务 - 历史记录管理"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from typing import List, Dict, Any, Optional
from storage.db_manager import AnalysisRecordManager


class RecordService:
    """历史记录服务类"""
    
    def __init__(self):
        self.manager = AnalysisRecordManager()
    
    async def get_recent_records(
        self,
        limit: int = 20,
        investor_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """获取最近记录"""
        records = self.manager.get_recent_analyses(
            limit=limit,
            investor_id=investor_filter
        )
        
        # 格式化记录，添加预览
        formatted_records = []
        for record in records:
            formatted = {
                "record_id": str(record.get("_id", "")),
                "type": record.get("type", "single"),
                "material": record.get("material", ""),
                "created_at": record.get("created_at"),
            }
            
            # 根据类型添加不同字段
            if record.get("type") == "comparison":
                formatted["investor_names"] = [
                    a.get("investor_name") for a in record.get("analyses", [])
                ]
                # 预览第一个分析结果
                preview = record.get("analyses", [{}])[0].get("analysis", "")[:200]
            else:
                formatted["investor_name"] = record.get("investor_name", "")
                preview = record.get("analysis_result", "")[:200]
            
            formatted["preview"] = preview + "..." if len(preview) == 200 else preview
            formatted_records.append(formatted)
        
        return formatted_records
    
    async def get_record_detail(self, record_id: str) -> Optional[Dict[str, Any]]:
        """获取记录详情"""
        return self.manager.get_analysis_by_id(record_id)
    
    async def search_records(
        self,
        keyword: str,
        limit: int = 20,
        investor_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """搜索记录"""
        # 首先搜索
        records = self.manager.search_analyses(keyword=keyword, limit=limit)
        
        # 如果有投资者过滤，进一步筛选
        if investor_filter:
            records = [
                r for r in records
                if r.get("investor_id") == investor_filter or
                   investor_filter in [a.get("investor_id") for a in r.get("analyses", [])]
            ]
        
        # 格式化输出（复用 get_recent_records 的逻辑）
        formatted_records = []
        for record in records:
            formatted = {
                "record_id": str(record.get("_id", "")),
                "type": record.get("type", "single"),
                "material": record.get("material", ""),
                "created_at": record.get("created_at"),
            }
            
            if record.get("type") == "comparison":
                formatted["investor_names"] = [
                    a.get("investor_name") for a in record.get("analyses", [])
                ]
                preview = record.get("analyses", [{}])[0].get("analysis", "")[:200]
            else:
                formatted["investor_name"] = record.get("investor_name", "")
                preview = record.get("analysis_result", "")[:200]
            
            formatted["preview"] = preview + "..." if len(preview) == 200 else preview
            formatted_records.append(formatted)
        
        return formatted_records
    
    async def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.manager.get_statistics()


# 全局服务实例
_record_service = None


def get_record_service() -> RecordService:
    """获取记录服务实例（单例模式）"""
    global _record_service
    if _record_service is None:
        _record_service = RecordService()
    return _record_service
