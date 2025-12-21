"""
Muhe Opportunity Radar - 主应用
基于 Gradio 的投资机会分析前端界面
"""

import gradio as gr
from pathlib import Path
import sys

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
    print(f"✓ 已加载环境变量: {env_path}")
except ImportError:
    print("⚠️  python-dotenv 未安装")

from analysis.perspective_analyzer import PerspectiveAnalyzer
from storage.db_manager import AnalysisRecordManager
from datetime import datetime
import traceback


# 全局变量
analyzer = None
db_manager = None


def init_analyzer(provider: str = "siliconflow"):
    """初始化分析器"""
    global analyzer
    try:
        analyzer = PerspectiveAnalyzer(llm_provider=provider, enable_db=True)
        return f"✓ 分析器初始化成功 ({provider})"
    except Exception as e:
        return f"✗ 初始化失败: {str(e)}"


def get_available_investors():
    """获取可用的投资者列表"""
    if not analyzer:
        init_analyzer()
    
    investors = analyzer.get_available_investors()
    return [(f"{inv['name']} - {inv['title']}", inv['id']) for inv in investors]


def single_analysis(material: str, investor_id: str, context: str = None, progress=gr.Progress()):
    """单一视角分析"""
    if not material.strip():
        return "⚠️ 请输入分析材料"
    
    if not analyzer:
        init_analyzer()
    
    # 获取投资者信息
    try:
        profile = analyzer.profile_manager.get_profile(investor_id)
        investor_name = profile.name if profile else "未知投资者"
    except:
        investor_name = "投资大师"
    
    try:
        # 显示开始分析的提示
        progress(0, desc=f"🚀 开始分析...")
        yield f"# 🔄 正在分析中...\n\n**分析师**: {investor_name}\n\n请稍候，AI 正在思考中..."
        
        progress(0.3, desc=f"📊 {investor_name}正在分析材料...")
        
        result = analyzer.analyze_from_perspective(
            material=material,
            investor_id=investor_id,
            additional_context=context if context and context.strip() else None
        )
        
        progress(0.9, desc="✅ 分析完成")
        
        if result['success']:
            output = f"""
# {result['investor_name']} 的分析

**投资头衔**: {result['investor_title']}  
**投资哲学**: {result['investment_philosophy']}  
**风险承受度**: {result['risk_tolerance']}  
**持有期偏好**: {result['holding_period']}

---

## 分析结果

{result['analysis']}
"""
            progress(1.0, desc="✅ 完成")
            yield output
        else:
            yield f"✗ 分析失败: {result.get('error', '未知错误')}"
            
    except Exception as e:
        yield f"✗ 分析出错: {str(e)}\n\n{traceback.format_exc()}"


def multi_analysis(material: str, investor_ids: list, context: str = None, progress=gr.Progress()):
    """多视角对比分析"""
    if not material.strip():
        return "⚠️ 请输入分析材料"
    
    if not investor_ids or len(investor_ids) == 0:
        return "⚠️ 请至少选择一位投资者"
    
    if not analyzer:
        init_analyzer()
    
    try:
        # 显示开始分析的提示
        progress(0, desc=f"🚀 开始多视角分析...")
        yield f"# 🔄 正在进行多视角分析...\n\n**分析投资者数量**: {len(investor_ids)}\n\n请稍候，正在从 {len(investor_ids)} 位投资大师的角度分析..."
        
        # 分析进度
        total_steps = len(investor_ids) + 1  # 包括最后的综合对比
        
        # 逐个分析
        for i, inv_id in enumerate(investor_ids, 1):
            progress((i / total_steps) * 0.9, desc=f"📊 正在分析 {i}/{len(investor_ids)}...")
            
            try:
                profile = analyzer.profile_manager.get_profile(inv_id)
                inv_name = profile.name if profile else f"投资者{i}"
            except:
                inv_name = f"投资者{i}"
            
            # 更新进度显示
            current_output = f"# 🔄 多视角分析进行中...\n\n"
            current_output += f"**已完成**: {i-1}/{len(investor_ids)}\n"
            current_output += f"**正在分析**: {inv_name}\n\n"
            current_output += "请稍候..."
            yield current_output
        
        progress(0.9, desc="🔄 生成综合对比...")
        
        result = analyzer.compare_perspectives(
            material=material,
            investor_ids=investor_ids,
            additional_context=context if context and context.strip() else None
        )
        
        progress(0.95, desc="✅ 整理结果...")
        
        output = f"# 多视角对比分析\n\n**分析投资者数量**: {result['investor_count']}\n\n"
        output += "---\n\n"
        
        # 各投资者分析
        for i, analysis in enumerate(result['analyses'], 1):
            output += f"## {i}. {analysis['investor_name']} 的分析\n\n"
            output += f"**投资头衔**: {analysis['investor_title']}  \n"
            output += f"**风险承受度**: {analysis.get('risk_tolerance', 'N/A')}  \n"
            output += f"**持有期偏好**: {analysis.get('holding_period', 'N/A')}  \n\n"
            output += f"{analysis['analysis']}\n\n"
            output += "---\n\n"
        
        # 综合对比
        output += f"## 综合对比总结\n\n{result['comparison_summary']}\n"
        
        progress(1.0, desc="✅ 完成")
        yield output
        
    except Exception as e:
        yield f"✗ 分析出错: {str(e)}\n\n{traceback.format_exc()}"


