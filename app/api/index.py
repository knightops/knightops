from fastapi import APIRouter, Request
from fishbase.fish_logger import logger as log
from core.response import api_return_handler, ResponseMessage
from app.utils.constants import *
from pydantic import BaseModel

method_get_router = APIRouter()

method_post_router = APIRouter()


@method_get_router.get('/')
def get_method(request: Request, type: str, app_id: str):
    """
    get 方法示例
    - **type**: 类型
    - **app_id**: 应用id
    """

    return_dict = ResponseMessage(code=SUCCESS, message=ERR_MSG[SUCCESS], data={'check_status': '1'})

    # 日志
    log.info('xxx result  : {}'.format(''))

    return api_return_handler(return_dict)



class Param(BaseModel):
    type: str
    app_id: str



@method_post_router.post('/')
def check_capthca(param: Param, request: Request):
    """
    post 方法示例
    - **type**: 类型
    - **app_id**: 应用id
    """

    type = param.type
    app_id = param.app_id

    return_dict = ResponseMessage(code=SUCCESS, message=ERR_MSG[SUCCESS], data={'check_status': '1'})

    # 日志
    log.info('xxx result  : {}'.format(''))

    return api_return_handler(return_dict)
