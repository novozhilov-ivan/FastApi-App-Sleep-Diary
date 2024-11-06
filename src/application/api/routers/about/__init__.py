from fastapi import APIRouter

from src.application.api.routers.about import about
from src.application.api.routers.about.schemas import AboutSleepDiarySchema


router = APIRouter(tags=["About"])
router.include_router(about.router)
router.include_router(about.router, prefix="/about")

__all__ = (
    "router",
    "AboutSleepDiarySchema",
)
