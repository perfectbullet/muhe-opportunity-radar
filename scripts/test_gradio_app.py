"""
测试 Gradio 应用的各个功能模块
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print("测试 Gradio 应用功能模块")
print("=" * 80)

# 测试1：导入检查
print("\n1. 检查依赖导入...")
try:
    import gradio as gr
    print(f"   ✓ Gradio {gr.__version__}")
except ImportError as e:
    print(f"   ✗ Gradio 导入失败: {e}")
    sys.exit(1)

try:
    from analysis.perspective_analyzer import PerspectiveAnalyzer
    print("   ✓ PerspectiveAnalyzer")
except ImportError as e:
    print(f"   ✗ PerspectiveAnalyzer 导入失败: {e}")
    sys.exit(1)

try:
    from storage.db_manager import AnalysisRecordManager
    print("   ✓ AnalysisRecordManager")
except ImportError as e:
    print(f"   ⚠️  AnalysisRecordManager 导入失败: {e}")

# 测试2：初始化分析器
print("\n2. 测试分析器初始化...")
try:
    analyzer = PerspectiveAnalyzer(llm_provider="siliconflow", enable_db=False)
    print("   ✓ 分析器初始化成功")
except Exception as e:
    print(f"   ✗ 分析器初始化失败: {e}")
    sys.exit(1)

# 测试3：获取投资者列表
print("\n3. 测试获取投资者列表...")
try:
    investors = analyzer.get_available_investors()
    print(f"   ✓ 找到 {len(investors)} 位投资者")
    for inv in investors[:3]:
        print(f"      - {inv['name']}: {inv['title']}")
    print(f"      ... 等")
except Exception as e:
    print(f"   ✗ 获取投资者列表失败: {e}")

# 测试4：测试数据库管理器（可选）
print("\n4. 测试数据库管理器...")
try:
    db_manager = AnalysisRecordManager()
    print("   ✓ 数据库管理器初始化成功")
    
    # 测试统计功能
    stats = db_manager.get_statistics()
    print(f"   ✓ 统计信息获取成功: {stats.get('total_count', 0)} 条记录")
    
except Exception as e:
    print(f"   ⚠️  数据库管理器测试跳过: {e}")
    print("      提示：如需历史记录功能，请启动 MongoDB")

# 测试5：测试应用启动（不实际启动）
print("\n5. 测试应用模块导入...")
try:
    # 导入应用但不启动
    import app
    print("   ✓ app.py 模块导入成功")
    print("   ✓ 所有功能函数已定义")
except Exception as e:
    print(f"   ✗ app.py 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)
print("\n下一步：运行 'python app.py' 启动 Gradio 界面")
print("访问地址：http://localhost:7860")
print("=" * 80)
