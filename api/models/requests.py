"""API 请求模型定义"""
from typing import List, Optional
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """单一视角分析请求"""
    material: str = Field(..., description="分析材料文本", min_length=10)
    investor_id: str = Field(..., description="投资者ID (如: buffett, graham)")
    additional_context: Optional[str] = Field(None, description="额外上下文信息")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "material": "公司：贵州茅台\n市盈率：35倍\nROE：30%\n营收增长：15%",
                "investor_id": "buffett",
                "additional_context": "当前市场处于牛市阶段"
            }
        }
    }


class ComparisonRequest(BaseModel):
    """多视角对比分析请求"""
    material: str = Field(..., description="分析材料文本", min_length=10)
    investor_ids: List[str] = Field(
        ..., 
        description="投资者ID列表",
        min_length=2,
        max_length=10
    )
    additional_context: Optional[str] = Field(None, description="额外上下文信息")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "material": "公司：贵州茅台\n市盈率：35倍\nROE：30%",
                "investor_ids": ["buffett", "graham", "lynch"],
                "additional_context": "2024年白酒行业景气度下降"
            }
        }
    }


class SearchRequest(BaseModel):
    """搜索请求"""
    keyword: str = Field(..., description="搜索关键词", min_length=1)
    limit: int = Field(20, description="返回结果数量", ge=1, le=100)
    investor_filter: Optional[str] = Field(None, description="按投资者筛选")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "keyword": "茅台",
                "limit": 20,
                "investor_filter": "buffett"
            }
        }
    }


class WorkflowAnalysisRequest(BaseModel):
    """工作流分析请求"""
    material: str = Field(..., description="分析材料文本", min_length=10)
    investor_id: str = Field("buffett", description="投资者ID")
    additional_context: Optional[str] = Field(None, description="额外上下文信息")
    use_workflow: bool = Field(True, description="是否使用 LangGraph 工作流")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "material": "公司：贵州茅台\n市盈率：35倍\nPB：12倍\nROE：30%\n营收增长：15%\n毛利率：92%",
                "investor_id": "buffett",
                "use_workflow": True
            }
        }
    }


class DocumentAnalysisRequest(BaseModel):
    """文档分析请求（上传后）"""
    document_id: str = Field(..., description="已上传的文档ID")
    investor_id: str = Field("buffett", description="投资者ID")
    additional_context: Optional[str] = Field(None, description="额外上下文信息")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "document_id": "doc_12345",
                "investor_id": "buffett"
            }
        }
    }

