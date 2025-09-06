from typing import ClassVar

from fastapi.security import APIKeyCookie
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
    bearer_token_url: str = "/users/sign-in"

    @property
    def jwt_api_key_cookies(self) -> APIKeyCookie:
        return APIKeyCookie(
            name=self.cookies_key,
            scheme_name="JWT authorization user",
            description="JWT stored in cookie after sign-in",
            auto_error=False,
        )
