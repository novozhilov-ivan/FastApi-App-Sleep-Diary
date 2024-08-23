from typing import ClassVar

from pydantic_settings import SettingsConfigDict

from src.settings.authentication import AuthJWTSettings
from src.settings.database import PostgresSettings
from src.settings.flask import FlaskSettings
from src.settings.flask_restx import FlaskRestXSettings


class Settings(
    PostgresSettings,
    FlaskSettings,
    FlaskRestXSettings,
    AuthJWTSettings,
):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        use_enum_values=True,
    )
