from dataclasses import dataclass, field
from typing_extensions import Self

from src.infra.jwt import IPayload, JWTPayload


@dataclass
class BearerToken:
    token_type: str = field(default="Bearer", init=False)


@dataclass
class AccessToken(BearerToken):
    access_token: str


@dataclass
class RefreshToken(AccessToken):
    refresh_token: str


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
