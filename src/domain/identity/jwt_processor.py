from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

import jwt

from src.domain.identity.exceptions import JWTDecodeError, JWTExpiredError
from src.domain.identity.types import JWTClaims, JWTToken
from src.project.settings.jwt import JWTSettings


class IJWTProcessor(Protocol):
    @abstractmethod
    def encode(self, payload: JWTClaims) -> JWTToken:
        raise NotImplementedError

    @abstractmethod
    def decode(self, token: JWTToken) -> JWTClaims:
        raise NotImplementedError


@dataclass
class JWTProcessor(IJWTProcessor):
    jwt_settings: JWTSettings

    def encode(self, payload: JWTClaims) -> JWTToken:
        return jwt.encode(
            payload,
            self.jwt_settings.private_key,
            self.jwt_settings.algorithm,
        )

    def decode(self, token: JWTToken) -> JWTClaims:
        try:
            return jwt.decode(
                token,
                self.jwt_settings.public_key,
                algorithms=self.jwt_settings.algorithms,
            )
        except jwt.ExpiredSignatureError as error:
            raise JWTExpiredError from error
        except jwt.DecodeError as error:
            raise JWTDecodeError from error
