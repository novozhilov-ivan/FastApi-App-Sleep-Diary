from fastapi import APIRouter, status

from src.application.api.about.handlers import (
    router as about_router,
)
from src.application.api.identity.handlers import router as user_router
from src.application.api.notes.handlers import (
    router as notes_router,
)
from src.application.api.schemas import ErrorSchema
from src.application.api.weeks.handlers import (
    router as weeks_router,
)

router = APIRouter(
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ErrorSchema},
    },
)

router.include_router(about_router)
router.include_router(notes_router)
router.include_router(weeks_router)
router.include_router(user_router)
