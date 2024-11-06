from datetime import timedelta
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings


class AuthJWTSettings(BaseSettings):
    _BASE_DIR: ClassVar[Path] = Path(__file__).parent.parent.parent.parent

    private_key: str = (_BASE_DIR / "jwt-private.pem").read_text()
    public_key: str = (_BASE_DIR / "jwt-public.pem").read_text()
    algorithm: str = "RS256"
    access_token_expire: int = timedelta(minutes=3).total_seconds()
    refresh_token_expire: int = timedelta(days=30).total_seconds()
