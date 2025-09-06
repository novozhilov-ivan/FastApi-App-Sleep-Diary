from datetime import date
from typing import Annotated

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Depends, Path, status

from src.application.api.weeks.schemas import (
    AllWeeksInfoSchema,
    WeekNotesListSchema,
)
from src.domain.sleep_diary.dtos import WeekNotes
from src.domain.sleep_diary.use_cases.get_user_week_notes import GetUserWeekNotesUseCase
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
def get_weeks_info(
    action: FromDishka[GetUserWeeksInfoUseCase],
) -> AllWeeksInfoSchema:
    weeks_list = action()

    return AllWeeksInfoSchema.from_week_list(weeks_list)


@router.get(
    "/{start_date}",
    status_code=status.HTTP_200_OK,
)
def get_week_notes(
    start_date: Annotated[date, Path()],
    action: FromDishka[GetUserWeekNotesUseCase],
) -> WeekNotesListSchema:
    week_notes: WeekNotes = action(start_date=start_date)

    return WeekNotesListSchema.from_week_notes(week_notes)
