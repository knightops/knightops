from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from core.response import api_return_handler, ResponseMessage
from core.pagination import Pagination
from fastapi import Depends
from fastapi_utils.api_model import APIMessage
from fastapi_utils.api_model import APIModel

from fastapi_utils.session import FastAPISessionMaker

router = InferringRouter()


@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class AddonsCBV:
    # Step 3: Add dependencies as class attributes

    @router.get("/", status_code=201, )
    def list(self, pager: Pagination = Depends(Pagination)):
        data = pager.paginate(['a','b'])
        return data

    @router.post("/", status_code=201, response_model=ResponseMessage)
    def post(self, item):
        print(item)
        return ResponseMessage(message='hello', data={})

    @router.get("/item/{pk}")
    def get(self, pk):
        print(pk)
        return_dict = ResponseMessage(message='hello', data={})
        return api_return_handler(return_dict)

    @router.put("/item/{pk}")
    def update(self, pk):
        print(pk)
        return_dict = ResponseMessage(message='hello', data={})
        return api_return_handler(return_dict)

