from dataclasses import dataclass
from typing import Self

from src.domain.specifications import UserCredentialsSpecification
from src.service_layer.exceptions import AuthenticationException


@dataclass(eq=False)
class UserCredentialsFormatException(AuthenticationException):
    specification: UserCredentialsSpecification

    @property
    def message(self: Self) -> str:
        return (
            f"Неправильный формат данных пользователя: "
            f"Имя пользователя должно быть больше "
            f"{self.specification.MIN_LEN_USERNAME} символов и меньше "
            f"{self.specification.MAX_LEN_USERNAME} символов. "
            f"Пароль должен быть больше "
            f"{self.specification.MIN_LEN_PASSWORD} символов и меньше "
            f"{self.specification.MAX_LEN_PASSWORD} символов."
        )
