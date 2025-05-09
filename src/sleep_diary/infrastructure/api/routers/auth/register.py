from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.sleep_diary.application.exceptions import (
    UserCredentialsFormatException,
    UserRegisterException,
)
from src.sleep_diary.application.services import IUserAuthenticationService
from src.sleep_diary.config.containers import get_container
from src.sleep_diary.infrastructure.api.routers.auth.schemas import (
    PasswordForm,
    UserNameForm,
)


router = APIRouter(
    tags=["Authentication"],
)


@router.post(
    path="/register/",
    description=(
        "Эндпоинт для регистрации пользователя по имени пользователя и паролю."
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def register_user(
    username: str = UserNameForm,
    password: str = PasswordForm,
    container: Container = Depends(get_container),
) -> None:
    authentication_service: IUserAuthenticationService
    authentication_service = container.resolve(IUserAuthenticationService)

    try:
        authentication_service.register(username, password)
    except UserCredentialsFormatException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": exception.message},
        )
    except UserRegisterException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
