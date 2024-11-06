from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.dependecies import get_token_bearer
from src.application.api.routers.auth.schemas import (
    MeInfoResponse,
)
from src.project.containers import get_container
from src.service_layer.entities import UserPayload
from src.service_layer.exceptions.jwt_authorization import JWTAuthorizationException
from src.service_layer.services.base import IUserJWTAuthorizationService


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
    token: str = Depends(get_token_bearer),
    container: Container = Depends(get_container),
) -> UserPayload:
    token_service: IUserJWTAuthorizationService
    token_service = container.resolve(IUserJWTAuthorizationService)

    try:
        return token_service.get_payload(token)
    except JWTAuthorizationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
