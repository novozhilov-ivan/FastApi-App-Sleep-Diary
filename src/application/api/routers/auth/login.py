from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schemas import (
    JWTResponseSchema,
    PasswordForm,
    UserNameForm,
)
from src.infra.authorization import IUserTokenService
from src.project.containers import get_container
from src.service_layer.exceptions import (
    AuthenticationException,
    UserCredentialsFormatException,
)
from src.service_layer.services import IUserAuthenticationService


router = APIRouter(
    tags=["Authentication"],
    responses={
        status.HTTP_201_CREATED: {"model": JWTResponseSchema},
    },
)


@router.post(
    path="/login/",
    description=(
        "Эндпоинт для аутентификации пользователя по имени пользователя и паролю. "
        "И выпуска JWT токена для дальнейшей авторизации пользователя."
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=JWTResponseSchema,
)
def authenticate_user_and_issue_jwt(
    username: str = UserNameForm,
    password: str = PasswordForm,
    container: Container = Depends(get_container),
) -> dict:
    authentication_service: IUserAuthenticationService
    authentication_service = container.resolve(IUserAuthenticationService)

    token_service: IUserTokenService = container.resolve(IUserTokenService)

    try:
        authentication_service.login(username, password)
        return token_service.create_access(authentication_service.user)
    except UserCredentialsFormatException as exception:
        HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": exception.message},
        )
    except AuthenticationException as exception:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
