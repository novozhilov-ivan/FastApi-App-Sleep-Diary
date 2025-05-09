from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Form, Response, status
from fastapi.responses import JSONResponse

from src.identity.application.commands import SignInInputData
from src.identity.application.sign_in import SignIn
from src.identity.infrastructure.api.handlers.schemas import (
    SignInRequestSchema,
)
from src.identity.infrastructure.auth.token_auth import TokenAuth


user_router = APIRouter(prefix="/users", route_class=DishkaRoute)


@user_router.post(
    "/sign-in",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": {}},
    },
)
async def sign_in(
    form: Annotated[SignInRequestSchema, Form(...)],
    action: FromDishka[SignIn],
    token_auth: FromDishka[TokenAuth],
) -> Response:
    access_token_claims = await action(
        SignInInputData(username=form.username, password=form.password),
    )

    response = JSONResponse(status_code=status.HTTP_200_OK, content={})

    return token_auth.set_session(access_token_claims, response)
