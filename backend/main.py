from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

from config.settings import settings
from models.database import create_tables
from routers.offers import router as offers_router

# 创建FastAPI应用实例
app = FastAPI(
    title="邀请码发放系统",
    description="一个支持多项目的邀请码管理和发放系统",
    version="1.0.0",
    debug=settings.debug
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(offers_router, prefix=settings.api_v1_prefix)

# 静态文件服务
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# 启动时创建数据库表
@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    create_tables()
    print("✅ 数据库表创建完成")
    print(f"🚀 邀请码发放系统启动成功")
    print(f"📖 API文档地址: http://localhost:8000/docs")

# 根路径重定向到API文档
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "邀请码发放系统API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "api_prefix": settings.api_v1_prefix
    }

# 前端路由处理 - 支持单页应用
@app.get("/offer/{offer_name}")
async def serve_offer_page(offer_name: str):
    """服务前端offer页面"""
    frontend_index = frontend_path / "index.html"
    if frontend_index.exists():
        return FileResponse(str(frontend_index))
    else:
        raise HTTPException(
            status_code=404,
            detail="前端页面不存在，请确保frontend目录下有index.html文件"
        )

# 健康检查接口
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "invitation-code-system"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
