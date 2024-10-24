from pydantic import UUID4, BaseModel, Field


class UserValidate(BaseModel):
    oid: UUID4 = Field(description="Уникальный идентификатор пользователя")
    username: str = Field(
        title="User name",
        description="Имя пользователя для входа",
    )
    password: bytes = Field(
        title="Password",
        description="Пароль пользователя",
    )
