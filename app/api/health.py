from fastapi import APIRouter
from core.response import api_return_handler, ResponseMessage

health_router = APIRouter()


@health_router.get('')
def health():

    return_dict = ResponseMessage(message='hello',data={})
    return api_return_handler(return_dict)


@health_router.head('')
def health():

    return_dict = ResponseMessage(message='hello',data={})
    return api_return_handler(return_dict)
