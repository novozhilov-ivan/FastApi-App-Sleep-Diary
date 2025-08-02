from enum import StrEnum
from typing import Any, TypeAlias


JWTClaims: TypeAlias = dict[str, Any]
JWTToken: TypeAlias = str


class TokenType(StrEnum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"
