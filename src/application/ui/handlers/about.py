from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse

from src.infra.application.pages.about import AboutPage

router = APIRouter(
    route_class=DishkaSyncRoute,
)


@router.get(
    path="/about",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
def about_page(
    page: FromDishka[AboutPage],
) -> HTMLResponse:
    return page()
