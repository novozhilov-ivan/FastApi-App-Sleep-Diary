from fastapi import APIRouter

from src.sleep_diary.infrastructure.api.routers.notes import notes


router = APIRouter(prefix="/notes")
router.include_router(notes.router)

__all__ = ("router",)
