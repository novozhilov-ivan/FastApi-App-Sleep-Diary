from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import uuid4

from src.identity.domain.exceptions import JWTExpiredError
from src.identity.domain.types import TokenType


@dataclass(kw_only=True)
class BaseAccessTokenClaims(ABC):
    subject: str
    issued_at: int = field(
        default_factory=lambda: int(datetime.now(UTC).timestamp())
    )
    expired_at: int
    jwt_token_ident: str = field(default_factory=lambda: str(uuid4()))

    def as_dict(self) -> dict[str, str | int]:
        return {
            "sub": self.subject,
            "iat": self.issued_at,
            "exp": self.expired_at,
            "jti": self.jwt_token_ident,
        }

    def __post_init__(self) -> None:
        self._validate()

    @staticmethod
    def timestamp_seconds_now() -> int:
        return int(datetime.now(UTC).timestamp())

    def _validate(self) -> None:
        if self.expired_at < self.timestamp_seconds_now():
            raise JWTExpiredError


@dataclass(kw_only=True)
class AccessTokenClaims(BaseAccessTokenClaims):
    token_type: TokenType
    username: str

    def as_dict(self) -> dict[str, str | int]:
        payload = super().as_dict()
        payload.update(
            typ=self.token_type,
            username=self.username,
        )
        return payload
