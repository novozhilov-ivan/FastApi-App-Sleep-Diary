from fastapi import APIRouter

from src.application.ui.handlers.about import router as about_router
from src.application.ui.handlers.identity import router as identity_router
from src.application.ui.handlers.weeks import router as weeks_router

router = APIRouter(
    prefix="/ui",
    tags=["UI"],
)
router.include_router(about_router)
router.include_router(weeks_router)
router.include_router(identity_router)
