from fastapi import APIRouter, Depends
from starlette import status

from src.application.api.authorization import (
    get_user_payload_from_access_token,
)
from src.application.api.routers.auth.schemas import (
    MeInfoResponse,
)
from src.service_layer.entities import UserPayload
from src.service_layer.exceptions.user_authorization import (
    UserTokenAuthorizationException,
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
