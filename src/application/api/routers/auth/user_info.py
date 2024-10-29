from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from src.application.api.routers.auth.schemas import (
    AuthUserSelfInfoResponse,
    oauth2_scheme,
)
from src.infra.authorization.base import BaseTokenService
from src.infra.authorization.exceptions import JWTAuthorizationException
from src.project.containers import get_container


router = APIRouter(
    tags=["Authorization"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": JWTAuthorizationException},
    },
)


@router.get(
    path="/me/",
    status_code=status.HTTP_200_OK,
    response_model=AuthUserSelfInfoResponse,
)
def auth_user_check_self_info(
    credentials: str = Depends(oauth2_scheme),
    container: Container = Depends(get_container),
) -> dict:
    token_service: BaseTokenService = container.resolve(BaseTokenService)
    try:
        return token_service.get_token_payload(credentials)
    except JWTAuthorizationException as exception:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
