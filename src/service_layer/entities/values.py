from dataclasses import dataclass, field


@dataclass(frozen=True)
class BearerToken:
    token_type: str = field(default="Bearer", init=False)


@dataclass(frozen=True)
class AccessToken(BearerToken):
    access_token: str


@dataclass(frozen=True)
class RefreshToken(AccessToken):
    refresh_token: str
