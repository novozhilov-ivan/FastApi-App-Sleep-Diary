from datetime import datetime
from typing import (
    Annotated,
    ClassVar,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


user_id_field = Annotated[
    int,
    Field(
        title="Id",
        description="Идентификатор пользователя",
        ge=0,
    ),
]
username_field = Annotated[
    str,
    Field(
        title="Username",
        description="Имя пользователя для входа",
        min_length=4,
        max_length=25,
    ),
]
user_password_field = Annotated[
    bytes,
    Field(
        title="Password",
        description="Пароль пользователя",
        min_length=3,
    ),
]


class UserCredentials(BaseModel):
    """Данные пользователя для авторизации"""

    username: username_field
    password: user_password_field
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: user_id_field
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class UserValidate(
    User,
    UserCredentials,
):
    ...  # fmt: skip


class UserInfo(User):
    """Информация о пользователе"""

    username: username_field
    created_at: datetime
    updated_at: datetime
