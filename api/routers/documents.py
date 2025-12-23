"""
文档管理 API 路由
处理文档上传、解析和分析
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional, Dict, Any, List

import shutil
import uuid
from pathlib import Path
import os

from api.models.requests import WorkflowAnalysisRequest, DocumentAnalysisRequest
from api.models.responses import DocumentUploadResponse, WorkflowAnalysisResponse
from api.services.workflow_service import WorkflowService
from analysis.document_parser import DocumentParser

router = APIRouter(prefix="/documents")

# 上传文件存储目录
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 初始化服务
workflow_service = WorkflowService()
document_parser = DocumentParser()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(..., description="上传的文档文件"),
    investor_id: Optional[str] = Form("buffett", description="投资者ID"),
    auto_analyze: Optional[bool] = Form(False, description="是否自动分析")
):
    """
    上传文档并可选地进行分析
    
    支持格式: PDF (.pdf), Word (.doc, .docx), Markdown (.md, .markdown)
    """
    # 验证文件格式
    file_ext = Path(file.filename).suffix.lower()
    supported_formats = DocumentParser.get_supported_formats()
    
    if file_ext not in supported_formats:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {file_ext}，支持的格式: {', '.join(supported_formats)}"
        )
    
    try:
        # 生成唯一文件ID和保存路径
        document_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{document_id}{file_ext}"
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        
        # 解析文档
        parse_result = document_parser.parse(file_path)
        
        if not parse_result.get("success"):
            # 解析失败，删除文件
            file_path.unlink()
            raise HTTPException(
                status_code=400,
                detail=f"文档解析失败: {parse_result.get('error', '未知错误')}"
            )
        
        # 提取内容预览
        content = parse_result.get("content", "")
        content_preview = content[:200] + "..." if len(content) > 200 else content
        
        # 构建响应
        response = DocumentUploadResponse(
            success=True,
            document_id=document_id,
            filename=file.filename,
            format=parse_result.get("format", "unknown"),
            size=file_size,
            content_preview=content_preview,
            metadata=parse_result.get("metadata"),
            error=None
        )
        
        # 如果需要自动分析
        if auto_analyze:
            try:
                analysis_result = await workflow_service.analyze_with_workflow(
                    material=content,
                    investor_id=investor_id
                )
                
                # 将分析结果添加到响应的 metadata
                response.metadata = response.metadata or {}
                response.metadata["analysis"] = analysis_result
                
            except Exception as e:
                # 分析失败不影响上传成功
                response.metadata = response.metadata or {}
                response.metadata["analysis_error"] = str(e)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        # 清理可能已保存的文件
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()
        
        raise HTTPException(
            status_code=500,
            detail=f"文件上传失败: {str(e)}"
        )


@router.post("/analyze-workflow", response_model=WorkflowAnalysisResponse)
async def analyze_with_workflow(request: WorkflowAnalysisRequest):
    """
    使用 LangGraph 工作流分析材料
    
    工作流包括：文档解析 → 指标计算 → AI分析 → 结果汇总
    """
    try:
        result = await workflow_service.analyze_with_workflow(
            material=request.material,
            investor_id=request.investor_id,
            additional_context=request.additional_context
        )
        
        return WorkflowAnalysisResponse(
            success=not result.get("error"),
            final_report=result.get("final_report"),
            workflow_result=result,
            error=result.get("error"),
            metadata={
                "investor_id": request.investor_id,
                "completed_at": result.get("completed_at")
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"工作流分析失败: {str(e)}"
        )


@router.post("/analyze-document", response_model=WorkflowAnalysisResponse)
async def analyze_document(request: DocumentAnalysisRequest):
    """
    分析已上传的文档
    
    根据 document_id 从存储中读取文档并使用工作流分析
    """
    # 查找文档文件
    document_files = list(UPLOAD_DIR.glob(f"{request.document_id}.*"))
    
    if not document_files:
        raise HTTPException(
            status_code=404,
            detail=f"文档未找到: {request.document_id}"
        )
    
    file_path = document_files[0]
    
    try:
        result = await workflow_service.parse_and_analyze_document(
            file_path=str(file_path),
            investor_id=request.investor_id,
            additional_context=request.additional_context
        )
        
        return WorkflowAnalysisResponse(
            success=result.get("success"),
            final_report=result.get("final_report"),
            workflow_result=result.get("workflow_result"),
            error=result.get("error"),
            metadata={
                "document_id": request.document_id,
                "document_info": result.get("document_info")
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文档分析失败: {str(e)}"
        )


@router.get("")
async def list_documents():
    """列出所有已上传的文档"""
    documents = []
    
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file():
            # 提取文档ID和格式
            document_id = file_path.stem
            file_format = file_path.suffix
            
            documents.append({
                "document_id": document_id,
                "filename": file_path.name,
                "format": file_format,
                "size": os.path.getsize(file_path),
                "uploaded_at": file_path.stat().st_ctime
            })
    
    return {
        "documents": documents,
        "total": len(documents)
    }


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """删除指定文档"""
    document_files = list(UPLOAD_DIR.glob(f"{document_id}.*"))
    
    if not document_files:
        raise HTTPException(
            status_code=404,
            detail=f"文档未找到: {document_id}"
        )
    
    try:
        for file_path in document_files:
            file_path.unlink()
        
        return {
            "success": True,
            "message": f"文档已删除: {document_id}",
            "deleted_files": len(document_files)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除失败: {str(e)}"
        )


@router.get("/supported-formats")
async def get_supported_formats():
    """获取支持的文档格式"""
    return {
        "formats": DocumentParser.get_supported_formats(),
        "parser_info": {
            "pdf": "支持 PDF 文档（财报、研究报告）",
            "word": "支持 Word 文档（.doc, .docx）",
            "markdown": "支持 Markdown 文档（.md）"
        }
    }


@router.get("/{document_id}/markdown", response_model=Dict[str, Any])
async def get_document_markdown(document_id: str):
    """获取文档的 Markdown 内容"""
    from storage.document_manager import DocumentManager
    
    doc_manager = DocumentManager()
    markdown_content = await doc_manager.get_document_markdown(document_id)
    
    if not markdown_content:
        raise HTTPException(status_code=404, detail="文档不存在或未找到 Markdown 内容")
    
    return {
        "document_id": document_id,
        "markdown_content": markdown_content
    }


@router.get("/{document_id}/metrics", response_model=Dict[str, Any])
async def get_document_metrics(document_id: str):
    """获取文档的财务指标"""
    from storage.document_manager import DocumentManager
    
    doc_manager = DocumentManager()
    metrics = await doc_manager.get_metrics(document_id)
    
    if not metrics:
        raise HTTPException(status_code=404, detail="未找到财务指标数据")
    
    return {
        "document_id": document_id,
        "metrics": metrics
    }


@router.get("/{document_id}/reports", response_model=List[Dict[str, Any]])
async def get_document_reports(
    document_id: str,
    investor_id: Optional[str] = None
):
    """获取文档的分析报告列表"""
    from storage.document_manager import DocumentManager
    
    doc_manager = DocumentManager()
    reports = await doc_manager.list_reports(document_id, investor_id)
    
    return reports


@router.get("/{document_id}/full", response_model=Dict[str, Any])
async def get_document_full_info(document_id: str):
    """获取文档的完整信息（包含 markdown、指标、报告）"""
    from storage.document_manager import DocumentManager
    
    doc_manager = DocumentManager()
    full_info = await doc_manager.get_document_full_info(document_id)
    
    if not full_info:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    return full_info

