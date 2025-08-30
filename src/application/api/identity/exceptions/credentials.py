from dataclasses import dataclass

from src.application.api.identity.exceptions.base import AuthenticationError
from src.domain.sleep_diary.specifications.user_credentials import (
    UserCredentialsSpecification,
)


@dataclass(eq=False)
class UserCredentialsFormatError(AuthenticationError):
    specification: UserCredentialsSpecification

    @property
    def message(self) -> str:
        return (
            f"Неправильный формат данных пользователя: "
            f"Имя пользователя должно быть больше "
            f"{self.specification.MIN_LEN_USERNAME} символов и меньше "
            f"{self.specification.MAX_LEN_USERNAME} символов. "
            f"Пароль должен быть больше "
            f"{self.specification.MIN_LEN_PASSWORD} символов и меньше "
            f"{self.specification.MAX_LEN_PASSWORD} символов."
        )
