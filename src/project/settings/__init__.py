from dataclasses import dataclass, field

from src.project.settings.jwt import JWTSettings
from src.project.settings.postgresql import PostgreSQLSettings
from src.project.settings.token_auth import AuthorizationTokenSettings
from src.project.settings.ui import UISettings


@dataclass
class Config:
    postgresql: PostgreSQLSettings = field(default_factory=PostgreSQLSettings)
    jwt: JWTSettings = field(default_factory=JWTSettings)
    authorization_token: AuthorizationTokenSettings = field(
        default_factory=AuthorizationTokenSettings,
    )
    ui: UISettings = field(default_factory=UISettings)
