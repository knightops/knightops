"""
格式化返回结果
"""
from fastapi import Response, Depends
from typing import Any
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from pydantic import BaseModel
from app.utils.constants import *

class ResponseMessage(BaseModel):
    code: str = SUCCESS
    message: str = ''
    data: dict = None

    def __repr__(self):

        return self.dict()


def api_return_handler(resp_msg: ResponseMessage, status_code=200) -> JSONResponse:
    return JSONResponse(content=resp_msg.dict(),  status_code=status_code)
