from dataclasses import dataclass
from operator import eq

from src.domain.sleep_diary.entities.base import BaseEntity


@dataclass(eq=False, kw_only=True)
class UserEntity(BaseEntity):
    username: str
    password: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserEntity):
            return NotImplemented
        return eq(self.username, other.username)

    def __hash__(self) -> int:
        return hash(self.username)
