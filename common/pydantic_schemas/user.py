from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

user_id_field = Field(
    title="Id",
    description="Идентификатор пользователя",
    ge=0,
)
username_field = Field(
    title="Username",
    description="Имя пользователя для входа",
    min_length=4,
    max_length=25,
)
user_password_field = Field(
    title="Password",
    description="Пароль пользователя",
    min_length=3,
)


class UserCredentials(BaseModel):
    """Данные пользователя для авторизации"""

    username: str = username_field
    password: bytes = user_password_field
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int = user_id_field
    model_config = ConfigDict(from_attributes=True)


class UserValidate(User, UserCredentials):
    pass


class UserInfo(User):
    """Информация о пользователе"""

    username: str = username_field
    registration_date: datetime
    model_config = ConfigDict(from_attributes=True)
