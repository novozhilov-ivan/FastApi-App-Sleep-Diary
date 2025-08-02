from datetime import timedelta
from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    _env_prefix: ClassVar[str] = "JWT_"

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix=_env_prefix,
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )

    _BASE_DIR: ClassVar[Path] = Path(__file__).parent.parent.parent.parent
    print(_BASE_DIR)
    print(_BASE_DIR)
    print(_BASE_DIR)
    private_key: str = (_BASE_DIR / "jwt-private.pem").read_text()
    public_key: str = (_BASE_DIR / "jwt-public.pem").read_text()
    algorithm: str = "RS256"

    access_token_expire: int = Field(
        default_factory=lambda: int(
            timedelta(
                minutes=3,
            ).total_seconds(),
        ),
    )
    refresh_token_expire: int = Field(
        default_factory=lambda: int(
            timedelta(
                days=30,
            ).total_seconds(),
        ),
    )

    @property
    def algorithms(self) -> list[str]:
        return [self.algorithm]
