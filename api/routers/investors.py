"""投资者相关 API 路由"""
from fastapi import APIRouter, HTTPException

from api.models.responses import InvestorListResponse, InvestorProfile
from api.services import get_investor_service

router = APIRouter()


@router.get("/investors", response_model=InvestorListResponse)
async def get_all_investors():
    """
    获取所有投资者列表
    
    返回包含10位投资大师的详细信息
    """
    try:
        service = get_investor_service()
        investors = await service.get_all_investors()
        
        investor_profiles = [InvestorProfile(**inv) for inv in investors]
        
        return InvestorListResponse(
            investors=investor_profiles,
            total=len(investor_profiles)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取投资者列表失败: {str(e)}")


@router.get("/investors/{investor_id}")
async def get_investor_detail(investor_id: str):
    """
    获取投资者详情
    
    - **investor_id**: 投资者ID (如: buffett, graham)
    
    返回完整的投资者画像，包括投资哲学、决策标准等
    """
    try:
        service = get_investor_service()
        profile = await service.get_investor_detail(investor_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail=f"投资者 {investor_id} 不存在")
        
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取投资者详情失败: {str(e)}")
