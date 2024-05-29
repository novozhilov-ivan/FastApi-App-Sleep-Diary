from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCredentials(BaseModel):
    """Данные пользователя для авторизации"""

    username: str = Field(
        title="Username",
        description="Имя пользователя для входа",
        min_length=4,
        max_length=10,
    )
    password: bytes = Field(
        title="Пароль",
        description="Пароль пользователя",
        min_length=3,
    )
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int = Field(
        title="User id",
        description="Идентификатор пользователя",
        ge=0,
    )
    model_config = ConfigDict(from_attributes=True)


class UserValidate(User, UserCredentials):
    model_config = ConfigDict(from_attributes=True)


class UserInfo(BaseModel):
    """Информация о пользователе"""

    id: int = Field(
        title="Id",
        description="Идентификатор пользователя",
        ge=0,
    )
    username: str = Field(
        title="Username",
        description="Имя пользователя для входа",
        min_length=4,
        max_length=10,
    )
    date_of_registration: datetime
    model_config = ConfigDict(from_attributes=True)
