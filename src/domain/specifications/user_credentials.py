from dataclasses import dataclass
from operator import and_
from typing import ClassVar, Self

from src.domain.specifications.base import BaseSpecification


@dataclass
class UserCredentialsSpecification(BaseSpecification):
    MIN_LEN_USERNAME: ClassVar[int] = 3
    MAX_LEN_USERNAME: ClassVar[int] = 25
    MIN_LEN_PASSWORD: ClassVar[int] = 5
    MAX_LEN_PASSWORD: ClassVar[int] = 25

    username: str
    password: str

    def _validate_username(self: Self) -> bool:
        return self.MIN_LEN_USERNAME < len(self.username) < self.MAX_LEN_USERNAME

    def _validate_password(self: Self) -> bool:
        return self.MIN_LEN_PASSWORD < len(self.password) < self.MAX_LEN_PASSWORD

    def __bool__(self: Self) -> bool:
        return and_(self._validate_password(), self._validate_username())
