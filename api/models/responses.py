"""API 响应模型定义"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class AnalysisResponse(BaseModel):
    """单一视角分析响应"""
    record_id: str = Field(..., description="分析记录ID")
    investor_id: str = Field(..., description="投资者ID")
    investor_name: str = Field(..., description="投资者姓名")
    analysis: str = Field(..., description="分析结果")
    created_at: datetime = Field(..., description="创建时间")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")


class ComparisonResponse(BaseModel):
    """多视角对比分析响应"""
    record_id: str = Field(..., description="对比记录ID")
    investor_ids: List[str] = Field(..., description="投资者ID列表")
    analyses: List[Dict[str, Any]] = Field(..., description="各投资者分析结果")
    comparison_summary: str = Field(..., description="综合对比总结")
    created_at: datetime = Field(..., description="创建时间")


class RecordItem(BaseModel):
    """历史记录项"""
    record_id: str
    type: str = Field(..., description="记录类型: single 或 comparison")
    material: str
    investor_name: Optional[str] = None
    investor_names: Optional[List[str]] = None
    created_at: datetime
    preview: str = Field(..., description="分析结果预览（前200字）")


class RecordListResponse(BaseModel):
    """历史记录列表响应"""
    records: List[RecordItem]
    total: int = Field(..., description="总记录数")
    page: int = Field(1, description="当前页码")


class StatisticsResponse(BaseModel):
    """统计信息响应"""
    total_count: int = Field(..., description="总分析次数")
    by_investor: Dict[str, int] = Field(..., description="按投资者统计")
    by_type: Dict[str, int] = Field(..., description="按类型统计")
    recent_days: int = Field(30, description="统计天数")


class WorkflowAnalysisResponse(BaseModel):
    """工作流分析响应"""
    success: bool = Field(..., description="是否成功")
    final_report: Optional[Dict[str, Any]] = Field(None, description="最终报告")
    workflow_result: Optional[Dict[str, Any]] = Field(None, description="完整工作流结果")
    error: Optional[str] = Field(None, description="错误信息")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")


class DocumentUploadResponse(BaseModel):
    """文档上传响应"""
    success: bool = Field(..., description="是否成功")
    document_id: str = Field(..., description="文档ID")
    filename: str = Field(..., description="文件名")
    format: str = Field(..., description="文档格式")
    size: int = Field(..., description="文件大小（字节）")
    content_preview: str = Field(..., description="内容预览（前200字）")
    metadata: Optional[Dict[str, Any]] = Field(None, description="文档元数据")
    error: Optional[str] = Field(None, description="错误信息")


class InvestorProfile(BaseModel):
    """投资者画像"""
    id: str
    name: str
    title: str
    style: str
    philosophy: str


class InvestorListResponse(BaseModel):
    """投资者列表响应"""
    investors: List[InvestorProfile]
    total: int
