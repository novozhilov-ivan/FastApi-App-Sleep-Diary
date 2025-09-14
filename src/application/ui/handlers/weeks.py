from datetime import date
from typing import Annotated

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import HTMLResponse

from src.infra.application.pages.week import WeekPage
from src.infra.application.pages.weeks_info import WeeksInfoPage
from src.project.containers import config

router = APIRouter(
    prefix="/weeks",
    route_class=DishkaSyncRoute,
    dependencies=[
        Depends(config.authorization_token.jwt_api_key_cookies),
    ],
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
def weeks_info_page(
    page: FromDishka[WeeksInfoPage],
) -> HTMLResponse:
    return page()


@router.get(
    path="/{start_date}",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
def week_page(
    start_date: Annotated[date, Path()],
    page: FromDishka[WeekPage],
) -> HTMLResponse:
    return page(start_date)
