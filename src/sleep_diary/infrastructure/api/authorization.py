from dataclasses import dataclass
from typing import Self

from fastapi import Depends, HTTPException
from punq import Container
from starlette import status

from .dependecies import get_token_bearer  # noqa: ABS101 # need to fix
from src.sleep_diary.application.entities import TokenType, UserPayload
from src.sleep_diary.application.exceptions import UserTokenAuthorizationException
from src.sleep_diary.application.services import IUserJWTAuthorizationService
from src.sleep_diary.config.containers import get_container


@dataclass(unsafe_hash=True)
class GetUserPayloadFromToken:
    token_type: TokenType

    def __call__(
        self: Self,
        token: str = Depends(get_token_bearer),
        container: Container = Depends(get_container),
    ) -> UserPayload:
        user_jwt_service: IUserJWTAuthorizationService = container.resolve(
            IUserJWTAuthorizationService,
            jwt=token,  # TODO Прокинуть токен внутрь контейнера кваргсами
        )
        try:
            user_jwt_service.validate_token_type(self.token_type)
        except UserTokenAuthorizationException as exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": exception.message},
            )
        return user_jwt_service.current_payload


get_user_payload_from_access_token = GetUserPayloadFromToken(TokenType.ACCESS)
