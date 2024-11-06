from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing_extensions import Self


@dataclass
class IPayload(ABC):
    @abstractmethod
    def convert_to_dict(self: Self) -> dict:
        raise NotImplementedError
