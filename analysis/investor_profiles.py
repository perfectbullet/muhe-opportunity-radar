"""
投资者画像管理模块
用于加载和管理不同投资大师的投资理念和分析视角
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field


class InvestorProfile(BaseModel):
    """投资者画像类（基于 Pydantic）"""
    
    id: str = Field(..., description="投资者唯一标识")
    name: str = Field(..., description="投资者中文名")
    name_en: str = Field(..., description="投资者英文名")
    title: str = Field(..., description="投资者头衔/称号")
    investment_philosophy: str = Field(..., description="投资哲学")
    core_principles: List[str] = Field(default_factory=list, description="核心投资原则")
    analysis_focus: List[str] = Field(default_factory=list, description="分析关注点")
    decision_criteria: Dict = Field(default_factory=dict, description="决策标准")
    risk_tolerance: str = Field(..., description="风险承受度")
    holding_period: str = Field(..., description="持有期偏好")
    prompt_template: Optional[str] = Field(None, description="提示词模板")
    
    class Config:
        # 允许字段验证
        validate_assignment = True
        # 启用额外字段警告
        extra = "allow"
    
    def get_system_prompt(self) -> str:
        """
        获取系统提示词，用于指导AI以该投资者的视角进行分析
        """
        prompt = f"""你现在扮演{self.name}（{self.name_en}），{self.title}。

投资哲学：
{self.investment_philosophy}

核心投资原则：
"""
        for i, principle in enumerate(self.core_principles, 1):
            prompt += f"{i}. {principle}\n"
        
        prompt += f"""
分析关注点：
"""
        for i, focus in enumerate(self.analysis_focus, 1):
            prompt += f"{i}. {focus}\n"
        
        prompt += f"""
风险承受度：{self.risk_tolerance}
持有期偏好：{self.holding_period}

