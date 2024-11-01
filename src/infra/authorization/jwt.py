from dataclasses import dataclass
from datetime import timedelta
from typing_extensions import Self
from uuid import UUID

from fastapi import Depends, Header
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jwt import DecodeError, decode, encode

from src.domain.entities import UserEntity
from src.infra.authorization.base import (
    AccessToken,
    IPayload,
    IUserTokenService,
    RefreshToken,
    TokenType,
    UserJWTPayload,
)
from src.infra.authorization.exceptions import (
    JWTAuthorizationException,
    JWTTypeException,
)
from src.project.settings import AuthJWTSettings


oauth2_password_flow = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@dataclass
class UserJWTService(IUserTokenService):
    settings: AuthJWTSettings

    def _encode_payload(self: Self, payload: IPayload) -> str:
        return encode(
            payload=payload.convert_to_dict(),
            key=self.settings.PRIVATE_KEY.read_text(),
            algorithm=self.settings.ALGORITHM,
        )

    def _decode_jwt(self: Self, token: str | bytes) -> UserJWTPayload:
        try:
            return UserJWTPayload(
                **decode(
                    jwt=token,
                    key=self.settings.PUBLIC_KEY.read_text(),
                    algorithms=[self.settings.ALGORITHM],
                ),
            )
        except DecodeError:
            raise JWTAuthorizationException

    def create_access(self: Self, user: UserEntity) -> AccessToken:
        return AccessToken(
            self._encode_payload(
                UserJWTPayload(
                    sub=str(user.oid),
                    username=user.username,
                    token_type=TokenType.ACCESS,
                    expire_timedelta=timedelta(
                        minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                    ),
                ),
            ),
        )

    def create_refresh(self: Self, user: UserEntity) -> RefreshToken:
        return RefreshToken(
            self._encode_payload(
                UserJWTPayload(
                    sub=str(user.oid),
                    username=user.username,
                    token_type=TokenType.REFRESH,
                    expire_timedelta=timedelta(
                        days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS,
                    ),
                ),
            ),
        )

    @staticmethod
    def get_current_jwt(jwt: str = Depends(oauth2_password_flow)) -> str:
        return jwt

    @property
    def payload(self: Self) -> UserJWTPayload:
        return self._decode_jwt(self.get_current_jwt())

    def deauthorize(self: Self) -> None: ...

    @staticmethod
    def _received_token_type(
        token_type: TokenType = Header("some_auth"),
    ) -> TokenType: ...

    def validate_token_type(
        self: Self,
        token_type: TokenType = Depends(_received_token_type),
    ) -> None:
        if not isinstance(self.payload.token_type, TokenType):
            raise JWTAuthorizationException

        if self.payload.token_type != token_type:
            raise JWTTypeException(self.payload.token_type, token_type)

    def get_user_oid(self: Self) -> UUID:
        return UUID(self.payload.sub)
