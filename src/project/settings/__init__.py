from dataclasses import dataclass, field

from src.project.settings.jwt import JWTSettings
from src.project.settings.postgresql import PostgreSQLSettings
from src.project.settings.token_auth import AuthorizationTokenSettings


@dataclass
class Config:
    postgresql: PostgreSQLSettings = field(default_factory=PostgreSQLSettings)
    jwt: JWTSettings = field(default_factory=JWTSettings)
    authorization_token: AuthorizationTokenSettings = field(
        default_factory=AuthorizationTokenSettings,
    )
