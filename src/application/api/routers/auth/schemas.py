from fastapi import Form
from pydantic import BaseModel, UUID4


class AccessJWTResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class RefreshJWTResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


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
