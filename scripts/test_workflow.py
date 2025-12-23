"""
测试 LangGraph 工作流和文档解析功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.graph_workflow import DataAnalysisWorkflow, LANGGRAPH_AVAILABLE
from analysis.document_parser import DocumentParser


def test_document_parser():
    """测试文档解析器"""
    print("="*60)
    print("测试 1: 文档解析器")
    print("="*60)
    
    parser = DocumentParser()
    print(f"可用解析器: {parser.available_parsers}")
    print(f"支持格式: {DocumentParser.get_supported_formats()}")
    print()


def test_workflow():
    """测试 LangGraph 工作流"""
    print("="*60)
    print("测试 2: LangGraph 工作流")
    print("="*60)
    
    if not LANGGRAPH_AVAILABLE:
        print("⚠️  LangGraph 未安装，跳过工作流测试")
        print("请运行: pip install langgraph")
        return
    
    # 测试材料
    test_material = """
    公司：贵州茅台
    行业：白酒制造
    
    财务指标：
    - 市盈率（PE）：35倍
    - 市净率（PB）：12倍
    - 净资产收益率（ROE）：30%
    - 营收增长率：15%
    - 毛利率：92%
    - 股息率：1.2%
    
    基本面：
    茅台作为中国白酒行业的龙头企业，具有强大的品牌护城河和定价权。
    公司现金流充沛，负债率低，管理层稳健。
    """
    
    print("测试材料:")
    print(test_material)
    print("\n" + "="*60)
    
    try:
        # 创建工作流
        workflow = DataAnalysisWorkflow(llm_provider="siliconflow")
        print("✓ 工作流创建成功")
        
        # 执行工作流
        print("\n🚀 开始执行工作流...")
        result = workflow.run(
            material=test_material,
            investor_id="buffett"
        )
        
        print("\n" + "="*60)
        print("执行结果:")
        print("="*60)
        
        # 显示错误（如果有）
        if result.get("error"):
            print(f"❌ 错误: {result['error']}")
        
        # 显示计算的指标
        if result.get("calculated_metrics"):
            metrics = result["calculated_metrics"].get("metrics", {})
            summary = result["calculated_metrics"].get("summary", {})
            
            print("\n📊 提取的财务指标:")
            for key, value in metrics.items():
                if value is not None:
                    print(f"  - {key}: {value}")
            
            print(f"\n估值评估: {summary.get('valuation', 'N/A')}")
            print(f"企业质量: {summary.get('quality', 'N/A')}")
        
        # 显示最终报告
        if result.get("final_report"):
            print("\n" + "="*60)
            print("📄 最终报告:")
            print("="*60)
            print(result["final_report"]["markdown"])
        
        print("\n✅ 工作流测试完成")
        
    except Exception as e:
        print(f"\n❌ 工作流执行失败: {str(e)}")
        import traceback
        traceback.print_exc()


def test_metrics_extraction():
    """测试指标提取功能"""
    print("\n" + "="*60)
    print("测试 3: 指标提取")
    print("="*60)
    
    from analysis.nodes.calculate_node import calculate_metrics_node
    
    test_state = {
        "parsed_data": {
            "raw_text": """
            PE：25倍
            PB：3.5
            ROE：20%
            营收增长：18%
            毛利率：45%
            """
        }
    }
    
    result = calculate_metrics_node(test_state)
    
    if result.get("calculated_metrics"):
        metrics = result["calculated_metrics"]["metrics"]
        print("提取的指标:")
        for key, value in metrics.items():
            if value is not None:
                print(f"  - {key}: {value}")
        
        print(f"\nPEG 比率: {metrics.get('peg_ratio', 'N/A')}")
        print(f"估值评估: {result['calculated_metrics']['summary']['valuation']}")
        print(f"企业质量: {result['calculated_metrics']['summary']['quality']}")
    else:
        print(f"❌ 指标提取失败: {result.get('error')}")


if __name__ == "__main__":
    print("\n🧪 开始测试 LangGraph 工作流和文档解析功能\n")
    
    # 运行测试
    test_document_parser()
    test_metrics_extraction()
    test_workflow()
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
