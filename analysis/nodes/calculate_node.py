"""
指标计算节点
计算财务指标和统计数据
"""

from typing import Dict, Any
import re
import logging

logger = logging.getLogger(__name__)


def calculate_metrics_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    指标计算节点 - 从文本中提取并计算财务指标
    
    支持的指标：
    - PE (市盈率)
    - PB (市净率)
    - ROE (净资产收益率)
    - 营收增长率
    - 毛利率
    - 股息率
    
    Args:
        state: 工作流状态，包含 parsed_data
        
    Returns:
        更新后的状态，添加 calculated_metrics 字段
    """
    parsed_data = state.get("parsed_data")
    
    if not parsed_data:
        logger.error("缺少 parsed_data")
        return {
            **state,
            "error": "缺少解析数据",
            "calculated_metrics": None
        }
    
    try:
        text = parsed_data.get("raw_text", "")
        
        # 提取财务指标
        metrics = {
            "pe_ratio": _extract_metric(text, r"PE[：:=\s]*(\d+\.?\d*)"),
            "pb_ratio": _extract_metric(text, r"PB[：:=\s]*(\d+\.?\d*)"),
            "roe": _extract_metric(text, r"ROE[：:=\s]*(\d+\.?\d*)%?"),
            "revenue_growth": _extract_metric(text, r"营收增长[：:=\s]*(\d+\.?\d*)%?"),
            "gross_margin": _extract_metric(text, r"毛利率[：:=\s]*(\d+\.?\d*)%?"),
            "dividend_yield": _extract_metric(text, r"股息率[：:=\s]*(\d+\.?\d*)%?"),
            "market_cap": _extract_metric(text, r"市值[：:=\s]*(\d+\.?\d*)"),
        }
        
        # 计算衍生指标
        if metrics["pe_ratio"] and metrics["revenue_growth"]:
            # PEG = PE / 增长率
            metrics["peg_ratio"] = round(metrics["pe_ratio"] / metrics["revenue_growth"], 2)
        
        # 统计提取到的指标数量
        extracted_count = sum(1 for v in metrics.values() if v is not None)
        
        logger.info(f"✓ 指标计算完成，提取了 {extracted_count} 个指标")
        
        # 添加汇总信息
        calculated_metrics = {
            "metrics": metrics,
            "summary": {
                "total_extracted": extracted_count,
                "valuation": _assess_valuation(metrics),
                "quality": _assess_quality(metrics)
            }
        }
        
        return {
            **state,
            "calculated_metrics": calculated_metrics,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"指标计算失败: {str(e)}")
        return {
            **state,
            "error": f"计算失败: {str(e)}",
            "calculated_metrics": None
        }


def _extract_metric(text: str, pattern: str) -> float:
    """
    从文本中提取数值指标
    
    Args:
        text: 文本内容
        pattern: 正则表达式模式
        
    Returns:
        提取的数值，如果未找到则返回 None
    """
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except (ValueError, IndexError):
            return None
    return None


def _assess_valuation(metrics: Dict[str, float]) -> str:
    """
    评估估值水平
    
    Args:
        metrics: 财务指标字典
        
    Returns:
        估值评估结果
    """
    pe = metrics.get("pe_ratio")
    pb = metrics.get("pb_ratio")
    peg = metrics.get("peg_ratio")
    
    if not any([pe, pb, peg]):
        return "数据不足"
    
    # 简单评估逻辑
    valuation_score = 0
    
    if pe:
        if pe < 15:
            valuation_score += 1
        elif pe > 30:
            valuation_score -= 1
    
    if pb:
        if pb < 2:
            valuation_score += 1
        elif pb > 5:
            valuation_score -= 1
    
    if peg:
        if peg < 1:
            valuation_score += 1
        elif peg > 2:
            valuation_score -= 1
    
    if valuation_score >= 2:
        return "低估"
    elif valuation_score <= -2:
        return "高估"
    else:
        return "合理"


def _assess_quality(metrics: Dict[str, float]) -> str:
    """
    评估企业质量
    
    Args:
        metrics: 财务指标字典
        
    Returns:
        质量评估结果
    """
    roe = metrics.get("roe")
    gross_margin = metrics.get("gross_margin")
    
    if not any([roe, gross_margin]):
        return "数据不足"
    
    quality_score = 0
    
    if roe:
        if roe >= 15:
            quality_score += 2
        elif roe >= 10:
            quality_score += 1
    
    if gross_margin:
        if gross_margin >= 40:
            quality_score += 1
    
    if quality_score >= 3:
        return "优秀"
    elif quality_score >= 2:
        return "良好"
    elif quality_score >= 1:
        return "一般"
    else:
        return "较差"
