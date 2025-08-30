from fastapi import APIRouter, status

from src.application.api.identity.api.handlers.users import router as user_router
from src.application.api.schemas import ErrorSchema
from src.application.api.sleep_diary.handlers.about.handlers import (
    router as about_router,
)
from src.application.api.sleep_diary.handlers.notes.handlers import (
    router as notes_router,
)


router = APIRouter(
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)

router.include_router(about_router)
router.include_router(notes_router)
router.include_router(user_router)
