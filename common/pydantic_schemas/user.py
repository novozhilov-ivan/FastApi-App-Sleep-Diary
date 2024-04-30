from datetime import datetime

from pydantic import BaseModel, Field, AliasChoices, ConfigDict


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
