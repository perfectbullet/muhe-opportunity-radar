"""投资者服务 - 投资者画像管理"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from typing import List, Dict, Any
from analysis.investor_profiles import InvestorProfileManager


class InvestorService:
    """投资者服务类"""
    
    def __init__(self):
        self.manager = InvestorProfileManager()
    
    async def get_all_investors(self) -> List[Dict[str, Any]]:
        """获取所有投资者列表"""
        all_investors = self.manager.get_all_profiles()
        
        # 格式化输出 - all_investors 是 List[InvestorProfile]
        formatted_investors = []
        for profile in all_investors:
            formatted_investors.append({
                "id": profile.id,
                "name": profile.name,
                "title": profile.title,
                "style": profile.risk_tolerance,
                "philosophy": profile.investment_philosophy,
            })
        
        return formatted_investors
    
    async def get_investor_detail(self, investor_id: str) -> Dict[str, Any]:
        """获取投资者详情"""
        profile = self.manager.get_profile(investor_id)
        if profile:
            return profile.model_dump()
        return None


# 全局服务实例
_investor_service = None


def get_investor_service() -> InvestorService:
    """获取投资者服务实例（单例模式）"""
    global _investor_service
    if _investor_service is None:
        _investor_service = InvestorService()
    return _investor_service
