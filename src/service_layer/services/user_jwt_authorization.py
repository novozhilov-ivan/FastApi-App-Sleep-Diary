from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from src.domain.entities import UserEntity
from src.service_layer.entities import (
    AccessToken,
    RefreshToken,
    TokenType,
    UserJWTPayload,
    UserPayload,
)
from src.service_layer.exceptions import UserTokenAuthorizationException
from src.service_layer.exceptions.user_authorization import TokenTypeException
from src.service_layer.services.base import IJWTService, IUserJWTAuthorizationService


@dataclass
class UserJWTAuthorizationService(IUserJWTAuthorizationService):
    jwt_service: IJWTService
    jwt: str | None = None

    def create_access(self: Self) -> AccessToken:
        self.validate_token_type(TokenType.REFRESH)

        return AccessToken(
            access_token=self.jwt_service.create_jwt(
                jwt_type=TokenType.ACCESS,
                payload=UserPayload(
                    str(self.current_user_oid),
                    self.current_username,
                ),
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

    @property
    def current_payload(self: Self) -> UserJWTPayload:
        if self.jwt is None:
            raise UserTokenAuthorizationException

        return UserJWTPayload(**self.jwt_service.get_jwt_payload(self.jwt))

    def deauthorize(self: Self) -> None: ...

    def validate_token_type(self: Self, token_type: TokenType) -> None:
        if self.current_token_type not in TokenType:
            raise UserTokenAuthorizationException

        if self.current_payload.typ != token_type:
            raise TokenTypeException(self.current_payload.typ, token_type)

    @property
    def current_user_oid(self: Self) -> UUID:
        return UUID(self.current_payload.sub)

    @property
    def current_username(self: Self) -> str:
        return self.current_payload.username

    @property
    def current_token_type(self: Self) -> TokenType:
        return self.current_payload.typ
