from legacy_src.extension import bearer

from pydantic import (
    BaseModel,
    Field,
)


class AccessTokenInfo(BaseModel):
    """Access токен и тип токена"""

    access_token: str
    token_type: str = Field(default=bearer)


class TokenInfo(AccessTokenInfo):
    """Access токен, refresh токен и тип токена"""

    refresh_token: str
