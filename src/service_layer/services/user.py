from dataclasses import dataclass
from typing_extensions import Self

from src.domain.entities.user import UserEntity
from src.service_layer.services.base import BaseUserAuthorizationService


@dataclass
class UserAuthorizationService(BaseUserAuthorizationService):
    def login(self: Self, username: str, password: str) -> UserEntity:
        self._validate_credentials(username, password)
        return self.user
