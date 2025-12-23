"""
FastAPI 主应用入口
提供 RESTful API 接口，支持流式输出
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

from api.routers import analysis, records, investors, documents

# 加载环境变量
load_dotenv()

# 创建 FastAPI 应用
app = FastAPI(
    title="Muhe Opportunity Radar API",
    description="AI 投资机会分析 API - 多视角分析、历史记录、数据可视化、文档导入、LangGraph 工作流",
    version="2.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS 配置 - 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Vue3 开发环境
        "http://localhost:5173",  # Vite 默认端口
        "http://localhost:7860",  # Gradio 端口
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(analysis.router, prefix="/api/v1", tags=["分析"])
app.include_router(records.router, prefix="/api/v1", tags=["历史记录"])
app.include_router(investors.router, prefix="/api/v1", tags=["投资者"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["文档管理"])


@app.get("/")
async def root():
    """根路径 - API 信息"""
    return {
        "name": "Muhe Opportunity Radar API",
        "version": "2.1.0",
        "status": "running",
        "docs": "/api/docs",
        "endpoints": {
            "分析": "/api/v1/analyze",
            "多视角对比": "/api/v1/compare",
            "历史记录": "/api/v1/records",
            "统计信息": "/api/v1/statistics",
            "投资者列表": "/api/v1/investors",
            "文档上传": "/api/v1/documents/upload",
            "工作流分析": "/api/v1/documents/analyze-workflow"
        },
        "new_features": {
            "document_import": "支持 PDF/Word/Markdown 文档导入",
            "langgraph_workflow": "集成 LangGraph 数据分析工作流",
            "metrics_calculation": "自动计算财务指标（PE、PB、ROE、PEG）"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "path": str(request.url)
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式热重载
        log_level="info"
    )
