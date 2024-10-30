from typing import ClassVar

from pydantic_settings import SettingsConfigDict

from src.project.settings.authentication import AuthJWTSettings
from src.project.settings.database import PostgresSettings


class Settings(PostgresSettings, AuthJWTSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        use_enum_values=True,
        extra="ignore",
    )
