"""
测试 MongoDB 集成功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
    print(f"✓ 已加载环境变量: {env_path}\n")
except ImportError:
    print("⚠️  python-dotenv 未安装，将直接使用系统环境变量\n")

from storage.db_manager import AnalysisRecordManager


def test_db_connection():
    """测试数据库连接"""
    print("="*80)
    print("测试 1: MongoDB 连接")
    print("="*80)
    
    try:
        manager = AnalysisRecordManager()
        
        if manager.client:
            print("✓ MongoDB 连接成功")
            
            # 获取统计信息
            stats = manager.get_statistics()
            print(f"\n数据库统计:")
            print(f"  总记录数: {stats.get('total_count', 0)}")
            
            manager.close()
            return True
        else:
            print("✗ MongoDB 连接失败")
            print("  提示：请确保 MongoDB 服务已启动")
            print("  Windows: net start MongoDB")
            print("  Mac/Linux: sudo systemctl start mongod")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def test_save_and_query():
    """测试保存和查询"""
    print("\n" + "="*80)
    print("测试 2: 保存和查询分析记录")
    print("="*80)
    
    try:
        manager = AnalysisRecordManager()
        
        if not manager.client:
            print("⚠️  跳过测试（MongoDB 未连接）")
            return False
        
        # 测试保存单个分析
        print("\n保存测试分析记录...")
        record_id = manager.save_analysis(
            material="测试材料：某科技公司2024年Q3财报分析",
            investor_id="buffett",
            investor_name="沃伦·巴菲特",
            analysis_result="""
            作为巴菲特，我会从以下几个角度分析：
            1. 护城河分析...
            2. 管理层评估...
            3. 财务健康度...
            """,
            additional_context="测试上下文信息",
            metadata={
                "test": True,
                "investor_title": "股神、价值投资代表"
            }
        )
        
        if record_id:
            print(f"✓ 保存成功，记录ID: {record_id}")
            
            # 测试查询
            print("\n查询最近的分析记录...")
            recent = manager.get_recent_analyses(limit=5)
            print(f"✓ 找到 {len(recent)} 条记录")
            
            if recent:
                latest = recent[0]
                print(f"\n最新记录:")
                print(f"  投资者: {latest.get('investor_name')}")
                print(f"  时间: {latest.get('created_at')}")
                print(f"  材料长度: {latest.get('material_length')} 字符")
            
            # 测试搜索
            print("\n搜索包含'巴菲特'的记录...")
            results = manager.search_analyses("巴菲特", limit=3)
            print(f"✓ 找到 {len(results)} 条匹配记录")
            
            manager.close()
            return True
        else:
            print("✗ 保存失败")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_comparison_save():
    """测试对比分析保存"""
    print("\n" + "="*80)
    print("测试 3: 保存对比分析记录")
    print("="*80)
    
    try:
        manager = AnalysisRecordManager()
        
        if not manager.client:
            print("⚠️  跳过测试（MongoDB 未连接）")
            return False
        
        print("\n保存对比分析记录...")
        record_id = manager.save_comparison(
            material="测试材料：茅台酒业投资分析",
            investor_ids=["buffett", "graham", "lynch"],
            analyses=[
                {
                    "investor_id": "buffett",
                    "investor_name": "沃伦·巴菲特",
                    "analysis": "巴菲特的分析..."
                },
                {
                    "investor_id": "graham",
                    "investor_name": "本杰明·格雷厄姆",
                    "analysis": "格雷厄姆的分析..."
                },
                {
                    "investor_id": "lynch",
                    "investor_name": "彼得·林奇",
                    "analysis": "林奇的分析..."
                }
            ],
            comparison_summary="综合对比总结：三位大师的观点..."
        )
        
        if record_id:
            print(f"✓ 保存成功，记录ID: {record_id}")
            
            # 获取统计信息
            stats = manager.get_statistics()
            print(f"\n更新后的统计:")
            print(f"  总记录数: {stats.get('total_count', 0)}")
            
            manager.close()
            return True
        else:
            print("✗ 保存失败")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("MongoDB 集成功能测试套件")
    print("="*80)
    print("\n提示：此测试需要 MongoDB 服务正在运行")
    print("如果 MongoDB 未安装，可以跳过此测试\n")
    
    # 运行测试
    tests = [
        ("数据库连接", test_db_connection),
        ("保存和查询", test_save_and_query),
        ("对比分析保存", test_comparison_save),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "="*80)
    print("测试总结")
    print("="*80)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {name}")
    
    print(f"\n通过率: {passed}/{total}")
    
    if passed == 0:
        print("\n提示：如果所有测试都失败，可能是因为：")
        print("  1. MongoDB 服务未启动")
        print("  2. 连接配置不正确（检查 .env 文件）")
        print("  3. pymongo 未安装（pip install pymongo）")


if __name__ == '__main__':
    main()
