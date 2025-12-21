"""
快速入门示例
演示多投资理念分析功能的基本用法
"""

print("="*80)
print("穆和机会雷达 - 多投资理念分析功能 快速入门")
print("="*80)

# 示例1: 查看所有投资者
print("\n【示例1】查看所有可用的投资者")
print("-" * 80)

from analysis import InvestorProfileManager

manager = InvestorProfileManager()
print(f"\n✓ 已加载 {len(manager.get_all_profiles())} 位投资大师的画像\n")

for i, profile in enumerate(manager.get_all_profiles(), 1):
    print(f"{i:2d}. {profile.name:10s} | {profile.title}")
    print(f"    风险承受度: {profile.risk_tolerance:6s} | 持有期: {profile.holding_period}")
    print()

# 示例2: 查看特定投资者的详细信息
print("\n【示例2】查看巴菲特的投资理念")
print("-" * 80)

buffett = manager.get_profile('buffett')
print(f"\n投资者: {buffett.name}")
print(f"投资哲学: {buffett.investment_philosophy}\n")
print("核心原则:")
for i, principle in enumerate(buffett.core_principles, 1):
    print(f"  {i}. {principle}")

# 示例3: 搜索投资者
print("\n【示例3】搜索'价值投资'相关的投资者")
print("-" * 80)

value_investors = manager.search_profiles('价值投资')
print(f"\n找到 {len(value_investors)} 位价值投资者:")
for profile in value_investors:
    print(f"  • {profile.name} - {profile.title}")

# 示例4: 按风险筛选
print("\n【示例4】筛选低风险投资者")
print("-" * 80)

low_risk = manager.get_profiles_by_risk('低')
print(f"\n找到 {len(low_risk)} 位低风险偏好投资者:")
for profile in low_risk:
    print(f"  • {profile.name} ({profile.holding_period})")

# 示例5: AI分析功能预览
print("\n【示例5】AI分析功能（需要API密钥）")
print("-" * 80)

import os

api_key = os.getenv('DEEPSEEK_API_KEY')

if not api_key:
    print("\n⚠️  未配置 DEEPSEEK_API_KEY")
    print("\n要使用AI分析功能，请：")
    print("1. 复制 .env.example 为 .env")
    print("2. 在 .env 中填入你的 DeepSeek API密钥")
    print("3. 重新运行此脚本\n")
    print("示例代码：")
    print("""
from analysis import PerspectiveAnalyzer

# 初始化分析器
analyzer = PerspectiveAnalyzer(llm_provider="deepseek")

# 准备分析材料
material = '''
【投资标的】贵州茅台
- 市值：2.3万亿
- 市盈率：32倍
- ROE：30%
- 毛利率：91%
'''

# 从巴菲特的视角分析
result = analyzer.analyze_from_perspective(
    material=material,
    investor_id='buffett'
)

print(result['analysis'])

# 多视角对比分析
comparison = analyzer.compare_perspectives(
    material=material,
    investor_ids=['buffett', 'lynch', 'graham']
)

print(comparison['comparison_summary'])
    """)
else:
    print("\n✓ 检测到 API 密钥，可以使用AI分析功能")
    print("\n尝试快速分析...")
    
    try:
        from analysis import quick_analyze
        
        test_material = """
        【投资标的】某优质白酒企业
        - ROE: 30%
        - 毛利率: 90%+
        - 市盈率: 35倍
        - 品牌价值高，定价权强
        """
        
        print("\n使用巴菲特的视角分析：")
        print("-" * 60)
        
        result = quick_analyze(
            material=test_material,
            investor_id='buffett',
            llm_provider='deepseek'
        )
        
        print(result)
        print("\n✓ 分析完成！")
        
    except Exception as e:
        print(f"\n✗ 分析失败: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")

# 下一步指引
print("\n" + "="*80)
print("下一步")
print("="*80)
print("""
1. 查看详细文档：docs/multi_perspective_guide.md
2. 运行完整测试：python scripts/test_multi_perspective.py
3. 查看实现总结：docs/implementation_summary.md
4. 开始使用AI分析功能（需配置API密钥）

示例命令：
  python analysis/investor_profiles.py      # 查看所有投资者画像
  python scripts/test_multi_perspective.py  # 运行完整测试
""")

print("\n✨ 祝投资顺利！")
