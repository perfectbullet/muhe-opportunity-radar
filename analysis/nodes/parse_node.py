"""
文档解析节点
将文档 ID 转换为结构化文本数据
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


async def parse_document_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    文档解析节点 - 从数据库读取文档并解析
    
    Args:
        state: 工作流状态，包含 document_id
        
    Returns:
        更新后的状态，添加 parsed_data 字段
    """
    from storage.db_manager import AnalysisRecordManager
    
    document_id = state.get("document_id")
    
    if not document_id:
        logger.error("缺少 document_id")
        return {
            **state,
            "error": "缺少 document_id",
            "parsed_data": None
        }
    
    try:
        # 从数据库获取文档
        db_manager = AnalysisRecordManager()
        # 这里假设有一个获取文档的方法
        # document = await db_manager.get_document(document_id)
        
        # 临时模拟数据（实际应从数据库读取）
        document = {
            "content": state.get("material", ""),
            "format": "text",
            "metadata": {}
        }
        
        # 提取关键信息
        parsed_data = {
            "raw_text": document.get("content", ""),
            "format": document.get("format", "unknown"),
            "metadata": document.get("metadata", {}),
            "length": len(document.get("content", ""))
        }
        
        logger.info(f"✓ 文档解析完成，长度: {parsed_data['length']} 字符")
        
        return {
            **state,
            "parsed_data": parsed_data,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"文档解析失败: {str(e)}")
        return {
            **state,
            "error": f"解析失败: {str(e)}",
            "parsed_data": None
        }


def parse_document_node_sync(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    同步版本的文档解析节点（用于 LangGraph）
    
    Args:
        state: 工作流状态
        
    Returns:
        更新后的状态
    """
    import asyncio
    
    # 在同步环境中运行异步函数
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(parse_document_node(state))
