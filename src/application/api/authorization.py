from dataclasses import dataclass
from typing_extensions import Self

from fastapi import Depends, HTTPException
from punq import Container
from starlette import status

from .dependecies import get_token_bearer
from src.project.containers import get_container
from src.service_layer.entities import TokenType, UserPayload
from src.service_layer.exceptions import UserTokenAuthorizationException
from src.service_layer.services import IUserJWTAuthorizationService


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
