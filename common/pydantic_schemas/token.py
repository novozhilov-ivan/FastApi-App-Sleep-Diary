from pydantic import BaseModel


class TokenInfo(BaseModel):
    """Токен доступа и тип токена"""

    access_token: str
    token_type: str
