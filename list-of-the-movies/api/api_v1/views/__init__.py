__all__ = ("router",)

from api.api_v1.views.detail_views import router as detail_router
from api.api_v1.views.list_views import router

router.include_router(detail_router)
