from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schemas import (
    JWTResponseSchema,
    PasswordForm,
    UserNameForm,
)
from src.infrastructure.authorization.base import BaseTokenService
from src.project.containers import get_container
from src.service_layer.exceptions.base import AuthenticationException
from src.service_layer.services.base import BaseUserAuthenticationService


router = APIRouter(
    tags=["Authorization"],
)


@router.post(
    path="/login/",
    description=(
        "Эндпоинт для авторизации пользователя по имени пользователя и паролю."
    ),
    status_code=status.HTTP_200_OK,
    response_model=JWTResponseSchema,
)
def auth_user_issue_jwt(
    username: str = UserNameForm,
    password: str = PasswordForm,
    container: Container = Depends(get_container),
) -> dict:
    authentication_service: BaseUserAuthenticationService
    authentication_service = container.resolve(BaseUserAuthenticationService)
    try:
        authentication_service.login(username, password)
    except AuthenticationException as exception:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )

    token_service: BaseTokenService = container.resolve(BaseTokenService)
    return token_service.create_access(authentication_service.user)
