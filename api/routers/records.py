"""历史记录相关 API 路由"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from api.models.requests import ReanalyzeRequest
from api.models.responses import RecordListResponse, StatisticsResponse, RecordItem, AnalysisResponse, ComparisonResponse
from api.services import get_record_service, get_analysis_service

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


@router.post("/records/{record_id}/reanalyze")
async def reanalyze_material(record_id: str, request: ReanalyzeRequest):
    """
    重新分析已有材料
    
    从历史记录中获取原始材料，使用新的投资者视角重新分析
    
    - **record_id**: 原始记录ID
    - **investor_id**: 新的投资者ID
    - **use_comparison**: 是否使用多视角对比
    - **investor_ids**: 多视角对比时的投资者ID列表
    """
    try:
        # 获取原始记录
        record_service = get_record_service()
        original_record = await record_service.get_record_detail(record_id)
        
        if not original_record:
            raise HTTPException(status_code=404, detail="原始记录不存在")
        
        # 提取材料和上下文
        material = original_record.get("material")
        if not material:
            raise HTTPException(status_code=400, detail="原始记录中没有材料内容")
        
        # 合并上下文（如果有新的上下文，追加到原有上下文）
        original_context = original_record.get("additional_context", "")
        new_context = request.additional_context or ""
        combined_context = f"{original_context}\n{new_context}".strip() if original_context or new_context else None
        
        # 根据请求类型进行分析
        analysis_service = get_analysis_service()
        
        if request.use_comparison and request.investor_ids:
            # 多视角对比分析
            result = await analysis_service.compare_perspectives(
                material=material,
                investor_ids=request.investor_ids,
                additional_context=combined_context
            )
            
            return ComparisonResponse(
                record_id=result['record_id'],
                investor_ids=result['investor_ids'],
                analyses=result['analyses'],
                comparison_summary=result['comparison_summary'],
                created_at=result['created_at']
            )
        else:
            # 单一视角分析
            result = await analysis_service.analyze_single(
                material=material,
                investor_id=request.investor_id,
                additional_context=combined_context
            )
            
            return AnalysisResponse(
                record_id=result['record_id'],
                investor_id=result['investor_id'],
                investor_name=result['investor_name'],
                analysis=result['analysis'],
                created_at=result['created_at'],
                metadata={
                    **result.get('metadata', {}),
                    "reanalyzed_from": record_id,
                    "original_investor": original_record.get("investor_id") or original_record.get("investor_ids")
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重新分析失败: {str(e)}")
