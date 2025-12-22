"""历史记录相关 API 路由"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from api.models.responses import RecordListResponse, StatisticsResponse, RecordItem
from api.services import get_record_service

router = APIRouter()


@router.get("/records", response_model=RecordListResponse)
async def get_recent_records(
    limit: int = Query(20, ge=1, le=100, description="返回记录数量"),
    investor_filter: Optional[str] = Query(None, description="按投资者筛选")
):
    """
    获取最近分析记录
    
    - **limit**: 返回记录数量 (1-100)
    - **investor_filter**: 可选的投资者ID筛选
    """
    try:
        service = get_record_service()
        records = await service.get_recent_records(
            limit=limit,
            investor_filter=investor_filter
        )
        
        # 转换为响应模型
        record_items = [RecordItem(**record) for record in records]
        
        return RecordListResponse(
            records=record_items,
            total=len(record_items),
            page=1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取记录失败: {str(e)}")


@router.get("/records/{record_id}")
async def get_record_detail(record_id: str):
    """
    获取分析记录详情
    
    - **record_id**: 记录ID
    """
    try:
        service = get_record_service()
        record = await service.get_record_detail(record_id)
        
        if not record:
            raise HTTPException(status_code=404, detail="记录不存在")
        
        # 转换 ObjectId 为字符串
        record['_id'] = str(record['_id'])
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取详情失败: {str(e)}")


@router.get("/records/search/{keyword}", response_model=RecordListResponse)
async def search_records(
    keyword: str,
    limit: int = Query(20, ge=1, le=100, description="返回记录数量"),
    investor_filter: Optional[str] = Query(None, description="按投资者筛选")
):
    """
    搜索分析记录
    
    - **keyword**: 搜索关键词
    - **limit**: 返回记录数量
    - **investor_filter**: 可选的投资者ID筛选
    """
    try:
        service = get_record_service()
        records = await service.search_records(
            keyword=keyword,
            limit=limit,
            investor_filter=investor_filter
        )
        
        record_items = [RecordItem(**record) for record in records]
        
        return RecordListResponse(
            records=record_items,
            total=len(record_items),
            page=1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """
    获取统计信息
    
    返回总分析次数、按投资者统计、按类型统计等信息
    """
    try:
        service = get_record_service()
        stats = await service.get_statistics()
        
        return StatisticsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计失败: {str(e)}")
