from typing import Annotated

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.ui.schemas import MakeSignUpSchema
from src.domain.identity.exceptions import IdentityError
from src.domain.sleep_diary.exceptions.base import ApplicationError
from src.infra.application.pages.me import MePage
from src.infra.application.pages.sign_in import FetchSignInPage
from src.infra.application.pages.sign_up import FetchSignUpPage
from src.infra.identity.services.token_auth import TokenAuth
from src.infra.identity.use_cases.sign_up import SignUp
from src.project.containers import config

router = APIRouter(
    prefix="/identity",
    route_class=DishkaSyncRoute,
)


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
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
    status_code=status.HTTP_200_OK,
)
def fetch_sign_up_page(
    page: FromDishka[FetchSignUpPage],
) -> HTMLResponse:
    return page()


@router.post(
    path="/sign-up",
    status_code=status.HTTP_201_CREATED,
    response_class=RedirectResponse,
)
def make_sign_up_page(
    request: Request,
    form: Annotated[MakeSignUpSchema, Form()],
    token_auth: FromDishka[TokenAuth],
    sign_up: FromDishka[SignUp],
) -> RedirectResponse:
    try:
        access_token_claims = sign_up(form.to_command())
    except (ApplicationError, IdentityError) as error:
        make_sign_up_page_url = request.url_for("make_sign_up_page")
        return RedirectResponse(
            url=f"{make_sign_up_page_url}/?error={error.message}",
            status_code=status.HTTP_302_FOUND,
        )

    weeks_info_page_url = request.url_for("weeks_info_page")
    response = RedirectResponse(
        url=f"{weeks_info_page_url}/?success=Регистрация успешна",
        status_code=status.HTTP_302_FOUND,
    )

    return token_auth.set_session(access_token_claims, response)


@router.get(
    path="/sign-in",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
def fetch_sign_in_page(
    page: FromDishka[FetchSignInPage],
) -> HTMLResponse:
    return page()
