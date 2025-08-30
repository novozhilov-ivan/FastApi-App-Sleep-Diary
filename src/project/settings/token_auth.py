from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthorizationTokenSettings(BaseSettings):
    _env_prefix: ClassVar[str] = "AUTHORIZATION_TOKEN_"

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix=_env_prefix,
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )

    cookies_key: str = "authorization_token"
