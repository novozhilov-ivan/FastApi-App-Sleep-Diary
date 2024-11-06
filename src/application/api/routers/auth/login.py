from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schemas import (
    AccessJWTResponseSchema,
    PasswordForm,
    RefreshJWTResponseSchema,
    UserNameForm,
)
from src.infra.authorization import IUserJWTAuthorizationService, RefreshToken
from src.project.containers import get_container
from src.service_layer.exceptions import (
    AuthenticationException,
    UserCredentialsFormatException,
)
from src.service_layer.services import IUserAuthenticationService


router = APIRouter(
    tags=["Authentication", "JWT"],
    responses={
        status.HTTP_201_CREATED: {"model": AccessJWTResponseSchema},
    },
)


@router.post(
    path="/login/",
    description=(
        "Эндпоинт для аутентификации пользователя по имени пользователя и паролю. "
        "И выпуска JWT токена для дальнейшей авторизации пользователя."
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=RefreshJWTResponseSchema,
)
def login_user_and_issue_two_jwts(
    username: str = UserNameForm,
    password: str = PasswordForm,
    container: Container = Depends(get_container),
) -> RefreshToken:
    authentication_service: IUserAuthenticationService
    token_service: IUserJWTAuthorizationService

    authentication_service = container.resolve(IUserAuthenticationService)
    token_service = container.resolve(IUserJWTAuthorizationService)

    try:
        authentication_service.login(username, password)
        return token_service.create_refresh(authentication_service.user)
    except UserCredentialsFormatException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": exception.message},
        )
    except AuthenticationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
