from fastapi.routing import APIRoute, APIRouter


class RemoveNoneAPIRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        kwargs.update({"response_model_exclude_none": True})
        super().__init__(*args, **kwargs)


def create_api_router():
    router = APIRouter()
    router.route_class = RemoveNoneAPIRoute

    return router
