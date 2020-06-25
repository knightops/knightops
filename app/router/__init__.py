from fastapi import APIRouter
from app.api import health_router, method_get_router, method_post_router

router = APIRouter()

# 健康页
router.include_router(health_router, prefix='/v1/health')

# get 接口
router.include_router(method_get_router, prefix='/v1/method_get')

# post 接口
router.include_router(method_post_router, prefix='/v1/method_post')


