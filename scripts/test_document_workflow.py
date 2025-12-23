"""
测试文档管理和工作流功能
"""
import asyncio
import os
from pathlib import Path
from analysis.document_parser import DocumentParser
from analysis.graph_workflow import DataAnalysisWorkflow
from storage.document_manager import DocumentManager

async def test_document_workflow():
    """测试完整的文档工作流"""
    
    print("=" * 60)
    print("开始测试文档管理和工作流功能")
    print("=" * 60)
    
    # 1. 测试文档解析器
    print("\n1. 测试文档解析器")
    print("-" * 60)
    
    parser = DocumentParser()
    supported_formats = parser.get_supported_formats()
    print(f"支持的格式: {supported_formats}")
    
    # 创建测试 Markdown 文件
    test_content = """
# 测试投资标的分析

## 基本信息
- 公司名称: 测试科技股份有限公司
- 行业: 科技
- 市值: 1000亿元

## 财务指标
- PE (市盈率): 35
- PB (市净率): 8.5
- ROE (净资产收益率): 25%
- 营收增长率: 30%

## 业务分析
该公司主营业务为人工智能芯片研发和生产，是国内领先的AI芯片厂商。

近三年营收保持高速增长，盈利能力强劲。
"""
    
    test_file = Path("uploads/test_document.md")
    test_file.parent.mkdir(exist_ok=True)
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print(f"创建测试文件: {test_file}")
    
    # 解析文档
    parse_result = parser.parse(str(test_file))
    
    if parse_result.get("success"):
        print("✅ 文档解析成功")
        print(f"格式: {parse_result.get('format')}")
        print(f"内容长度: {len(parse_result.get('content', ''))} 字符")
        print(f"内容预览: {parse_result.get('content', '')[:100]}...")
    else:
        print(f"❌ 文档解析失败: {parse_result.get('error')}")
        return
    
    # 2. 测试数据库管理器
    print("\n2. 测试数据库管理器")
    print("-" * 60)
    
    doc_manager = DocumentManager()
    document_id = "test-doc-001"
    
    try:
        # 保存文档
        await doc_manager.save_document(
            document_id=document_id,
            filename="test_document.md",
            content=parse_result.get("content", ""),
            format="markdown",
            markdown_content=parse_result.get("content", ""),
            metadata={"test": True}
        )
        print("✅ 文档保存成功")
        
        # 读取文档
        markdown = await doc_manager.get_document_markdown(document_id)
        if markdown:
            print(f"✅ 读取 Markdown 成功，长度: {len(markdown)} 字符")
        else:
            print("⚠️  未找到 Markdown 内容")
        
        # 保存财务指标
        await doc_manager.save_metrics(
            document_id=document_id,
            metrics={
                "pe": 35.0,
                "pb": 8.5,
                "roe": 25.0,
                "revenue_growth": 30.0
            },
            summary={
                "valuation": "合理",
                "quality": "优秀"
            }
        )
        print("✅ 财务指标保存成功")
        
        # 读取指标
        metrics = await doc_manager.get_metrics(document_id)
        if metrics:
            print(f"✅ 读取指标成功: PE={metrics.get('metrics', {}).get('pe')}")
        else:
            print("⚠️  未找到财务指标")
        
        # 保存报告
        await doc_manager.save_report(
            document_id=document_id,
            investor_id="buffett",
            investor_name="沃伦·巴菲特",
            report_markdown="# 投资分析报告\n\n这是一个测试报告。",
            structured_data={
                "recommendation": "买入",
                "target_price": 2800,
                "risk_level": "中"
            },
            metadata={"confidence": 0.85}
        )
        print("✅ 分析报告保存成功")
        
        # 读取报告列表
        reports = await doc_manager.list_reports(document_id)
        print(f"✅ 读取报告列表成功，共 {len(reports)} 个报告")
        
        # 获取完整信息
        full_info = await doc_manager.get_document_full_info(document_id)
        if full_info:
            print(f"✅ 获取完整信息成功")
            print(f"   - 文档: {full_info['document']['filename']}")
            print(f"   - 指标: {len(full_info.get('metrics', {}))} 个")
            print(f"   - 报告: {len(full_info.get('reports', []))} 个")
        else:
            print("⚠️  未找到完整信息")
            
    except Exception as e:
        print(f"❌ 数据库操作失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 3. 测试工作流（可选，需要 LLM API Key）
    print("\n3. 测试 LangGraph 工作流")
    print("-" * 60)
    
    if os.getenv("SILICONFLOW_API_KEY"):
        print("检测到 LLM API Key，开始工作流测试...")
        
        try:
            workflow = DataAnalysisWorkflow(llm_provider="siliconflow")
            
            # 运行工作流（异步）
            result = await workflow.run_async(
                material=parse_result.get("content", ""),
                investor_id="buffett"
            )
            
            if result.get("final_report"):
                print("✅ 工作流执行成功")
                print(f"报告长度: {len(result['final_report'].get('markdown', ''))} 字符")
                print(f"报告预览: {result['final_report'].get('markdown', '')[:200]}...")
            else:
                print("⚠️  工作流执行完成，但未生成报告")
                
        except Exception as e:
            print(f"❌ 工作流执行失败: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️  未配置 LLM API Key，跳过工作流测试")
        print("提示: 在 .env 文件中配置 SILICONFLOW_API_KEY 以启用此测试")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_document_workflow())
