from datetime import datetime

from pydantic import BaseModel, Field, AliasChoices


class User(BaseModel):
    id: int = Field(
        title="User id",
        description='id пользователя для получения его записей.',
        ge=0,
        alias='user_id',
        validation_alias=AliasChoices(
            "id",
            "user_id"
        ),
    )


class UserExtend(User):
    login: str
    date_of_registration: datetime
