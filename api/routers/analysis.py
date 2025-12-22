"""分析相关 API 路由"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

from api.models.requests import AnalysisRequest, ComparisonRequest
from api.models.responses import AnalysisResponse, ComparisonResponse
from api.services import get_analysis_service

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_single(request: AnalysisRequest):
    """
    单一视角分析接口
    
    - **material**: 分析材料文本
    - **investor_id**: 投资者ID (如: buffett, graham, lynch)
    - **additional_context**: 可选的额外上下文
    """
    try:
        service = get_analysis_service()
        result = await service.analyze_single(
            material=request.material,
            investor_id=request.investor_id,
            additional_context=request.additional_context
        )
        
        return AnalysisResponse(
            record_id=result['record_id'],
            investor_id=result['investor_id'],
            investor_name=result['investor_name'],
            analysis=result['analysis'],
            created_at=result['created_at'],
            metadata=result.get('metadata')
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.post("/analyze/stream")
async def analyze_single_stream(request: AnalysisRequest):
    """
    单一视角流式分析接口
    
    返回 SSE (Server-Sent Events) 流式响应
    """
    try:
        service = get_analysis_service()
        
        async def event_generator() -> AsyncGenerator[str, None]:
            async for chunk in service.analyze_single_stream(
                material=request.material,
                investor_id=request.investor_id,
                additional_context=request.additional_context
            ):
                # SSE 格式: data: {content}\n\n
                yield f"data: {chunk}\n\n"
            
            # 发送结束信号
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # 禁用 Nginx 缓冲
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"流式分析失败: {str(e)}")


@router.post("/compare", response_model=ComparisonResponse)
async def compare_perspectives(request: ComparisonRequest):
    """
    多视角对比分析接口
    
    - **material**: 分析材料文本
    - **investor_ids**: 投资者ID列表 (2-10个)
    - **additional_context**: 可选的额外上下文
    """
    try:
        service = get_analysis_service()
        result = await service.compare_perspectives(
            material=request.material,
            investor_ids=request.investor_ids,
            additional_context=request.additional_context
        )
        
        return ComparisonResponse(
            record_id=result['record_id'],
            investor_ids=result['investor_ids'],
            analyses=result['analyses'],
            comparison_summary=result['comparison_summary'],
            created_at=result['created_at']
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对比分析失败: {str(e)}")


@router.post("/compare/stream")
async def compare_perspectives_stream(request: ComparisonRequest):
    """
    多视角对比流式分析接口
    
    返回 SSE (Server-Sent Events) 流式响应
    """
    try:
        service = get_analysis_service()
        
        async def event_generator() -> AsyncGenerator[str, None]:
            async for chunk in service.compare_perspectives_stream(
                material=request.material,
                investor_ids=request.investor_ids,
                additional_context=request.additional_context
            ):
                yield f"data: {chunk}\n\n"
            
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"流式对比分析失败: {str(e)}")
