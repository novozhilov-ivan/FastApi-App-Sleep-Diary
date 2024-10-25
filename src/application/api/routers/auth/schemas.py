from pydantic import BaseModel

from src.infrastructure.authentication.jwt import JWTTokenTypes
from src.project.authorization import BEARER_TOKEN_TYPE


class AccessJWTResponseSchema(BaseModel):
    token_type: str = BEARER_TOKEN_TYPE
    access_token: JWTTokenTypes


class JWTResponseSchema(AccessJWTResponseSchema):
    refresh_token: JWTTokenTypes


class LogInUserRequestSchema(BaseModel):
    username: str
    password: str
