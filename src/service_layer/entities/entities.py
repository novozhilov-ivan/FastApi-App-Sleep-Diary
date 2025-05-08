from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Self
from uuid import uuid4

from src.service_layer.entities.base import IPayload
from src.service_layer.entities.enums import TokenType


@dataclass(kw_only=True)
class JWTPayload(IPayload):
    typ: TokenType
    iat: int = field(default_factory=lambda: int(datetime.now(UTC).timestamp()))
    exp: int
    jti: str = field(default_factory=lambda: str(uuid4()))

    external_payload: IPayload | None = None

    def convert_to_dict(self: Self) -> dict:
        jwt_payload = {
            "typ": self.typ,
            "iat": self.iat,
            "exp": self.exp,
            "jti": self.jti,
        }
        if self.external_payload:
            jwt_payload.update(self.external_payload.convert_to_dict())

        return jwt_payload


@dataclass
class UserPayload(IPayload):
    sub: str
    username: str

    def convert_to_dict(self: Self) -> dict:
        return {
            "sub": self.sub,
            "username": self.username,
        }


@dataclass(kw_only=True)
class UserJWTPayload(JWTPayload, UserPayload):
    pass
