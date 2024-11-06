from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing_extensions import Self


@dataclass
class IPayload(ABC):
    @abstractmethod
    def convert_to_dict(self: Self) -> dict:
        raise NotImplementedError


class JWTType(StrEnum):
    ACCESS: str = "access"
    REFRESH: str = "refresh"


@dataclass
class IJWTService(ABC):

    @abstractmethod
    def encode(self: Self, payload: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self: Self, jwt: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_jwt(
        self: Self,
        jwt_type: JWTType,
        payload: IPayload | None = None,
        expire: int = 0,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_jwt_payload(self: Self, jwt: str) -> dict:
        raise NotImplementedError
