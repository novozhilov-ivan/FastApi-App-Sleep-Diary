from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    _BASE_DIR: ClassVar[Path] = Path(__file__).parent.parent.parent.parent.parent
    print(_BASE_DIR)
    private_key: str = (_BASE_DIR / "jwt-private.pem").read_text()
    public_key: str = (_BASE_DIR / "jwt-public.pem").read_text()
    algorithm: str = "RS256"

    access_token_expire: int = 60 * 3
    refresh_token_expire: int = 60 * 60 * 24 * 30

    @property
    def algorithms(self) -> list[str]:
        return [self.algorithm]
