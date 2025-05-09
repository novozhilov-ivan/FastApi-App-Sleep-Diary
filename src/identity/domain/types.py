from enum import StrEnum
from typing import Any, TypeAlias


JWTClaims: TypeAlias = dict[str, Any]
JWTToken: TypeAlias = str


class TokenType(StrEnum):
    ACCESS: str = "access_token"
    REFRESH: str = "refresh_token"
