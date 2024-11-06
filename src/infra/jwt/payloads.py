from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing_extensions import Self
from uuid import uuid4


class JWTType(StrEnum):
    ACCESS: str = "access"
    REFRESH: str = "refresh"


@dataclass
class IPayload(ABC):
    @abstractmethod
    def convert_to_dict(self: Self) -> dict:
        raise NotImplementedError


@dataclass(kw_only=True)
class JWTPayload(IPayload):
    typ: JWTType
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
