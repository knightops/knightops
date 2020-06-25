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
from starlette.config import Config
from starlette.exceptions import HTTPException as StarletteHTTPException
from .exception import bad_request_handler, BadRequestException
from app.utils.redis_client import RedisClient
from fishbase.fish_logger import set_log_file
from app.middleware.proxy_headers import ProxyHeadersMiddleware

basedir = os.path.split(os.path.dirname(__file__))[0]
app_config = ()
sys_redis = ()


def init_application(app_name: str = 'app'):
    """
    初始化应用容器
    :return:
    """

    application = FastAPI(title="knightops API", version="1.0")
    # 初始化配置文件
    init_config(app_name)
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
    application.include_router(app_mod.router, prefix=app_config('prefix', cast=str, default='/api'))
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


def init_config(app_name):
    """
    初始化配置文件
    """
    # 项目根目录
    global app_config
    config_dir = os.path.join(basedir, app_name, 'config')
    # 判断环境
    env_status = os.getenv('ENV_STATUS') or 'test'
    # 获取env文件内容
    app_config = Config('{}/env.{}'.format(config_dir, env_status))


def init_redis():
    """
    获取redis对象
    """
    global sys_redis
    sys_redis = RedisClient(app_config('redis_host', cast=str),
                            app_config('redis_port', cast=str),
                            app_config('redis_max_connections', cast=int),
                            app_config('redis_password', cast=str),
                            app_config('redis_db', cast=str)
                            )
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
