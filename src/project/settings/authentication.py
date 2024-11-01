from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent.parent


class AuthJWTSettings(BaseSettings):
    PRIVATE_KEY: Path = BASE_DIR / "jwt-private.pem"
    PUBLIC_KEY: Path = BASE_DIR / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
