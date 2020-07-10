from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.addons import AddonsManager
from core.config import settings
from core.pagination import Pagination
from core.response import api_return_handler, ResponseMessage

router = InferringRouter()


@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class AddonsCBV:
    # Step 3: Add dependencies as class attributes
    addons = AddonsManager(settings.ADDONS_FOLDER)

    @router.get("/", status_code=201, )
    def list(self, pager: Pagination = Depends(Pagination)):
        self.addons.load_addons()
        print(self.addons.all_addons)
        data = pager.paginate([i.dict() for i in self.addons.all_addons.values()])
        return data

    @router.post("/", status_code=201, response_model=ResponseMessage)
    def post(self, item):
        return ResponseMessage(message='hello', data={})

    @router.get("/item/{pk}")
    def get(self, pk):
        return_dict = ResponseMessage(message='hello', data={})
        return api_return_handler(return_dict)

    @router.put("/item/{pk}")
    def update(self, pk):
        return_dict = ResponseMessage(message='hello', data={})
        return api_return_handler(return_dict)

    @router.get("/install/{addons_name}")
    def install(self, addons_name):
        pass

