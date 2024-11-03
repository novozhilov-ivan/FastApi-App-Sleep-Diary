from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from fastapi import Depends, Header

from src.domain.entities import UserEntity
from src.infra.authorization.base import (
    AccessToken,
    IUserAuthorizationService,
    JWTType,
    RefreshToken,
    UserJWTPayload,
)
from src.infra.authorization.exceptions import (
    JWTAuthorizationException,
    JWTTypeException,
)
from src.infra.jwt import IJWTService


@dataclass
class UserAuthorizationService(IUserAuthorizationService):
    jwt_service: IJWTService

    def create_access(self: Self, user: UserEntity) -> AccessToken:
        payload = UserJWTPayload(
            sub=str(user.oid),
            username=user.username,
        )
        return AccessToken(
            access_token=self.jwt_service.create_jwt(JWTType.ACCESS, payload),
        )

    def create_refresh(self: Self, user: UserEntity) -> RefreshToken:
        payload = UserJWTPayload(
            sub=str(user.oid),
            username=user.username,
        )
        return RefreshToken(
            refresh_token=self.jwt_service.create_jwt(JWTType.REFRESH, payload),
        )

    def get_payload(self: Self, token: str) -> UserJWTPayload:
        return self.jwt_service.get_jwt_payload(token, UserJWTPayload)

    def deauthorize(self: Self) -> None: ...

    @staticmethod
    def _received_token_type(
        token_type: JWTType = Header("some_auth"),
    ) -> JWTType: ...

    def validate_token_type(
        self: Self,
        token_type: JWTType = Depends(_received_token_type),
    ) -> None:
        if not isinstance(self.payload.typ, JWTType):
            raise JWTAuthorizationException

        if self.payload.typ != token_type:
            raise JWTTypeException(self.payload.typ, token_type)

    def get_user_oid(self: Self) -> UUID:
        return UUID(self.payload.sub)
