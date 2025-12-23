"""
LangGraph 数据分析工作流
整合文档解析、指标计算、AI 分析的完整流程
"""

from typing import Dict, Any, TypedDict
from typing_extensions import Annotated
import logging

logger = logging.getLogger(__name__)

# 检查 LangGraph 是否可用
try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    logger.warning("⚠️  LangGraph 未安装，请运行: pip install langgraph")


# 定义工作流状态
class AnalysisState(TypedDict):
    """分析工作流的状态定义"""
    # 输入
    document_id: str                    # 文档 ID（可选）
    material: str                        # 直接提供的材料（可选）
    investor_id: str                     # 投资者 ID
    llm_provider: str                    # LLM 提供商
    additional_context: str              # 额外上下文
    
    # 中间结果
    parsed_data: Dict[str, Any]          # 解析后的数据
    calculated_metrics: Dict[str, Any]   # 计算的指标
    analysis_result: str                 # AI 分析结果
    investor_info: Dict[str, Any]        # 投资者信息
    
    # 最终输出
    final_report: Dict[str, Any]         # 最终报告
    
    # 元数据
    error: str                           # 错误信息
    completed_at: str                    # 完成时间


class DataAnalysisWorkflow:
    """数据分析工作流 - 基于 LangGraph"""
    
    def __init__(self, llm_provider: str = "siliconflow"):
        """
        初始化工作流
        
        Args:
            llm_provider: LLM 提供商（siliconflow/deepseek/qwen 等）
        """
        if not LANGGRAPH_AVAILABLE:
            raise ImportError("需要安装 LangGraph: pip install langgraph")
        
        self.llm_provider = llm_provider
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """
        构建工作流图
        
        流程: 解析 → 计算 → 分析 → 汇总
        """
        from analysis.nodes.parse_node import parse_document_node_sync
        from analysis.nodes.calculate_node import calculate_metrics_node
        from analysis.nodes.analyze_node import llm_analyze_node
        from analysis.nodes.summarize_node import summarize_node
        
        # 创建状态图
        workflow = StateGraph(AnalysisState)
        
        # 添加节点
        workflow.add_node("parse", parse_document_node_sync)
        workflow.add_node("calculate", calculate_metrics_node)
        workflow.add_node("analyze", llm_analyze_node)
        workflow.add_node("summarize", summarize_node)
        
        # 定义边（流程连接）
        workflow.add_edge("parse", "calculate")
        workflow.add_edge("calculate", "analyze")
        workflow.add_edge("analyze", "summarize")
        workflow.add_edge("summarize", END)
        
        # 设置入口点
        workflow.set_entry_point("parse")
        
        # 编译工作流
        app = workflow.compile()
        
        logger.info("✓ LangGraph 工作流已构建")
        return app
    
    def run(
        self,
        material: str,
        investor_id: str = "buffett",
        document_id: str = None,
        additional_context: str = None
    ) -> Dict[str, Any]:
        """
        执行完整的分析工作流（同步版本）
        
        Args:
            material: 分析材料文本
            investor_id: 投资者 ID
            document_id: 文档 ID（可选）
            additional_context: 额外上下文
            
        Returns:
            包含 final_report 的结果字典
        """
        # 初始化状态
        initial_state = {
            "document_id": document_id,
            "material": material,
            "investor_id": investor_id,
            "llm_provider": self.llm_provider,
            "additional_context": additional_context,
            "parsed_data": None,
            "calculated_metrics": None,
            "analysis_result": None,
            "investor_info": None,
            "final_report": None,
            "error": None,
            "completed_at": None
        }
        
        try:
            # 执行工作流
            logger.info(f"🚀 开始执行分析工作流 (投资者: {investor_id})")
            result = self.workflow.invoke(initial_state)
            
            # 检查是否有错误
            if result.get("error"):
                logger.error(f"工作流执行出错: {result['error']}")
            else:
                logger.info("✅ 工作流执行完成")
            
            return result
            
        except Exception as e:
            logger.error(f"工作流执行失败: {str(e)}")
            return {
                **initial_state,
                "error": str(e),
                "final_report": None
            }
    
    async def run_async(
        self,
        material: str,
        investor_id: str = "buffett",
        document_id: str = None,
        additional_context: str = None
    ) -> Dict[str, Any]:
        """
        执行完整的分析工作流（异步版本）
        
        Args:
            material: 分析材料文本
            investor_id: 投资者 ID
            document_id: 文档 ID（可选）
            additional_context: 额外上下文
            
        Returns:
            包含 final_report 的结果字典
        """
        import asyncio
        
        # 在线程池中执行同步工作流
        result = await asyncio.to_thread(
            self.run,
            material=material,
            investor_id=investor_id,
            document_id=document_id,
            additional_context=additional_context
        )
        
        return result


# 便捷函数
def create_workflow(llm_provider: str = "siliconflow") -> DataAnalysisWorkflow:
    """
    创建工作流实例的便捷函数
    
    Args:
        llm_provider: LLM 提供商
        
    Returns:
        DataAnalysisWorkflow 实例
    """
    return DataAnalysisWorkflow(llm_provider=llm_provider)


if __name__ == "__main__":
    # 测试代码
    print("LangGraph 数据分析工作流")
    
    if LANGGRAPH_AVAILABLE:
        # 创建工作流
        workflow = create_workflow()
        
        # 测试材料
        test_material = """
        公司：贵州茅台
        市盈率：35倍
        市净率：12倍
        ROE：30%
        营收增长：15%
        毛利率：92%
        """
        
        # 执行工作流
        result = workflow.run(
            material=test_material,
            investor_id="buffett"
        )
        
        if result.get("final_report"):
            print("\n" + "="*50)
            print(result["final_report"]["markdown"])
        else:
            print(f"执行失败: {result.get('error')}")
    else:
        print("请先安装 LangGraph: pip install langgraph")
