from dataclasses import dataclass

from src.domain.entities.base import BaseEntity


@dataclass(eq=False, kw_only=True)
class UserEntity(BaseEntity):
    username: str
    password: bytes