请严格按照{self.name}的投资理念和方法论进行分析，给出符合其风格的投资建议。
"""
        return prompt
    
    def get_analysis_prompt(self, material: str) -> str:
        """
        获取分析提示词，用于分析具体材料
        
        Args:
            material: 要分析的投资材料
            
        Returns:
            完整的分析提示词
        """
        if self.prompt_template:
            return self.prompt_template.format(material=material)
        else:
            return f"{self.get_system_prompt()}\n\n分析材料：\n{material}"
    
    def to_dict(self) -> Dict:
        """转换为字典格式（兼容旧接口）"""
        return self.model_dump(exclude={'prompt_template'}, exclude_none=True)
    
    def __str__(self) -> str:
        return f"{self.name}（{self.name_en}）- {self.title}"


class InvestorProfileManager:
    """投资者画像管理器"""
    
    def __init__(self, profiles_path: Optional[Path] = None):
        """
        初始化管理器
        
        Args:
            profiles_path: 投资者画像JSON文件路径，默认为 data/investor_profiles.json
        """
        if profiles_path is None:
            # 默认路径：项目根目录的 data/investor_profiles.json
            current_dir = Path(__file__).parent.parent
            profiles_path = current_dir / 'data' / 'investor_profiles.json'
        
        self.profiles_path = Path(profiles_path)
        self.profiles: Dict[str, InvestorProfile] = {}
        self.load_profiles()
    
    def load_profiles(self):
        """从JSON文件加载投资者画像（使用 Pydantic 验证）"""
        try:
            if not self.profiles_path.exists():
                raise FileNotFoundError(f"投资者画像文件不存在: {self.profiles_path}")
            
            with open(self.profiles_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            investors = data.get('investors', [])
            for investor_data in investors:
                # 使用 Pydantic 的模型验证
                try:
                    profile = InvestorProfile(**investor_data)
                    self.profiles[profile.id] = profile
                except Exception as e:
                    print(f"⚠️  加载投资者 {investor_data.get('id', 'unknown')} 时出错: {e}")
                    continue
            
            print(f"✓ 成功加载 {len(self.profiles)} 个投资者画像")
            
        except FileNotFoundError as e:
            print(f"✗ 错误: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"✗ JSON解析错误: {e}")
            raise
        except Exception as e:
            print(f"✗ 加载投资者画像时出错: {e}")
            raise
    
    def get_profile(self, investor_id: str) -> Optional[InvestorProfile]:
        """
        根据ID获取投资者画像
        
        Args:
            investor_id: 投资者ID
            
        Returns:
            投资者画像对象，如果不存在则返回None
        """
        return self.profiles.get(investor_id)
    
    def get_all_profiles(self) -> List[InvestorProfile]:
        """获取所有投资者画像"""
        return list(self.profiles.values())
    
    def get_profile_ids(self) -> List[str]:
        """获取所有投资者ID列表"""
        return list(self.profiles.keys())
    
    def get_profile_names(self) -> List[str]:
        """获取所有投资者名称列表"""
        return [profile.name for profile in self.profiles.values()]
    
    def search_profiles(self, keyword: str) -> List[InvestorProfile]:
        """
        搜索投资者画像
        
        Args:
            keyword: 搜索关键词（可以是名字、风格等）
            
        Returns:
            匹配的投资者画像列表
        """
        results = []
        keyword_lower = keyword.lower()
        
        for profile in self.profiles.values():
            if (keyword_lower in profile.name.lower() or
                keyword_lower in profile.name_en.lower() or
                keyword_lower in profile.title.lower() or
                keyword_lower in profile.investment_philosophy.lower()):
                results.append(profile)
        
        return results
    
    def get_profiles_by_risk(self, risk_level: str) -> List[InvestorProfile]:
        """
        根据风险承受度筛选投资者
        
        Args:
            risk_level: 风险等级（极低/低/中等/高）
            
        Returns:
            匹配的投资者画像列表
        """
        return [p for p in self.profiles.values() 
                if p.risk_tolerance == risk_level]
    
    def get_profiles_by_holding_period(self, period_keyword: str) -> List[InvestorProfile]:
        """
        根据持有期偏好筛选投资者
        
        Args:
            period_keyword: 持有期关键词（短期/中期/长期/超长期）
            
        Returns:
            匹配的投资者画像列表
        """
        return [p for p in self.profiles.values() 
                if period_keyword in p.holding_period]
    
    def print_profiles_summary(self):
        """打印所有投资者画像摘要"""
        print("\n" + "="*80)
        print("投资者画像库".center(80))
        print("="*80)
        
        for i, profile in enumerate(self.profiles.values(), 1):
            print(f"\n{i}. {profile.name}（{profile.name_en}）")
            print(f"   {profile.title}")
            print(f"   投资哲学：{profile.investment_philosophy[:50]}...")
            print(f"   风险承受度：{profile.risk_tolerance} | 持有期：{profile.holding_period}")
        
        print("\n" + "="*80)


# 便捷函数
def load_investor_profile(investor_id: str) -> Optional[InvestorProfile]:
    """
    快速加载单个投资者画像
    
    Args:
        investor_id: 投资者ID
        
    Returns:
        投资者画像对象
    """
    manager = InvestorProfileManager()
    return manager.get_profile(investor_id)


def list_all_investors() -> List[str]:
    """
    列出所有可用的投资者
    
    Returns:
        投资者名称列表
    """
    manager = InvestorProfileManager()
    return manager.get_profile_names()


if __name__ == '__main__':
    # 测试代码
    print("测试投资者画像管理模块...\n")
    
    # 创建管理器
    manager = InvestorProfileManager()
    
    # 打印所有投资者摘要
    manager.print_profiles_summary()
    
    # 测试获取单个投资者
    print("\n" + "="*80)
    print("测试获取巴菲特画像：")
    print("="*80)
    buffett = manager.get_profile('buffett')
    if buffett:
        print(f"\n{buffett}")
        print(f"\n投资哲学：{buffett.investment_philosophy}")
        print(f"\n核心原则：")
        for principle in buffett.core_principles:
            print(f"  • {principle}")
    
    # 测试搜索功能
    print("\n" + "="*80)
    print("搜索'价值投资'相关的投资者：")
    print("="*80)
    results = manager.search_profiles('价值投资')
    for profile in results:
        print(f"  • {profile}")
    
    # 测试风险筛选
    print("\n" + "="*80)
    print("风险承受度为'低'的投资者：")
    print("="*80)
    low_risk = manager.get_profiles_by_risk('低')
    for profile in low_risk:
        print(f"  • {profile}")
    
    print("\n✓ 测试完成")
