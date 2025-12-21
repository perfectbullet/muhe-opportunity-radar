"""
多视角分析引擎
支持从不同投资大师的视角分析投资材料
"""

import os
from typing import Dict, List, Optional
from pathlib import Path

# 加载环境变量
try:
    from dotenv import load_dotenv
    # 加载项目根目录的 .env 文件
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    print("⚠️  python-dotenv 未安装，将直接使用系统环境变量")


from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import SecretStr

from .investor_profiles import InvestorProfile, InvestorProfileManager


class PerspectiveAnalyzer:
    """多视角分析器 - 让AI以不同投资大师的视角分析材料"""

    def __init__(
        self,
        llm_provider: str = "deepseek",
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
    ):
        """
        初始化多视角分析器

        Args:
            llm_provider: LLM提供商 (deepseek/qwen/zhipu/openai/claude/siliconflow)
            api_key: API密钥，如果不提供则从环境变量读取
            model_name: 模型名称，如果不提供则使用默认模型
            temperature: 温度参数，控制输出的随机性
        """

        self.llm_provider = llm_provider.lower()
        self.temperature = temperature

        # 加载投资者画像管理器
        self.profile_manager = InvestorProfileManager()

        # 初始化LLM客户端
        self.llm = self._init_llm(api_key, model_name)

    def _init_llm(self, api_key: Optional[str], model_name: Optional[str]):
        """初始化LLM客户端"""

        # 初始化默认值
        default_model = None
        base_url = None

        # 从环境变量获取API密钥
        if api_key is None:
            if self.llm_provider == "deepseek":
                api_key = os.getenv("DEEPSEEK_API_KEY")
                default_model = "deepseek-chat"
                base_url = "https://api.deepseek.com"
            elif self.llm_provider == "qwen":
                api_key = os.getenv("QWEN_API_KEY")
                default_model = "qwen-max"
                base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            elif self.llm_provider == "zhipu":
                api_key = os.getenv("ZHIPU_API_KEY")
                default_model = "glm-4"
                base_url = None
            elif self.llm_provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                default_model = "gpt-4o-mini"
                base_url = None
            elif self.llm_provider == "siliconflow":
                api_key = os.getenv("SILICONFLOW_API_KEY")
                default_model = os.getenv(
                    "SILICONFLOW_MODEL", "deepseek-ai/DeepSeek-V3.1-Terminus"
                )
                base_url = os.getenv(
                    "SILICONFLOW_API_BASE_URL", "https://api.siliconflow.cn/v1"
                )
            else:
                raise ValueError(f"不支持的LLM提供商: {self.llm_provider}")

        if not api_key:
            raise ValueError(f"未找到 {self.llm_provider.upper()} 的API密钥")

        # 使用提供的模型名称或默认模型
        model = model_name or default_model
        
        if not model:
            raise ValueError(f"未找到 {self.llm_provider.upper()} 的默认模型名称")
        if not api_key:
            raise ValueError(f"未找到 {self.llm_provider.upper()} 的API密钥")

        # 创建LLM客户端
        if self.llm_provider in ["deepseek", "qwen", "openai", "siliconflow"]:
            llm = ChatOpenAI(
                model=model,
                api_key=SecretStr(api_key),
                base_url=base_url if self.llm_provider not in ["openai"] else None,
                temperature=self.temperature,
            )
        elif self.llm_provider == "zhipu":
            llm = ChatZhipuAI(
                model=model, api_key=api_key, temperature=self.temperature
            )
        else:
            raise ValueError(f"不支持的LLM提供商: {self.llm_provider}")

        print(f"✓ 已初始化 {self.llm_provider.upper()} LLM: {model}")
        return llm

    def analyze_from_perspective(
        self, material: str, investor_id: str, additional_context: Optional[str] = None
    ) -> Dict:
        """
        从特定投资者的视角分析材料

        Args:
            material: 要分析的投资材料（新闻、财报、数据等）
            investor_id: 投资者ID
            additional_context: 额外的上下文信息

        Returns:
            分析结果字典
        """
        # 获取投资者画像
        profile = self.profile_manager.get_profile(investor_id)
        if not profile:
            raise ValueError(f"未找到投资者画像: {investor_id}")

        print(f"\n🎯 从 {profile.name} 的视角分析...")

        # 构建提示词
        system_prompt = profile.get_system_prompt()

        # 构建分析材料
        full_material = material
        if additional_context:
            full_material = f"{material}\n\n额外上下文：\n{additional_context}"

        analysis_prompt = profile.get_analysis_prompt(full_material)

        # 调用LLM
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=analysis_prompt),
            ]

            response = self.llm.invoke(messages)
            analysis_result = response.content

            return {
                "investor_id": investor_id,
                "investor_name": profile.name,
                "investor_title": profile.title,
                "analysis": analysis_result,
                "investment_philosophy": profile.investment_philosophy,
                "risk_tolerance": profile.risk_tolerance,
                "holding_period": profile.holding_period,
                "success": True,
            }

        except Exception as e:
            print(f"✗ 分析时出错: {e}")
            return {
                "investor_id": investor_id,
                "investor_name": profile.name,
                "analysis": f"分析失败: {str(e)}",
                "success": False,
                "error": str(e),
            }

    def analyze_from_multiple_perspectives(
        self,
        material: str,
        investor_ids: List[str],
        additional_context: Optional[str] = None,
    ) -> List[Dict]:
        """
        从多个投资者的视角分析同一材料

        Args:
            material: 要分析的投资材料
            investor_ids: 投资者ID列表
            additional_context: 额外的上下文信息

        Returns:
            多个分析结果的列表
        """
        results = []

        for investor_id in investor_ids:
            result = self.analyze_from_perspective(
                material=material,
                investor_id=investor_id,
                additional_context=additional_context,
            )
            results.append(result)

        return results

    def compare_perspectives(
        self,
        material: str,
        investor_ids: List[str],
        additional_context: Optional[str] = None,
    ) -> Dict:
        """
        对比不同投资者对同一材料的分析

        Args:
            material: 要分析的投资材料
            investor_ids: 投资者ID列表
            additional_context: 额外的上下文信息

        Returns:
            包含所有分析和对比总结的字典
        """
        # 获取所有分析
        analyses = self.analyze_from_multiple_perspectives(
            material, investor_ids, additional_context
        )

        # 生成对比总结
        print("\n📊 生成多视角对比总结...")

        comparison_prompt = f"""
请对比以下{len(analyses)}位投资大师对同一投资材料的分析，总结：

1. **共识观点**：哪些方面他们的看法一致？
2. **分歧观点**：哪些方面存在明显分歧？
3. **互补视角**：不同视角提供了哪些互补的洞察？
4. **综合建议**：综合考虑各方观点后的投资建议

各位投资大师的分析：

"""

        for i, analysis in enumerate(analyses, 1):
            separator = '=' * 60
            comparison_prompt += f"""
{separator}
{i}. {analysis['investor_name']}（{analysis['investor_title']}）
风险承受度：{analysis.get('risk_tolerance', 'N/A')}
持有期偏好：{analysis.get('holding_period', 'N/A')}

分析内容：
{analysis['analysis']}

"""

        try:
            messages = [
                SystemMessage(
                    content="你是一位资深的投资分析师，擅长综合不同投资理念。"
                ),
                HumanMessage(content=comparison_prompt),
            ]

            response = self.llm.invoke(messages)
            comparison_summary = response.content

        except Exception as e:
            comparison_summary = f"生成对比总结时出错: {str(e)}"

        return {
            "material": material,
            "investor_count": len(investor_ids),
            "analyses": analyses,
            "comparison_summary": comparison_summary,
        }

    def get_available_investors(self) -> List[Dict]:
        """
        获取所有可用的投资者列表

        Returns:
            投资者信息列表
        """
        profiles = self.profile_manager.get_all_profiles()
        return [
            {
                "id": p.id,
                "name": p.name,
                "name_en": p.name_en,
                "title": p.title,
                "philosophy": p.investment_philosophy,
                "risk_tolerance": p.risk_tolerance,
                "holding_period": p.holding_period,
            }
            for p in profiles
        ]

    def recommend_investors(
        self,
        risk_preference: Optional[str] = None,
        holding_period: Optional[str] = None,
        keyword: Optional[str] = None,
    ) -> List[Dict]:
        """
        根据偏好推荐投资者

        Args:
            risk_preference: 风险偏好（极低/低/中等/高）
            holding_period: 持有期偏好（短期/中期/长期/超长期）
            keyword: 搜索关键词

        Returns:
            推荐的投资者列表
        """
        profiles = self.profile_manager.get_all_profiles()

        # 筛选
        if risk_preference:
            profiles = [p for p in profiles if p.risk_tolerance == risk_preference]

        if holding_period:
            profiles = [p for p in profiles if holding_period in p.holding_period]

        if keyword:
            profiles = self.profile_manager.search_profiles(keyword)

        return [
            {
                "id": p.id,
                "name": p.name,
                "title": p.title,
                "risk_tolerance": p.risk_tolerance,
                "holding_period": p.holding_period,
            }
            for p in profiles
        ]


