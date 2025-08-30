from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from src.domain.identity.exceptions import JWTExpiredError
from src.domain.identity.types import TokenType


@dataclass(kw_only=True)
class AccessTokenClaims:
    subject: str
    issued_at: int = field(
        default_factory=lambda: int(datetime.now(UTC).timestamp()),
    )
    expired_at: int
    jwt_token_ident: str = field(default_factory=lambda: str(uuid4()))
    token_type: TokenType
    username: str

    def __post_init__(self) -> None:
        self._validate()

    @staticmethod
    def timestamp_seconds_now() -> int:
        return int(datetime.now(UTC).timestamp())

    def _validate(self) -> None:
        if self.expired_at < self.timestamp_seconds_now():
            raise JWTExpiredError

    def as_dict(self) -> dict[str, str | int]:
        return {
            "sub": self.subject,
            "iat": self.issued_at,
            "exp": self.expired_at,
            "jti": self.jwt_token_ident,
            "typ": self.token_type,
            "username": self.username,
        }
