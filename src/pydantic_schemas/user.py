from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(
        title="User id",
        description='id пользователя для получения его записей.',
        alias='user_id'
    )


class UserExtend(User):
    login: str
    date_of_registration: datetime