def get_recent_records(limit: int = 10, investor_filter: str = "all"):
    """获取最近的分析记录"""
    try:
        if not db_manager:
            return "⚠️ 数据库未连接，无法查询历史记录", []
        
        investor_id = None if investor_filter == "all" else investor_filter
        records = db_manager.get_recent_analyses(limit=limit, investor_id=investor_id)
        
        if not records:
            return "📭 暂无历史记录", []
        
        output = f"# 最近 {len(records)} 条分析记录\n\n"
        
        # 构建记录选择列表（用于详情查看）
        record_choices = []
        
        for i, record in enumerate(records, 1):
            created_at = record.get('created_at', 'N/A')
            if isinstance(created_at, datetime):
                created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
            
            record_id = str(record.get('_id', ''))
            investor_name = record.get('investor_name', 'N/A')
            
            output += f"## {i}. {investor_name}\n"
            output += f"- **时间**: {created_at}\n"
            output += f"- **记录ID**: `{record_id}`\n"
            output += f"- **材料长度**: {record.get('material_length', 0)} 字符\n"
            output += f"- **分析长度**: {record.get('analysis_length', 0)} 字符\n"
            
            # 显示材料摘要
            material = record.get('material', '')
            material_preview = material[:150] + "..." if len(material) > 150 else material
            output += f"- **材料摘要**: {material_preview}\n"
            output += f"- 💡 **查看全文**: 复制记录ID到下方`详情查看`区域\n\n"
            
            output += "---\n\n"
            
            # 添加到选择列表
            record_choices.append((f"{created_at} - {investor_name}", record_id))
        
        return output, record_choices
        
    except Exception as e:
        return f"✗ 查询出错: {str(e)}", []


def search_records(keyword: str, limit: int = 10):
    """搜索分析记录"""
    if not keyword.strip():
        return "⚠️ 请输入搜索关键词", []
    
    try:
        if not db_manager:
            return "⚠️ 数据库未连接，无法搜索", []
        
        records = db_manager.search_analyses(keyword, limit=limit)
        
        if not records:
            return f"🔍 未找到包含 '{keyword}' 的记录", []
        
        output = f"# 搜索结果: '{keyword}'\n\n找到 {len(records)} 条匹配记录\n\n"
        
        # 构建记录选择列表
        record_choices = []
        
        for i, record in enumerate(records, 1):
            created_at = record.get('created_at', 'N/A')
            if isinstance(created_at, datetime):
                created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
            
            record_id = str(record.get('_id', ''))
            investor_name = record.get('investor_name', 'N/A')
            
            output += f"## {i}. {investor_name}\n"
            output += f"- **时间**: {created_at}\n"
            output += f"- **记录ID**: `{record_id}`\n"
            
            material = record.get('material', '')
            material_preview = material[:150] + "..." if len(material) > 150 else material
            output += f"- **材料**: {material_preview}\n"
            output += f"- 💡 **查看全文**: 复制记录ID到下方`详情查看`区域\n\n"
            
            output += "---\n\n"
            
            # 添加到选择列表
            record_choices.append((f"{created_at} - {investor_name}", record_id))
        
        return output, record_choices
        
    except Exception as e:
        return f"✗ 搜索出错: {str(e)}", []


