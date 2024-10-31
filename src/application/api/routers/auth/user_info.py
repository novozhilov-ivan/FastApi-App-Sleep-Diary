from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schemas import (
    MeInfoResponse,
    oauth2_scheme,
)
from src.infra.authorization import IUserTokenService, JWTAuthorizationException
from src.project.containers import get_container


router = APIRouter(
    tags=["Authentication"],
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
    credentials: str = Depends(oauth2_scheme),
    container: Container = Depends(get_container),
) -> dict:
    token_service: IUserTokenService = container.resolve(IUserTokenService)
    try:
        return token_service.get_token_payload(credentials)
    except JWTAuthorizationException as exception:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
