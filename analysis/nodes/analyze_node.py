"""
LLM 分析节点
使用 AI 模型进行深度分析
"""

from typing import Dict, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def llm_analyze_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LLM 分析节点 - 使用大语言模型进行投资分析
    
    Args:
        state: 工作流状态，包含 parsed_data 和 calculated_metrics
        
    Returns:
        更新后的状态，添加 analysis_result 字段
    """
    from analysis.perspective_analyzer import PerspectiveAnalyzer
    
    parsed_data = state.get("parsed_data")
    calculated_metrics = state.get("calculated_metrics")
    investor_id = state.get("investor_id", "buffett")
    
    if not parsed_data:
        logger.error("缺少 parsed_data")
        return {
            **state,
            "error": "缺少解析数据",
            "analysis_result": None
        }
    
    try:
        # 构建分析材料
        material = _build_analysis_material(parsed_data, calculated_metrics)
        
        # 使用投资者视角分析
        analyzer = PerspectiveAnalyzer(
            llm_provider=state.get("llm_provider", "siliconflow"),
            enable_db=False  # 工作流内部不直接保存到数据库
        )
        
        result = analyzer.analyze_from_perspective(
            material=material,
            investor_id=investor_id,
            additional_context=state.get("additional_context")
        )
        
        logger.info(f"✓ LLM 分析完成 (投资者: {result.get('investor_name', 'Unknown')})")
        
        return {
            **state,
            "analysis_result": result.get("analysis", ""),
            "investor_info": {
                "name": result.get("investor_name"),
                "title": result.get("investor_title"),
                "philosophy": result.get("investment_philosophy")
            },
            "error": None
        }
        
    except Exception as e:
        logger.error(f"LLM 分析失败: {str(e)}")
        return {
            **state,
            "error": f"分析失败: {str(e)}",
            "analysis_result": None
        }


def _build_analysis_material(parsed_data: Dict, calculated_metrics: Dict) -> str:
    """
    构建分析材料，整合文本和计算指标
    
    Args:
        parsed_data: 解析后的数据
        calculated_metrics: 计算的指标
        
    Returns:
        格式化的分析材料
    """
    material_parts = []
    
    # 原始文本
    raw_text = parsed_data.get("raw_text", "")
    if raw_text:
        material_parts.append("## 原始材料\n")
        material_parts.append(raw_text[:2000])  # 限制长度
        if len(raw_text) > 2000:
            material_parts.append("\n...(内容过长，已截断)")
    
    # 计算指标
    if calculated_metrics:
        metrics = calculated_metrics.get("metrics", {})
        summary = calculated_metrics.get("summary", {})
        
        material_parts.append("\n\n## 财务指标")
        
        if metrics.get("pe_ratio"):
            material_parts.append(f"\n- 市盈率 (PE): {metrics['pe_ratio']}")
        if metrics.get("pb_ratio"):
            material_parts.append(f"\n- 市净率 (PB): {metrics['pb_ratio']}")
        if metrics.get("roe"):
            material_parts.append(f"\n- 净资产收益率 (ROE): {metrics['roe']}%")
        if metrics.get("peg_ratio"):
            material_parts.append(f"\n- PEG: {metrics['peg_ratio']}")
        if metrics.get("revenue_growth"):
            material_parts.append(f"\n- 营收增长率: {metrics['revenue_growth']}%")
        if metrics.get("gross_margin"):
            material_parts.append(f"\n- 毛利率: {metrics['gross_margin']}%")
        if metrics.get("dividend_yield"):
            material_parts.append(f"\n- 股息率: {metrics['dividend_yield']}%")
        
        if summary:
            material_parts.append(f"\n\n## 初步评估")
            material_parts.append(f"\n- 估值水平: {summary.get('valuation', 'N/A')}")
            material_parts.append(f"\n- 企业质量: {summary.get('quality', 'N/A')}")
    
    return "".join(material_parts)
