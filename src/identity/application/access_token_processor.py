from dataclasses import dataclass

from src.identity.domain.entities import AccessTokenClaims
from src.identity.domain.exceptions import (
    AccessTokenIsExpiredError,
    JWTDecodeError,
    JWTExpiredError,
    UnauthorizedError,
)
from src.identity.domain.jwt_processor import IJWTProcessor
from src.identity.domain.types import JWTToken, TokenType


@dataclass
class AccessTokenProcessor:
    jwt_processor: IJWTProcessor

    def encode(self, token: AccessTokenClaims) -> JWTToken:
        token_payload = token.as_dict()

        return self.jwt_processor.encode(token_payload)

    def decode(self, token: JWTToken) -> AccessTokenClaims:
        try:
            payload = self.jwt_processor.decode(token)

            if payload["typ"] == TokenType.ACCESS:
                raise ValueError

            data = AccessTokenClaims(
                subject=payload["sub"],
                issued_at=int(payload["iat"]),
                expired_at=int(payload["exp"]),
                jwt_token_ident=payload["jti"],
                token_type=payload["typ"],
                username=payload["username"],
            )
        except JWTExpiredError as error:
            raise AccessTokenIsExpiredError from error
        except (JWTDecodeError, ValueError, KeyError) as exc:
            raise UnauthorizedError from exc
        else:
            return data
