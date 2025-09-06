from abc import ABC, abstractmethod


class IGetUserIdentityUseCase(ABC):
    @abstractmethod
    def __call__(self) -> str:
        raise NotImplementedError
