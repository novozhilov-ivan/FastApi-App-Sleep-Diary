from typing import Annotated

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Form, HTTPException, Response, status
from fastapi.responses import JSONResponse

from src.application.api.identity.handlers.schemas import (
    SignInRequestSchema,
    SignUpRequestSchema,
)
from src.application.api.identity.services.token_auth import TokenAuth
from src.domain.sleep_diary.exceptions.base import ApplicationError
from src.infra.identity.commands import SignInInputData
from src.infra.identity.sign_in import SignIn
from src.infra.identity.sign_up import SignUp

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


@router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED,
)
def sign_up(
    form: Annotated[SignUpRequestSchema, Form()],
    action: FromDishka[SignUp],
    token_auth: FromDishka[TokenAuth],
) -> Response:
    try:
        access_token_claims = action(form.to_command())
    except ApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.message,
        ) from error

    response = JSONResponse(status_code=status.HTTP_201_CREATED, content={})

    return token_auth.set_session(access_token_claims, response)
