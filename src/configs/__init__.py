from typing import ClassVar

from pydantic_settings import SettingsConfigDict

from src.configs.authentication import AuthJWTSettings
from src.configs.database import PostgresSettings
from src.configs.flask import FlaskSettings
from src.configs.flask_restx import FlaskRestXSettings


class Settings(
    PostgresSettings,
    FlaskSettings,
    FlaskRestXSettings,
    AuthJWTSettings,
):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
    )
