from fastapi import APIRouter

from src.application.api.routers.notes import notes


router = APIRouter(prefix="/notes")
router.include_router(notes.router)

__all__ = ("router",)
