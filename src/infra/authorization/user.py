from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from src.domain.entities import UserEntity
from src.infra.authorization.base import (
    AccessToken,
    IUserJWTAuthorizationService,
    JWTType,
    RefreshToken,
    UserJWTPayload,
    UserPayload,
)
from src.infra.authorization.exceptions import (
    JWTAuthorizationException,
    JWTTypeException,
)
from src.infra.jwt import IJWTService


@dataclass
class UserJWTAuthorizationService(IUserJWTAuthorizationService):
    jwt_service: IJWTService

    def create_access(self: Self, user: UserEntity) -> AccessToken:
        return AccessToken(
            access_token=self.jwt_service.create_jwt(
                jwt_type=JWTType.ACCESS,
                payload=UserPayload(str(user.oid), user.username).convert_to_dict(),
            ),
        )

    def create_refresh(self: Self, user: UserEntity) -> RefreshToken:
        return RefreshToken(
            refresh_token=self.jwt_service.create_jwt(
                jwt_type=JWTType.REFRESH,
                payload=UserPayload(str(user.oid), user.username).convert_to_dict(),
            ),
        )

    def get_payload(self: Self, token: str) -> UserJWTPayload:
        return UserJWTPayload(**self.jwt_service.get_jwt_payload(token))

    def deauthorize(self: Self) -> None: ...

    def validate_token_type(self: Self, jwt_type: JWTType) -> None:
        if not isinstance(self.payload.typ, JWTType):
            raise JWTAuthorizationException

        if self.payload.typ != jwt_type:
            raise JWTTypeException(self.payload.typ, jwt_type)

    def get_user_oid(self: Self) -> UUID:
        return UUID(self.payload.sub)
