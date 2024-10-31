from fastapi import APIRouter
from starlette import status

from src.application.api.routers.about.schemas import (
    AboutSleepDiarySchema,
)


router = APIRouter(tags=["About"])


@router.get(
    path="/",
    description="Информация о дневнике сна.",
    status_code=status.HTTP_200_OK,
    response_model=AboutSleepDiarySchema,
)
def about_sleep_diary() -> AboutSleepDiarySchema:
    return AboutSleepDiarySchema()
