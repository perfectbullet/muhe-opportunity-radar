"""
结果汇总节点
整合所有分析结果并生成最终报告
"""

from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def summarize_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    结果汇总节点 - 整合所有分析结果
    
    Args:
        state: 工作流状态
        
    Returns:
        更新后的状态，添加 final_report 字段
    """
    try:
        # 收集所有结果
        parsed_data = state.get("parsed_data", {})
        calculated_metrics = state.get("calculated_metrics", {})
        analysis_result = state.get("analysis_result", "")
        investor_info = state.get("investor_info", {})
        
        # 构建最终报告
        report = _build_final_report(
            parsed_data=parsed_data,
            calculated_metrics=calculated_metrics,
            analysis_result=analysis_result,
            investor_info=investor_info
        )
        
        logger.info("✓ 结果汇总完成")
        
        return {
            **state,
            "final_report": report,
            "completed_at": datetime.utcnow().isoformat(),
            "error": None
        }
        
    except Exception as e:
        logger.error(f"结果汇总失败: {str(e)}")
        return {
            **state,
            "error": f"汇总失败: {str(e)}",
            "final_report": None
        }


def _build_final_report(
    parsed_data: Dict,
    calculated_metrics: Dict,
    analysis_result: str,
    investor_info: Dict
) -> Dict[str, Any]:
    """
    构建最终报告
    
    Returns:
        包含完整分析结果的字典
    """
    metrics = calculated_metrics.get("metrics", {}) if calculated_metrics else {}
    summary = calculated_metrics.get("summary", {}) if calculated_metrics else {}
    
    # 构建 Markdown 格式的报告
    markdown_report = f"""# 投资分析报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 财务指标

"""
    
    if metrics:
        if metrics.get("pe_ratio"):
            markdown_report += f"- **市盈率 (PE)**: {metrics['pe_ratio']}\n"
        if metrics.get("pb_ratio"):
            markdown_report += f"- **市净率 (PB)**: {metrics['pb_ratio']}\n"
        if metrics.get("roe"):
            markdown_report += f"- **净资产收益率 (ROE)**: {metrics['roe']}%\n"
        if metrics.get("peg_ratio"):
            markdown_report += f"- **PEG 比率**: {metrics['peg_ratio']}\n"
        if metrics.get("revenue_growth"):
            markdown_report += f"- **营收增长率**: {metrics['revenue_growth']}%\n"
        if metrics.get("gross_margin"):
            markdown_report += f"- **毛利率**: {metrics['gross_margin']}%\n"
    
    if summary:
        markdown_report += f"\n## 📈 初步评估\n\n"
        markdown_report += f"- **估值水平**: {summary.get('valuation', 'N/A')}\n"
        markdown_report += f"- **企业质量**: {summary.get('quality', 'N/A')}\n"
    
    if investor_info:
        markdown_report += f"\n## 👤 分析师视角\n\n"
        markdown_report += f"**投资者**: {investor_info.get('name', 'Unknown')}\n"
        markdown_report += f"**头衔**: {investor_info.get('title', 'N/A')}\n"
        markdown_report += f"**投资哲学**: {investor_info.get('philosophy', 'N/A')}\n"
    
    if analysis_result:
        markdown_report += f"\n## 🎯 深度分析\n\n{analysis_result}\n"
    
    # 返回结构化数据
    return {
        "markdown": markdown_report,
        "structured_data": {
            "metrics": metrics,
            "summary": summary,
            "investor": investor_info,
            "analysis": analysis_result
        },
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "document_length": len(parsed_data.get("raw_text", "")),
            "metrics_count": calculated_metrics.get("summary", {}).get("total_extracted", 0)
        }
    }
