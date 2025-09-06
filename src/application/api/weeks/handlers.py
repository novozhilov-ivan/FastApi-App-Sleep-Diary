from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Depends, status

from src.application.api.weeks.schemas import (
    AllWeeksInfoSchema,
)
from src.domain.sleep_diary.use_cases.get_user_weeks_info import GetUserWeeksInfoUseCase
from src.project.containers import config

router = APIRouter(
    prefix="/weeks",
    tags=["Weeks"],
    route_class=DishkaSyncRoute,
    dependencies=[
        Depends(config.authorization_token.jwt_api_key_cookies),
    ],
)


@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
)
def get_weeks(
    action: FromDishka[GetUserWeeksInfoUseCase],
) -> AllWeeksInfoSchema:
    weeks_list = action()

    return AllWeeksInfoSchema.from_week_list(weeks_list)
