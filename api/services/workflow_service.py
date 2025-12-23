"""
工作流服务层
封装 LangGraph 工作流的异步调用
"""

import asyncio
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class WorkflowService:
    """工作流服务 - 提供异步接口"""
    
    def __init__(self, llm_provider: str = "siliconflow"):
        """
        初始化服务
        
        Args:
            llm_provider: LLM 提供商
        """
        self.llm_provider = llm_provider
        self._workflow = None
    
    def _get_workflow(self):
        """延迟加载工作流（避免启动时的开销）"""
        if self._workflow is None:
            from analysis.graph_workflow import DataAnalysisWorkflow
            self._workflow = DataAnalysisWorkflow(llm_provider=self.llm_provider)
        return self._workflow
    
    async def analyze_with_workflow(
        self,
        material: str,
        investor_id: str = "buffett",
        document_id: str = None,
        additional_context: str = None
    ) -> Dict[str, Any]:
        """
        使用工作流进行分析（异步）
        
        Args:
            material: 分析材料
            investor_id: 投资者 ID
            document_id: 文档 ID（可选）
            additional_context: 额外上下文
            
        Returns:
            工作流执行结果
        """
        workflow = self._get_workflow()
        
        # 使用异步方法
        result = await workflow.run_async(
            material=material,
            investor_id=investor_id,
            document_id=document_id,
            additional_context=additional_context
        )
        
        return result
    
    async def parse_and_analyze_document(
        self,
        file_path: str,
        document_id: str,
        investor_id: str = "buffett",
        additional_context: str = None
    ) -> Dict[str, Any]:
        """
        解析文档并进行工作流分析
        
        Args:
            file_path: 文档文件路径
            document_id: 文档ID
            investor_id: 投资者 ID
            additional_context: 额外上下文
            
        Returns:
            分析结果
        """
        from analysis.document_parser import parse_document
        from storage.document_manager import DocumentManager
        from pathlib import Path
        
        doc_manager = DocumentManager()
        
        # 1. 解析文档
        parse_result = await asyncio.to_thread(parse_document, file_path)
        
        if not parse_result.get("success"):
            return {
                "success": False,
                "error": parse_result.get("error", "文档解析失败"),
                "final_report": None
            }
        
        # 2. 保存文档到数据库
        try:
            await doc_manager.save_document(
                document_id=document_id,
                filename=Path(file_path).name,
                content=parse_result.get("content", ""),
                format=parse_result.get("format", "unknown"),
                markdown_content=parse_result.get("content", ""),  # 原样保存，后续可转换
                metadata=parse_result.get("metadata", {})
            )
        except Exception as e:
            logger.error(f"保存文档失败: {str(e)}")
        
        # 3. 使用工作流分析
        material = parse_result.get("content", "")
        
        workflow_result = await self.analyze_with_workflow(
            material=material,
            investor_id=investor_id,
            document_id=document_id,
            additional_context=additional_context
        )
        
        # 4. 保存指标和报告
        try:
            if workflow_result.get("calculated_metrics"):
                await doc_manager.save_metrics(
                    document_id=document_id,
                    metrics=workflow_result["calculated_metrics"].get("metrics", {}),
                    summary=workflow_result["calculated_metrics"].get("summary", {})
                )
            
            if workflow_result.get("final_report"):
                investor_info = workflow_result.get("investor_info", {})
                await doc_manager.save_report(
                    document_id=document_id,
                    investor_id=investor_id,
                    investor_name=investor_info.get("name", "未知"),
                    report_markdown=workflow_result["final_report"].get("markdown", ""),
                    structured_data=workflow_result["final_report"].get("structured_data", {}),
                    metadata=workflow_result["final_report"].get("metadata", {})
                )
        except Exception as e:
            logger.error(f"保存分析结果失败: {str(e)}")
        
        # 5. 整合结果
        return {
            "success": not workflow_result.get("error"),
            "document_info": {
                "format": parse_result.get("format"),
                "pages": parse_result.get("pages"),
                "metadata": parse_result.get("metadata")
            },
            "workflow_result": workflow_result,
            "final_report": workflow_result.get("final_report"),
            "error": workflow_result.get("error")
        }