def get_record_detail(record_id: str):
    """获取分析记录详情"""
    if not record_id or not record_id.strip():
        return "⚠️ 请输入记录ID或从列表中选择"
    
    try:
        if not db_manager:
            return "⚠️ 数据库未连接，无法查询详情"
        
        record = db_manager.get_analysis_by_id(record_id.strip())
        
        if not record:
            return f"❌ 未找到记录ID: {record_id}"
        
        # 构建详细输出
        created_at = record.get('created_at', 'N/A')
        if isinstance(created_at, datetime):
            created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
        
        output = f"""# 📄 分析记录详情

## 基本信息

- **记录ID**: `{record.get('_id', 'N/A')}`
- **投资者**: {record.get('investor_name', 'N/A')}
- **分析时间**: {created_at}
- **分析类型**: {record.get('type', '单次分析')}

---

"""
        
        # 如果是对比分析
        if record.get('type') == 'comparison':
            output += f"""## 📊 对比分析信息

- **投资者数量**: {record.get('investor_count', 0)}
- **投资者列表**: {', '.join(record.get('investor_ids', []))}

---

"""
        
        # 显示完整材料
        material = record.get('material', '无')
        output += f"""## 📋 完整分析材料

{material}

---

"""
        
        # 显示额外上下文
        additional_context = record.get('additional_context')
        if additional_context:
            output += f"""## 📝 额外上下文

{additional_context}

---

"""
        
        # 显示分析结果
        if record.get('type') == 'comparison':
            # 对比分析
            analyses = record.get('analyses', [])
            if analyses:
                output += "## 🎯 各投资者分析\n\n"
                for i, analysis in enumerate(analyses, 1):
                    output += f"### {i}. {analysis.get('investor_name', 'N/A')}\n\n"
                    output += f"{analysis.get('analysis', '无')}\n\n"
                    output += "---\n\n"
            
            # 综合对比总结
            comparison_summary = record.get('comparison_summary')
            if comparison_summary:
                output += f"""## 📊 综合对比总结

{comparison_summary}

"""
        else:
            # 单次分析
            analysis_result = record.get('analysis_result', '无')
            output += f"""## 🎯 完整分析结果

{analysis_result}

"""
        
        # 显示元数据
        metadata = record.get('metadata', {})
        if metadata:
            output += """---

## 🔧 分析元数据

"""
            for key, value in metadata.items():
                output += f"- **{key}**: {value}\n"
        
        return output
        
    except Exception as e:
        return f"✗ 获取详情出错: {str(e)}\n\n{traceback.format_exc()}"


def get_statistics():
    """获取统计信息"""
    try:
        if not db_manager:
            return "⚠️ 数据库未连接，无法获取统计信息"
        
        stats = db_manager.get_statistics()
        
        output = "# 📊 分析统计\n\n"
        output += f"**总记录数**: {stats.get('total_count', 0)}\n\n"
        
        # 按投资者统计
        investor_stats = stats.get('investor_stats', [])
        if investor_stats:
            output += "## 按投资者统计\n\n"
            for stat in investor_stats[:10]:  # 显示前10个
                output += f"- **{stat.get('investor_name', 'N/A')}**: {stat.get('count', 0)} 次分析\n"
        
        output += "\n"
        
        # 按类型统计
        type_stats = stats.get('type_stats', [])
        if type_stats:
            output += "## 按类型统计\n\n"
            for stat in type_stats:
                type_name = stat.get('_id') or '单次分析'
                output += f"- **{type_name}**: {stat.get('count', 0)} 次\n"
        
        return output
        
    except Exception as e:
        return f"✗ 获取统计信息出错: {str(e)}"


