from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from src.application.services.exceptions import JWTTypeException
from src.domain.entities import UserEntity
from src.service_layer.entities import (
    AccessToken,
    RefreshToken,
    TokenType,
    UserJWTPayload,
    UserPayload,
)
from src.service_layer.exceptions.jwt_authorization import JWTAuthorizationException
from src.service_layer.services.base import IJWTService, IUserJWTAuthorizationService


@dataclass
class UserJWTAuthorizationService(IUserJWTAuthorizationService):
    jwt_service: IJWTService

    def create_access(self: Self, user: UserEntity) -> AccessToken:
        return AccessToken(
            access_token=self.jwt_service.create_jwt(
                jwt_type=TokenType.ACCESS,
                payload=UserPayload(str(user.oid), user.username),
            ),
        )

    def create_refresh(self: Self, user: UserEntity) -> RefreshToken:
        payload = UserPayload(str(user.oid), user.username)
        return RefreshToken(
            access_token=self.jwt_service.create_jwt(
                jwt_type=TokenType.ACCESS,
                payload=payload,
            ),
            refresh_token=self.jwt_service.create_jwt(
                jwt_type=TokenType.REFRESH,
                payload=payload,
            ),
        )

    def get_payload(self: Self, token: str) -> UserJWTPayload:
        # validate_token_type()
        return UserJWTPayload(**self.jwt_service.get_jwt_payload(token))

    def deauthorize(self: Self) -> None: ...

    def validate_token_type(self: Self, jwt_type: TokenType) -> None:
        if not isinstance(self.payload.typ, TokenType):
            raise JWTAuthorizationException

        if self.payload.typ != jwt_type:
            raise JWTTypeException(self.payload.typ, jwt_type)

    def get_user_oid(self: Self) -> UUID:
        return UUID(self.payload.sub)
