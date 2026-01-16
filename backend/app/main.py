"""
智能食物记录 - 后端服务主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Base, engine
from .api import meal, system
import uvicorn

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="智能食物记录 API", version="1.0.0")

# CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(meal.meal_router)
app.include_router(system.system_router)


@app.get("/")
async def root():
    return {"message": "智能食物记录 API 服务运行中"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
