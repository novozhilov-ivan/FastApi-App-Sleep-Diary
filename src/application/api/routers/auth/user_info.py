from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schemas import (
    MeInfoResponse,
)
from src.infra.authorization import IUserTokenService, JWTAuthorizationException
from src.infra.authorization.base import UserJWTPayload
from src.project.containers import get_container


router = APIRouter(
    tags=["JWT"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": JWTAuthorizationException},
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
    container: Container = Depends(get_container),
) -> UserJWTPayload:
    token_service: IUserTokenService = container.resolve(IUserTokenService)
    try:
        return token_service.payload
    except JWTAuthorizationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
