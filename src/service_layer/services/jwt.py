from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self

from jwt import decode, DecodeError, encode, PyJWTError

from src.project.settings import AuthJWTSettings
from src.service_layer.entities import IPayload, JWTPayload, TokenType
from src.service_layer.exceptions import DecodeJWTException, EncodeJWTException
from src.service_layer.services.base import IJWTService


@dataclass
class JWTService(IJWTService):
    settings: AuthJWTSettings

    def encode(self: Self, payload: dict) -> str:
        try:
            return encode(
                payload=payload,
                key=self.settings.private_key,
                algorithm=self.settings.algorithm,
            )
        except PyJWTError:
            raise EncodeJWTException

    def decode(self: Self, jwt: str) -> dict:
        try:
            return decode(
                jwt=jwt,
                key=self.settings.public_key,
                algorithms=[self.settings.algorithm],
            )
        except DecodeError:
            raise DecodeJWTException

    def create_jwt(
        self: Self,
        jwt_type: TokenType,
        payload: IPayload | None = None,
        expire: int = 0,
    ) -> str:
        return self.encode(
            payload=JWTPayload(
                typ=jwt_type,
                exp=self.get_expired_at(jwt_type, expire),
                external_payload=payload,
            ).convert_to_dict(),
        )

    def get_jwt_payload(self: Self, jwt: str) -> dict:
        return self.decode(jwt)

    def get_expired_at(
        self: Self,
        token_type: TokenType,
        expire: int = 0,
    ) -> int:
        if expire:
            return int(datetime.now(UTC).timestamp() + expire)

        default_expire_by_token_type: int

        if token_type == TokenType.ACCESS:
            default_expire_by_token_type = self.settings.access_token_expire
        else:
            default_expire_by_token_type = self.settings.refresh_token_expire

        return int(datetime.now(UTC).timestamp() + default_expire_by_token_type)
