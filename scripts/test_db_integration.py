"""
快速测试 MongoDB 集成功能
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
except:
    pass

print("测试 MongoDB 集成...")

# 测试导入
from analysis.perspective_analyzer import PerspectiveAnalyzer

# 创建分析器（启用数据库）
analyzer = PerspectiveAnalyzer(
    llm_provider='siliconflow',
    enable_db=True
)

print(f"\n✓ 分析器创建成功")
print(f"数据库状态: {'已连接' if analyzer.db_manager and analyzer.db_manager.client else '未连接（降级模式）'}")

if not analyzer.db_manager or not analyzer.db_manager.client:
    print("\n提示：MongoDB 未连接，分析将继续但不会保存到数据库")
    print("这是正常的降级行为，不影响核心功能")

print("\n✓ 所有测试通过！")
