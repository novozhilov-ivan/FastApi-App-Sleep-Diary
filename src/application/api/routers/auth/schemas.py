from fastapi import Form
from pydantic import UUID4, BaseModel


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
