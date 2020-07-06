from fastapi import APIRouter
from app.api import health_router, method_get_router, method_post_router, addons_router

router = APIRouter()

# 健康页
router.include_router(health_router, prefix='/health')

# get 接口
router.include_router(method_get_router, prefix='/method_get')

# post 接口
router.include_router(method_post_router, prefix='/method_post')

router.include_router(addons_router, prefix='/addons')


