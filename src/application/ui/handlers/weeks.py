from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter(
    prefix="/weeks",
    route_class=DishkaSyncRoute,
)


@router.get(
    path="",
    response_class=HTMLResponse,
)
def weeks_page(
    request: Request,
    templates: FromDishka[Jinja2Templates],
) -> HTMLResponse:
    return templates.TemplateResponse("sleep_diary.html", {"request": request})
