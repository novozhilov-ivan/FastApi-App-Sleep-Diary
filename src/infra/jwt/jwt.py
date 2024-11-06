from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing_extensions import Self
from uuid import uuid4

from jwt import DecodeError, PyJWTError, decode, encode

from src.infra.jwt.base import IJWTService, IPayload, JWTType
from src.infra.jwt.exceptions import DecodeJWTException, EncodeJWTException
from src.project.settings import AuthJWTSettings


@dataclass(kw_only=True)
class JWTPayload(IPayload):
    typ: JWTType
    iat: float = field(default_factory=lambda: datetime.now(UTC).timestamp())
    exp: float
    jti: str = field(default_factory=lambda: str(uuid4()))

    def convert_to_dict(self: Self) -> dict:
        return {
            "typ": self.typ,
            "iat": self.iat,
            "exp": self.exp,
            "jti": self.jti,
        }


@dataclass
class JWTService(IJWTService):
    settings: AuthJWTSettings

    def _encode(self: Self, payload: dict) -> str:
        try:
            return encode(
                payload=payload,
                key=self.settings.private_key,
                algorithm=self.settings.algorithm,
            )
        except PyJWTError:
            raise EncodeJWTException

    def _decode(self: Self, jwt: str) -> dict:
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
        jwt_type: JWTType,
        payload: dict | None = None,
        expired_timedelta: timedelta | None = None,
    ) -> str:
        if payload is None:
            payload = {}

        return self._encode(
            {
                **JWTPayload(
                    typ=jwt_type,
                    exp=self.get_expired_at(jwt_type, expired_timedelta),
                ).convert_to_dict(),
                **payload,
            },
        )

    def get_jwt_payload(self: Self, jwt: str) -> dict:
        return self._decode(jwt)

    def get_expired_at(
        self: Self,
        token_type: JWTType,
        expired_timedelta: timedelta | None = None,
    ) -> float:
        if expired_timedelta:
            return datetime.now(UTC).timestamp() + expired_timedelta.total_seconds()

        expired_seconds: float

        if token_type == JWTType.ACCESS:
            expired_seconds = timedelta(
                minutes=self.settings.access_token_expire,
            ).total_seconds()
        else:
            expired_seconds = timedelta(
                days=self.settings.refresh_token_expire,
            ).total_seconds()

        return datetime.now(UTC).timestamp() + expired_seconds
