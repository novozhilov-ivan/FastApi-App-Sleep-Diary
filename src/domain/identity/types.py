from enum import StrEnum
from typing import Any

type JWTClaims = dict[str, Any]
type JWTToken = str


class TokenType(StrEnum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"
