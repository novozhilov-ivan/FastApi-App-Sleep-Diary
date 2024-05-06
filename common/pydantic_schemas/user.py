from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CreateUserCredentials(BaseModel):
    """Данные пользователя для авторизации"""

    username: str = Field(
        title="Логин",
        description="Логин пользователя",
        min_length=4,
        max_length=10,
        alias="login",
        validation_alias=AliasChoices("username", "login"),
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
        alias="user_id",
        validation_alias=AliasChoices("id", "user_id"),
    )
    model_config = ConfigDict(from_attributes=True)


class UserValidate(User, CreateUserCredentials):
    model_config = ConfigDict(from_attributes=True)


class UserInfo(BaseModel):
    """Информация о пользователе"""

    username: str = Field(
        title="Логин",
        description="Логин пользователя",
        min_length=4,
        max_length=10,
        alias="login",
        validation_alias=AliasChoices("username", "login"),
    )
    date_of_registration: datetime
    model_config = ConfigDict(from_attributes=True)
