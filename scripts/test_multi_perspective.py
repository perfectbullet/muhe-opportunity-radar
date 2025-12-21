"""
多视角分析功能测试脚本
用于测试不同投资大师视角的AI分析功能
"""

import os
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
    print(f"✓ 已加载环境变量: {env_path}")
except ImportError:
    print("⚠️  python-dotenv 未安装，将直接使用系统环境变量")

from analysis.investor_profiles import InvestorProfileManager, load_investor_profile
from analysis.perspective_analyzer import PerspectiveAnalyzer, quick_analyze


def test_profile_manager():
    """测试投资者画像管理器"""
    print("\n" + "="*80)
    print("测试 1: 投资者画像管理器")
    print("="*80)
    
    try:
        manager = InvestorProfileManager()
        
        # 打印所有投资者
        manager.print_profiles_summary()
        
        # 测试获取单个投资者
        print("\n获取巴菲特画像：")
        buffett = manager.get_profile('buffett')
        if buffett:
            print(f"✓ {buffett}")
            print(f"  投资哲学：{buffett.investment_philosophy}")
            print(f"  风险承受度：{buffett.risk_tolerance}")
        
        # 测试搜索
        print("\n搜索'成长'相关投资者：")
        results = manager.search_profiles('成长')
        for p in results:
            print(f"  • {p}")
        
        print("\n✓ 投资者画像管理器测试通过")
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        return False


def test_perspective_analyzer():
    """测试多视角分析器"""
    print("\n" + "="*80)
    print("测试 2: 多视角分析器")
    print("="*80)
    
    # 示例投资材料
    test_material = """
    【投资标的分析】茅台酒业
    
    基本面：
    - 市值：2.3万亿人民币
    - 市盈率：32倍
    - 市净率：9倍
    - ROE：30%
    - 负债率：15%
    - 毛利率：91%
    - 净利润率：52%
    
    业务特点：
    - 国内高端白酒绝对龙头，市占率40%+
    - 品牌价值极高，定价权强
    - 产能受限，供不应求
    - 客户群体稳定，复购率高
    - 渠道控制力强
    
    财务数据：
    - 近五年营收年均增长15%
    - 净利润年均增长18%
    - 现金流充沛，账上现金1500亿+
    - 连续20年分红，股息率1.5%
    
    风险因素：
    - 估值偏高，PE处于历史75%分位
    - 消费降级可能影响高端白酒需求
    - 政策监管风险（反腐、限酒令）
    - 年轻一代消费习惯改变
    """
    
    try:
        # 创建分析器
        analyzer = PerspectiveAnalyzer(llm_provider="siliconflow")
        
        # 测试单一视角分析
        print("\n测试单一视角分析（巴菲特）：")
        print("-" * 60)
        result = analyzer.analyze_from_perspective(
            material=test_material,
            investor_id='buffett'
        )
        
        if result['success']:
            print(f"\n投资者：{result['investor_name']}")
            print(f"投资哲学：{result['investment_philosophy']}")
            print(f"\n分析结果：")
            print(result['analysis'])
            print("\n✓ 单一视角分析测试通过")
        else:
            print(f"✗ 分析失败: {result.get('error')}")
            return False
        
        # 测试多视角对比分析
        print("\n" + "="*80)
        print("测试多视角对比分析")
        print("="*80)
        
        selected_investors = ['buffett', 'graham', 'lynch']
        print(f"\n选择的投资者：{', '.join(selected_investors)}")
        
        comparison = analyzer.compare_perspectives(
            material=test_material,
            investor_ids=selected_investors
        )
        
        # 打印各投资者的分析
        for analysis in comparison['analyses']:
            print("\n" + "="*60)
            print(f"{analysis['investor_name']} 的分析")
            print("="*60)
            print(analysis['analysis'])
        
        # 打印对比总结
        print("\n" + "="*80)
        print("综合对比总结")
        print("="*80)
        print(comparison['comparison_summary'])
        
        print("\n✓ 多视角分析器测试通过")
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quick_analyze():
    """测试快速分析接口"""
    print("\n" + "="*80)
    print("测试 3: 快速分析接口")
    print("="*80)
 
    
    test_news = """
    【行业新闻】新能源汽车行业观察
    
    比亚迪发布2024年Q3财报：
    - 营收同比增长38%
    - 新能源汽车销量突破80万辆
    - 海外市场收入占比提升至15%
    - 电池技术获得新突破
    
    行业趋势：
    - 国内新能源渗透率突破35%
    - 价格战持续，竞争激烈
    - 自动驾驶技术加速落地
    - 充电基础设施完善
    """
    
    try:
        print("\n使用彼得·林奇的视角分析：")
        print("-" * 60)
        
        result = quick_analyze(
            material=test_news,
            investor_id='lynch',
            llm_provider='siliconflow'
        )
        
        print(result)
        print("\n✓ 快速分析接口测试通过")
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        return False


def interactive_demo():
    """交互式演示"""
    print("\n" + "="*80)
    print("交互式多视角分析演示")
    print("="*80)
    
    try:
        analyzer = PerspectiveAnalyzer(llm_provider="siliconflow")
        
        # 显示可用投资者
        print("\n可选的投资者角色：")
        investors = analyzer.get_available_investors()
        for i, inv in enumerate(investors, 1):
            print(f"{i}. {inv['name']} - {inv['title']}")
            print(f"   风险承受度：{inv['risk_tolerance']} | 持有期：{inv['holding_period']}")
        
        print("\n请输入要分析的投资材料（输入空行结束）：")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        
        material = "\n".join(lines)
        
        if not material.strip():
            print("未输入任何内容，使用示例材料...")
            material = "某科技公司刚发布财报，营收增长30%，但利润率下降5%。"
        
        print("\n请选择投资者（输入编号，多个用逗号分隔，如 1,3,5）：")
        selection = input().strip()
        
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_ids = [investors[i]['id'] for i in indices]
        except:
            print("输入格式错误，使用默认选择：巴菲特、林奇、费雪")
            selected_ids = ['buffett', 'lynch', 'fisher']
        
        print(f"\n开始分析...")
        comparison = analyzer.compare_perspectives(
            material=material,
            investor_ids=selected_ids
        )
        
        # 显示结果
        for analysis in comparison['analyses']:
            print("\n" + "="*80)
            print(f"{analysis['investor_name']} 的分析")
            print("="*80)
            print(analysis['analysis'])
        
        print("\n" + "="*80)
        print("综合对比")
        print("="*80)
        print(comparison['comparison_summary'])
        
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"\n✗ 出错: {e}")


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("多视角分析功能测试套件")
    print("="*80)
    
    # 运行测试
    tests = [
        ("投资者画像管理器", test_profile_manager),
        ("多视角分析器", test_perspective_analyzer),
        ("快速分析接口", test_quick_analyze),
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
    
    # 询问是否运行交互式演示
    if passed > 0:
        print("\n是否运行交互式演示？(y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            interactive_demo()


if __name__ == '__main__':
    main()
