from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from src.infra.application.pages.me import MePage
from src.infra.application.pages.sign_in import FetchSignInPage
from src.infra.application.pages.sign_up import FetchSignUpPage
from src.project.containers import config

router = APIRouter(
    prefix="/identity",
    route_class=DishkaSyncRoute,
)


@router.get(
    path="/me",
    response_class=HTMLResponse,
    dependencies=[
        Depends(config.authorization_token.jwt_api_key_cookies),
    ],
)
def me_page(
    page: FromDishka[MePage],
) -> HTMLResponse:
    return page()


@router.get(
    path="/sign-up",
    response_class=HTMLResponse,
)
def fetch_sign_up_page(
    page: FromDishka[FetchSignUpPage],
) -> HTMLResponse:
    return page()


@router.get(
    path="/sign-in",
    response_class=HTMLResponse,
)
def fetch_sign_in_page(
    page: FromDishka[FetchSignInPage],
) -> HTMLResponse:
    return page()
