from fastapi import APIRouter, Depends
from starlette import status

from src.sleep_diary.application.entities import UserPayload
from src.sleep_diary.application.exceptions.user_authorization import (
    UserTokenAuthorizationException,
)
from src.sleep_diary.infrastructure.api.authorization import (
    get_user_payload_from_access_token,
)
from src.sleep_diary.infrastructure.api.routers.auth.schemas import (
    MeInfoResponse,
)


router = APIRouter(
    tags=["JWT"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UserTokenAuthorizationException},
    },
)


@router.get(
    path="/me/",
    description=(
        "Эндпоинт для получения информации авторизованному пользователю о себе из "
        "токена."
    ),
    status_code=status.HTTP_200_OK,
    response_model=MeInfoResponse,
)
def me_info(
    user_payload: UserPayload = Depends(get_user_payload_from_access_token),
) -> UserPayload:
    return user_payload
