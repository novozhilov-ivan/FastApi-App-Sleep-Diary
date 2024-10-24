from pydantic import BaseModel

from src.application.authentication import BEARER_TOKEN_TYPE
from src.infrastructure.authentication.jwt import JWTTokenTypes


class AccessAuthTokenInfoResponseSchema(BaseModel):
    token_type: str = BEARER_TOKEN_TYPE
    access_token: JWTTokenTypes


class AuthTokensInfoResponseSchema(AccessAuthTokenInfoResponseSchema):
    refresh_token: JWTTokenTypes


class AuthUserRequestSchema(BaseModel):
    username: str
    password: bytes
