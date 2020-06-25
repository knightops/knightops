"""

"""
from typing import Any, Union
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST
)
from fastapi.exceptions import RequestValidationError, HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail: Any = None, headers: dict = None):
        super(BadRequestException, self).__init__(HTTP_400_BAD_REQUEST, detail, headers)


async def page_not_found_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """page not found"""
    return JSONResponse(dict(message='page not found'), status_code=exc.status_code)


async def bad_request_handler(_: Request, exc: BadRequestException) -> JSONResponse:
    """Bad Request"""
    return JSONResponse(dict(message=exc.detail), status_code=HTTP_400_BAD_REQUEST)



