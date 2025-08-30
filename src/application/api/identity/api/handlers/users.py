from typing import Annotated

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Form, Response, status
from fastapi.responses import JSONResponse

from src.application.api.identity.api.handlers.schemas import (
    SignInRequestSchema,
)
from src.application.api.identity.auth.token_auth import TokenAuth
from src.infra.identity.commands import SignInInputData
from src.infra.identity.sign_in import SignIn

router = APIRouter(
    prefix="/users",
    route_class=DishkaSyncRoute,
)


@router.post(
    "/sign-in",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": {}},
    },
)
def sign_in(
    form: Annotated[SignInRequestSchema, Form()],
    action: FromDishka[SignIn],
    token_auth: FromDishka[TokenAuth],
) -> Response:
    access_token_claims = action(
        SignInInputData(username=form.username, password=form.password),
    )

    response = JSONResponse(status_code=status.HTTP_200_OK, content={})

    return token_auth.set_session(access_token_claims, response)
