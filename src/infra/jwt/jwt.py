from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing_extensions import Self
from uuid import uuid4

from jwt import DecodeError, PyJWTError, decode, encode

from src.infra.jwt.base import IJWTService, IPayload, JWTType
from src.project.settings import AuthJWTSettings


@dataclass(kw_only=True)
class JWTPayload(IPayload):
    typ: JWTType
    exp: float

    external_payload: dict = field(default_factory=dict)

    iat: float = field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    jti: str = field(default_factory=lambda: str(uuid4()))

    def convert_to_dict(self: Self) -> dict:
        return {
            **self.external_payload,
            "typ": self.typ.value,
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
                key=self.settings.PRIVATE_KEY,
                algorithm=self.settings.ALGORITHM,
            )
        except PyJWTError:
            raise EncodeJWTException

    def _decode(self: Self, jwt: str) -> dict:
        try:
            return decode(
                jwt=jwt,
                key=self.settings.PUBLIC_KEY,
                algorithms=[self.settings.ALGORITHM],
            )
        except DecodeError:
            raise DecodeJWTException

    def create_jwt(
        self: Self,
        jwt_type: JWTType,
        payload: IPayload | None = None,
        expired_timedelta: timedelta | None = None,
    ) -> str:
        return self._encode(
            payload=JWTPayload(
                typ=jwt_type,
                external_payload=payload.convert_to_dict() if payload else {},
                exp=self.get_expired_at(jwt_type, expired_timedelta),
            ).convert_to_dict(),
        )

    def get_jwt_payload(
        self: Self,
        jwt: str,
        payload_schema: type[JWTPayload],
    ) -> JWTPayload:
        payload = self._decode(jwt)
        try:
            return payload_schema(**payload)
        except DataclassInit:
            raise ParseJWTPayloadException

    def get_expired_at(
        self: Self,
        token_type: JWTType,
        expired_timedelta: timedelta | None = None,
    ) -> float:
        if expired_timedelta:
            return datetime.now(UTC).timestamp() + expired_timedelta.seconds

        expired_seconds: float
        if token_type == JWTType.ACCESS:
            expired_seconds = timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            ).seconds
        else:
            expired_seconds = timedelta(
                days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS,
            ).seconds

        return datetime.now(UTC).timestamp() + expired_seconds
