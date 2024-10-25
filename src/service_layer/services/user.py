from dataclasses import dataclass
from typing_extensions import Self

from src.service_layer.services.base import BaseUserAuthenticationService


@dataclass
class UserAuthenticationService(BaseUserAuthenticationService):
    def login(self: Self, username: str, password: str) -> None:
        self._validate_credentials(username, password)
