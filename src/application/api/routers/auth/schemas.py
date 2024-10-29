from fastapi import Form
from fastapi.security import (
    OAuth2PasswordBearer,
)
from pydantic import UUID4, BaseModel, Field

from src.infra.authorization.base import JWTTypes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class AccessJWTResponseSchema(BaseModel):
    token_type: str = "Bearer"
    access_token: JWTTypes


class JWTResponseSchema(AccessJWTResponseSchema):
    refresh_token: JWTTypes


UserNameForm: str = Form(
    title="User name",
    description="Имя пользователя для входа",
)
PasswordForm: str = Form(
    title="User password",
    description="Пароль пользователя",
)


class LogInUserRequestSchema(BaseModel):
    username: str = Field(
        title="User name",
        description="Имя пользователя для входа",
    )
    password: str = Field(
        title="Password",
        description="Пароль пользователя",
    )


class AuthUserSelfInfoResponse(BaseModel):
    oid: UUID4
    username: str