# 初始化
print("正在初始化应用...")
init_analyzer()

try:
    db_manager = AnalysisRecordManager()
except Exception as e:
    print(f"⚠️ 数据库管理器初始化失败: {e}")
    db_manager = None

print("✓ 应用初始化完成")


# 创建 Gradio 界面
with gr.Blocks(title="炑禾机会雷达 - 多视角投资分析") as app:
    
    gr.Markdown("""
    # 🎯 炑禾机会雷达 - 多视角投资分析
    
    > 基于 AI 的投资机会挖掘工具，从10位投资大师的视角分析投资标的
    """)
    
    with gr.Tabs():
        # Tab 1: 单一视角分析
        with gr.Tab("📝 单一视角分析"):
            gr.Markdown("### 选择一位投资大师的视角进行分析")
            
            with gr.Row():
                with gr.Column(scale=2):
                    single_material = gr.Textbox(
                        label="投资材料",
                        placeholder="输入要分析的投资材料（如：公司财报、新闻、基本面数据等）...",
                        lines=10
                    )
                    single_context = gr.Textbox(
                        label="额外上下文（可选）",
                        placeholder="补充信息、行业背景等...",
                        lines=3
                    )
                    
                    investor_choices = get_available_investors()
                    single_investor = gr.Dropdown(
                        choices=investor_choices,
                        label="选择投资者",
                        value=investor_choices[0][1] if investor_choices else None
                    )
                    
                    single_btn = gr.Button("🚀 开始分析", variant="primary", size="lg")
            
            single_output = gr.Markdown(label="分析结果")
            
            single_btn.click(
                fn=single_analysis,
                inputs=[single_material, single_investor, single_context],
                outputs=single_output
            )
            
            # 示例
            gr.Examples(
                examples=[
                    ["茅台酒业：市值2.3万亿，PE 32倍，ROE 30%，毛利率91%，品牌护城河强，供不应求。风险：估值偏高，消费降级影响。", "buffett"],
                    ["比亚迪：Q3营收增长38%，新能源车销量80万辆，电池技术突破，海外市场占比15%。挑战：价格战激烈。", "lynch"],
                ],
                inputs=[single_material, single_investor]
            )
        
        # Tab 2: 多视角对比分析
        with gr.Tab("🔄 多视角对比"):
            gr.Markdown("### 从多位投资大师的视角对比分析")
            
            with gr.Row():
                with gr.Column(scale=2):
                    multi_material = gr.Textbox(
                        label="投资材料",
                        placeholder="输入要分析的投资材料...",
                        lines=10
                    )
                    multi_context = gr.Textbox(
                        label="额外上下文（可选）",
                        placeholder="补充信息...",
                        lines=3
                    )
                    
                    multi_investors = gr.CheckboxGroup(
                        choices=[choice[0] for choice in investor_choices],
                        label="选择投资者（可多选）",
                        value=[investor_choices[0][0], investor_choices[1][0]] if len(investor_choices) > 1 else []
                    )
                    
                    multi_btn = gr.Button("🚀 开始对比分析", variant="primary", size="lg")
            
            multi_output = gr.Markdown(label="对比分析结果")
            
            def multi_analysis_wrapper(material, investor_names, context, progress=gr.Progress()):
                # 将名称转换为ID
                name_to_id = {choice[0]: choice[1] for choice in investor_choices}
                investor_ids = [name_to_id[name] for name in investor_names if name in name_to_id]
                yield from multi_analysis(material, investor_ids, context, progress)
            
            multi_btn.click(
                fn=multi_analysis_wrapper,
                inputs=[multi_material, multi_investors, multi_context],
                outputs=multi_output
            )
        
        # Tab 3: 历史记录
        with gr.Tab("📚 历史记录"):
            gr.Markdown("### 查看和搜索历史分析记录")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### 最近记录")
                    
                    with gr.Row():
                        history_limit = gr.Slider(
                            minimum=5,
                            maximum=50,
                            value=10,
                            step=5,
                            label="显示数量"
                        )
                        
                        history_filter = gr.Dropdown(
                            choices=[("全部", "all")] + investor_choices,
                            label="筛选投资者",
                            value="all"
                        )
                    
                    history_btn = gr.Button("🔄 刷新记录", variant="secondary")
                    history_output = gr.Markdown()
                    history_record_list = gr.Dropdown(
                        label="选择记录查看详情",
                        choices=[],
                        interactive=True
                    )
                    
                    def update_history_with_choices(limit, filter):
                        output, choices = get_recent_records(limit, filter)
                        return output, gr.Dropdown(choices=choices)
                    
                    history_btn.click(
                        fn=update_history_with_choices,
                        inputs=[history_limit, history_filter],
                        outputs=[history_output, history_record_list]
                    )
                
                with gr.Column():
                    gr.Markdown("#### 搜索记录")
                    
                    search_keyword = gr.Textbox(
                        label="搜索关键词",
                        placeholder="输入关键词搜索..."
                    )
                    search_limit = gr.Slider(
                        minimum=5,
                        maximum=50,
                        value=10,
                        step=5,
                        label="显示数量"
                    )
                    
                    search_btn = gr.Button("🔍 搜索", variant="secondary")
                    search_output = gr.Markdown()
                    search_record_list = gr.Dropdown(
                        label="选择记录查看详情",
                        choices=[],
                        interactive=True
                    )
                    
                    def update_search_with_choices(keyword, limit):
                        output, choices = search_records(keyword, limit)
                        return output, gr.Dropdown(choices=choices)
                    
                    search_btn.click(
                        fn=update_search_with_choices,
                        inputs=[search_keyword, search_limit],
                        outputs=[search_output, search_record_list]
                    )
            
            # 详情查看区域
            gr.Markdown("---")
            gr.Markdown("### 📄 记录详情查看")
            gr.Markdown("选择上方列表中的记录，或手动输入记录ID")
            
            with gr.Row():
                with gr.Column(scale=3):
                    detail_record_id = gr.Textbox(
                        label="记录ID",
                        placeholder="输入记录ID或从上方下拉列表选择..."
                    )
                with gr.Column(scale=1):
                    detail_btn = gr.Button("🔍 查看详情", variant="primary")
            
            detail_output = gr.Markdown()
            
            # 点击查看详情
            detail_btn.click(
                fn=get_record_detail,
                inputs=detail_record_id,
                outputs=detail_output
            )
            
            # 从列表选择后自动填充ID
            history_record_list.change(
                fn=lambda x: x,
                inputs=history_record_list,
                outputs=detail_record_id
            )
            
            search_record_list.change(
                fn=lambda x: x,
                inputs=search_record_list,
                outputs=detail_record_id
            )
            
            # 加载初始记录
            def load_initial_history(limit, filter):
                output, choices = get_recent_records(limit, filter)
                return output, gr.Dropdown(choices=choices)
            
            app.load(
                fn=load_initial_history,
                inputs=[history_limit, history_filter],
                outputs=[history_output, history_record_list]
            )
        
        # Tab 4: 统计信息
        with gr.Tab("📊 统计信息"):
            gr.Markdown("### 分析记录统计")
            
            stats_btn = gr.Button("🔄 刷新统计", variant="secondary")
            stats_output = gr.Markdown()
            
            stats_btn.click(
                fn=get_statistics,
                outputs=stats_output
            )
            
            # 加载初始统计
            app.load(fn=get_statistics, outputs=stats_output)
    
    gr.Markdown("""
    ---
    
    ### 💡 使用提示
    
    1. **单一视角分析**: 选择一位投资大师，从他的角度分析投资标的
    2. **多视角对比**: 同时从多位大师的角度分析，对比不同观点
    3. **历史记录**: 查看所有分析历史，支持按投资者筛选和关键词搜索
    4. **统计信息**: 查看分析记录的统计数据
    
    **提示**: 所有分析会自动保存到数据库（如果 MongoDB 已启动）
    """)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("启动 Gradio 应用...")
    print("="*80)
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="purple")
    )