def quick_analyze(
    material: str, investor_id: str = "buffett", llm_provider: str = "deepseek"
) -> str:
    """
    快速分析函数 - 便捷接口

    Args:
        material: 投资材料
        investor_id: 投资者ID，默认为巴菲特
        llm_provider: LLM提供商

    Returns:
        分析结果文本
    """
    analyzer = PerspectiveAnalyzer(llm_provider=llm_provider)
    result = analyzer.analyze_from_perspective(material, investor_id)

    if result["success"]:
        return result["analysis"]
    else:
        return f"分析失败: {result.get('error', '未知错误')}"


if __name__ == "__main__":
    # 测试代码
    print("测试多视角分析引擎...\n")

    # 示例投资材料
    test_material = """
    公司名称：某科技公司
    
    基本情况：
    - 市值：500亿人民币
    - 市盈率：35倍
    - 市净率：5倍
    - ROE：18%
    - 负债率：45%
    - 近三年营收增长率：年均30%
    
    业务情况：
    - 主营业务：云计算和人工智能服务
    - 市场份额：国内第三
    - 核心技术：拥有多项AI专利
    - 客户：主要服务大型企业客户
    - 护城河：技术壁垒和客户粘性
    
    最新动态：
    - 刚发布新一代AI模型，性能提升50%
    - Q3财报显示营收增长35%，但利润率下降3个百分点（研发投入增加）
    - 管理层表示未来三年将继续高强度研发投入
    """

    try:
        # 创建分析器（这里需要配置环境变量 DEEPSEEK_API_KEY）
        analyzer = PerspectiveAnalyzer(llm_provider="deepseek")

        # 显示可用投资者
        print("可用的投资者：")
        investors = analyzer.get_available_investors()
        for inv in investors[:5]:  # 显示前5个
            print(f"  • {inv['name']} - {inv['title']}")

        print("\n" + "=" * 80)
        print("开始多视角分析...")
        print("=" * 80)

        # 选择几位投资者进行分析
        selected_investors = ["buffett", "lynch", "fisher"]

        # 进行对比分析
        comparison = analyzer.compare_perspectives(
            material=test_material, investor_ids=selected_investors
        )

        # 打印结果
        print("\n" + "=" * 80)
        print("多视角分析结果")
        print("=" * 80)

        for analysis in comparison["analyses"]:
            print(f"\n{'='*60}")
            print(f"{analysis['investor_name']}的分析：")
            print(f"{'='*60}")
            print(analysis["analysis"])

        print(f"\n{'='*80}")
        print("综合对比总结：")
        print(f"{'='*80}")
        print(comparison["comparison_summary"])

        print("\n✓ 测试完成")

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        print("\n提示：请确保已设置环境变量 DEEPSEEK_API_KEY")
