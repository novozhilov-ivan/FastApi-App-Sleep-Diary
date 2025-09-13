from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from src.infra.application.pages.about import AboutPage

router = APIRouter(
    route_class=DishkaSyncRoute,
)


@router.get(
    path="/",
    response_class=HTMLResponse,
)
@router.get(
    path="/about",
    response_class=HTMLResponse,
)
def about_page(
    page: FromDishka[AboutPage],
) -> HTMLResponse:
    return page()
