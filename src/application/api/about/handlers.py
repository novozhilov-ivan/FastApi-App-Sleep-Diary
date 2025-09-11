from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter
from starlette import status

from src.application.api.about.schemas import (
    AboutSleepDiarySchema,
)
from src.domain.sleep_diary.dtos import AboutInfo

router = APIRouter(
    prefix="/about",
    tags=["About"],
    route_class=DishkaSyncRoute,
)


@router.get(
    path="",
    description="Информация о дневнике сна.",
    status_code=status.HTTP_200_OK,
    response_model=AboutSleepDiarySchema,
)
def about_sleep_diary(
    about_info: FromDishka[AboutInfo],
) -> AboutSleepDiarySchema:
    return AboutSleepDiarySchema(description=about_info.description)
