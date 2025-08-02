from dataclasses import dataclass, field

from src.domain.sleep_diary.entities.user import UserEntity
from src.domain.sleep_diary.services.base import IUsersRepository


@dataclass
class MemoryUsersRepository(IUsersRepository):
    _saved_users: set[UserEntity] = field(default_factory=set)

    def get_by_username(self, username: str) -> UserEntity | None:
        return next(
            (user for user in self._saved_users if user.username == username),
            None,
        )

    def add_user(self, user: UserEntity) -> None:
        self._saved_users.add(user)

    def delete_user(self, username: str) -> None:
        if (user := self.get_by_username(username)) is not None:
            self._saved_users.remove(user)
