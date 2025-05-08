from dataclasses import dataclass, field
from typing import Self

from src.domain.entities import UserEntity
from src.domain.services import IUsersRepository


@dataclass
class MemoryUsersRepository(IUsersRepository):
    _saved_users: set[UserEntity] = field(default_factory=set)

    def get_by_username(self: Self, username: str) -> UserEntity | None:
        return next(
            (user for user in self._saved_users if user.username == username),
            None,
        )

    def add_user(self: Self, user: UserEntity) -> None:
        self._saved_users.add(user)

    def delete_user(self: Self, username: str) -> None:
        if (user := self.get_by_username(username)) is not None:
            self._saved_users.remove(user)
