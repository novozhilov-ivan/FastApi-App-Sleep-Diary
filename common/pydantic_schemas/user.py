from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class UserLogIn(BaseModel):
    """Данные пользователя для авторизации"""

    username: str = Field(
        title="Login field",
        min_length=4,
        max_length=10,
    )
    password: str = Field(
        title="Password field",
        min_length=6,
    )
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int = Field(
        title="User id",
        description="id пользователя для получения его записей.",
        ge=0,
        alias="user_id",
        validation_alias=AliasChoices("id", "user_id"),
    )
    model_config = ConfigDict(from_attributes=True)


class UserExtend(User):
    login: str
    date_of_registration: datetime
