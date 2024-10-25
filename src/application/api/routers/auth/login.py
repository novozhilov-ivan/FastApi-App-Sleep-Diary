from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schemas import (
    AccessJWTResponseSchema,
    LogInUserRequestSchema,
)
from src.project.containers import get_container
from src.service_layer.exceptions.base import AuthorizationException
from src.service_layer.services.base import BaseUserAuthorizationService


router = APIRouter(
    tags=["Authorization"],
)


@router.post(
    path="/login/",
    description=(
        "Эндпоинт для авторизации пользователя по имени пользователя и паролю."
    ),
    status_code=status.HTTP_200_OK,
    response_model=AccessJWTResponseSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": AuthorizationException},
    },
)
def login_user(
    schema: LogInUserRequestSchema,
    container: Container = Depends(get_container),
) -> AccessJWTResponseSchema:
    authorization_service: BaseUserAuthorizationService
    authorization_service = container.resolve(BaseUserAuthorizationService)
    try:
        user = authorization_service.login(
            username=schema.username,
            password=schema.password,
        )
    except AuthorizationException as exception:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )

    return AccessJWTResponseSchema(user).tokens
