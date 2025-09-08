from fastapi import APIRouter

from src.application.ui.handlers.weeks import router as weeks_router

router = APIRouter(
    tags=["UI"],
)
router.include_router(weeks_router)
