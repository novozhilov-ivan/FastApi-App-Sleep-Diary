from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing_extensions import Self

from src.infra.jwt.payloads import IPayload, JWTType


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
