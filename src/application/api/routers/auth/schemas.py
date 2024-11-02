from fastapi import Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4, BaseModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class AccessJWTResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class JWTResponseSchema(AccessJWTResponseSchema):
    refresh_token: str


UserNameForm: str = Form(
    title="User name",
    description="Имя пользователя для входа",
)
PasswordForm: str = Form(
    title="User password",
    description="Пароль пользователя",
)


class MeInfoResponse(BaseModel):
    sub: UUID4
    username: str
