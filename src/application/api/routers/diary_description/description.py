from fastapi import APIRouter
from starlette import status

from src.application.api.routers.diary_description.schemas import (
    SleepDiaryDescriptionSchema,
)


router = APIRouter(tags=["Description"])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=SleepDiaryDescriptionSchema,
)
def get_sleep_diary_description():
    return SleepDiaryDescriptionSchema()
