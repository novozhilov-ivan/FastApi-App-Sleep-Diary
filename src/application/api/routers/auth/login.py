from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schema import (
    AccessAuthTokenInfoResponseSchema,
    AuthUserRequestSchema,
)
from src.project.containers import get_container


router = APIRouter(
    tags=["Authentication"],
    # responses={
    #     status.HTTP_401_UNAUTHORIZED: {"model": None},
    # },
)


@router.post(
    path="/login/",
    description=(
        "Эндпоинт для авторизации пользователя по имени пользователя и паролю."
    ),
    status_code=status.HTTP_200_OK,
    response_model=AccessAuthTokenInfoResponseSchema,
)
def authenticate_user(
    schema: AuthUserRequestSchema,
    container: Container = Depends(get_container),
) -> AccessAuthTokenInfoResponseSchema:
    auth_mediator: AuthenticationService
    auth_mediator = container.resolve(AuthenticationService)
    try:
        tokens_etc = auth_mediator.auth_user(
            username=schema.username,
            password=schema.password,
        )
    except AuthenticationException as exception:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return AccessAuthTokenInfoResponseSchema(**tokens_etc)
