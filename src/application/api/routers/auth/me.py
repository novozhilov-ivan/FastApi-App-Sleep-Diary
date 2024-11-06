from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schemas import (
    MeInfoResponse,
)
from src.application.api.schemas import jwt_dependency
from src.infra.authorization import (
    IUserJWTAuthorizationService,
    JWTAuthorizationException,
    UserPayload,
)
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
    token: str = Depends(jwt_dependency),
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
