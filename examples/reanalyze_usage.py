"""
重新分析功能使用示例
演示如何使用重新分析 API
"""
import requests
import json
from datetime import datetime

# API 基础地址
BASE_URL = "http://localhost:8080/api/v1"


def example_1_single_perspective():
    """
    示例 1: 单一视角重新分析
    
    场景: 首次用巴菲特视角分析后，想用林奇视角重新看
    """
    print("="*60)
    print("示例 1: 单一视角重新分析")
    print("="*60)
    
    # 假设已有记录 ID
    original_record_id = "your_record_id_here"
    
    # 构造重新分析请求
    reanalyze_data = {
        "investor_id": "lynch",  # 彼得·林奇视角
        "additional_context": "关注公司的成长性和 PEG 指标",
        "use_comparison": False
    }
    
    print(f"\n原记录ID: {original_record_id}")
    print(f"新投资者: {reanalyze_data['investor_id']}")
    print(f"额外上下文: {reanalyze_data['additional_context']}")
    
    # 发送请求
    try:
        response = requests.post(
            f"{BASE_URL}/records/{original_record_id}/reanalyze",
            json=reanalyze_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ 重新分析成功！")
            print(f"  新记录ID: {result['record_id']}")
            print(f"  投资者: {result['investor_name']}")
            print(f"  分析时间: {result['created_at']}")
            print(f"  分析结果预览: {result['analysis'][:200]}...")
            
            if 'metadata' in result and 'reanalyzed_from' in result['metadata']:
                print(f"  原记录ID: {result['metadata']['reanalyzed_from']}")
        else:
            print(f"\n✗ 请求失败: {response.status_code}")
            print(f"  错误信息: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n✗ 网络错误: {e}")


def example_2_multi_perspective_comparison():
    """
    示例 2: 多视角对比分析
    
    场景: 想同时看多位大师的观点
    """
    print("\n" + "="*60)
    print("示例 2: 多视角对比分析")
    print("="*60)
    
    original_record_id = "your_record_id_here"
    
    reanalyze_data = {
        "investor_id": "buffett",  # 主要视角
        "use_comparison": True,
        "investor_ids": ["buffett", "lynch", "graham", "soros"],
        "additional_context": "综合多位大师的投资理念进行分析"
    }
    
    print(f"\n原记录ID: {original_record_id}")
    print(f"对比投资者: {', '.join(reanalyze_data['investor_ids'])}")
    print(f"额外上下文: {reanalyze_data['additional_context']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/records/{original_record_id}/reanalyze",
            json=reanalyze_data,
            timeout=120  # 多视角分析需要更长时间
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ 多视角对比完成！")
            print(f"  对比记录ID: {result['record_id']}")
            print(f"  对比投资者数: {len(result['analyses'])}")
            
            print("\n  各投资者观点:")
            for analysis in result['analyses']:
                print(f"    - {analysis['investor_name']}: {analysis['analysis'][:100]}...")
            
            print(f"\n  综合对比总结:")
            print(f"    {result['comparison_summary'][:200]}...")
        else:
            print(f"\n✗ 请求失败: {response.status_code}")
            print(f"  错误信息: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n✗ 网络错误: {e}")


def get_recent_records():
    """
    辅助函数: 获取最近的分析记录
    用于获取可以重新分析的记录ID
    """
    print("\n" + "="*60)
    print("获取最近的分析记录")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/records?limit=5")
        
        if response.status_code == 200:
            data = response.json()
            records = data['records']
            
            if records:
                print(f"\n找到 {len(records)} 条记录:")
                for i, record in enumerate(records, 1):
                    print(f"\n  {i}. 记录ID: {record['record_id']}")
                    print(f"     投资者: {record.get('investor_name', 'N/A')}")
                    print(f"     时间: {record['created_at']}")
                    print(f"     材料预览: {record['material'][:80]}...")
                    
                print("\n提示: 复制上面的记录ID，替换示例中的 'your_record_id_here'")
                return records[0]['record_id']
            else:
                print("\n暂无历史记录，请先进行一次分析")
                return None
        else:
            print(f"\n✗ 获取记录失败: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n✗ 网络错误: {e}")
        print("提示: 请确保 API 服务正在运行 (http://localhost:8080)")
        return None


def main():
    """主函数"""
    print("\n" + "🔄"*30)
    print("重新分析功能使用示例")
    print("🔄"*30)
    
    print("\n步骤 1: 检查 API 服务状态")
    get_recent_records()
    
    print("\n" + "-"*60)
    print("使用说明:")
    print("-"*60)
    print("  1. 取消注释下面的示例函数即可运行")
    print("  2. 将 'your_record_id_here' 替换为真实的记录ID")
    print("  3. 确保 API 服务正在运行: python -m uvicorn api.main:app --reload")
    print("  4. 确保已配置 LLM API 密钥")
    
    # 运行示例 (取消注释以运行)
    # example_1_single_perspective()
    # example_2_multi_perspective_comparison()


if __name__ == "__main__":
    main()
