from fastapi import APIRouter

from src.sleep_diary.infrastructure.api.routers.about import about
from src.sleep_diary.infrastructure.api.routers.about.schemas import (
    AboutSleepDiarySchema,
)


router = APIRouter(tags=["About"])
router.include_router(about.router)
router.include_router(about.router, prefix="/about")

__all__ = (
    "router",
    "AboutSleepDiarySchema",
)
