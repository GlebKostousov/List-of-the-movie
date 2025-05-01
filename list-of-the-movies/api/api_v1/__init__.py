from fastapi import APIRouter
from .views.list_views import router as get_film_by_id_router

router = APIRouter(prefix="/v1")
router.include_router(get_film_by_id_router)
