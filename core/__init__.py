"""
web-api开发框架
2020.03.24
"""
import os
import importlib
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.utils.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.exceptions import HTTPException as StarletteHTTPException
from .exception import bad_request_handler, BadRequestException
from app.utils.redis_client import RedisClient
from fishbase.fish_logger import set_log_file
from app.middleware.proxy_headers import ProxyHeadersMiddleware
from core.config import settings

basedir = os.path.split(os.path.dirname(__file__))[0]
app_config = ()
sys_redis = ()


def init_application(app_name: str = 'app'):
    """
    初始化应用容器
    :return:
    """

    application = FastAPI(**settings.fastapi_kwargs)
    # 初始化redis
    init_redis()
    # 初始化log
    init_log()
    # 启动时候的事件
    application.add_event_handler('startup', startup)
    application.add_event_handler('shutdown', shutdown)
    # application.add_exception_handler()
    # 添加异常时候的处理
    application.add_exception_handler(BadRequestException, bad_request_handler)

    # 异常处理重写
    @application.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, exc):
        return await http_exception_handler(request, exc)

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return await request_validation_exception_handler(request, exc)

    # 加载路由
    app_mod = importlib.import_module('{}.router'.format(app_name))
    application.include_router(app_mod.router, prefix=settings.API_V1_STR)
    # 跨域解决
    origins = [
        "*",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 获取客户端ip解决
    application.add_middleware(
        ProxyHeadersMiddleware,
        trusted_hosts="*",
    )

    return application


def init_redis():
    """
    获取redis对象
    """
    pass
    # global sys_redis
    # sys_redis = RedisClient(app_config('redis_host', cast=str),
    #                         app_config('redis_port', cast=str),
    #                         app_config('redis_max_connections', cast=int),
    #                         app_config('redis_password', cast=str),
    #                         app_config('redis_db', cast=str)
    #                         )


def init_log():
    """
    初始化log
    """

    # 创建必须的log文件夹
    log_path = os.path.join(basedir, 'log')
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # 日志文件路径
    log_file = os.path.join(basedir, 'log',  'knightops.log')
    set_log_file(log_file)


async def startup():
    print('开始启动')
    pass


async def shutdown():
    pass
