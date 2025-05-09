from dataclasses import dataclass

from src.identity.application.authentication import IUserAuthenticationService
from src.identity.application.commands import SignInInputData
from src.identity.config.settings.jwt import JWTSettings
from src.identity.domain.entities import AccessTokenClaims
from src.identity.domain.types import TokenType


@dataclass
class SignIn:
    settings: JWTSettings
    service: IUserAuthenticationService

    async def __call__(self, command: SignInInputData) -> AccessTokenClaims:
        user = self.service.login(command.username, command.password)
        expired_at = (
            AccessTokenClaims.timestamp_seconds_now()
            + self.settings.access_token_expire
        )
        return AccessTokenClaims(
            subject=str(user.oid),
            expired_at=expired_at,
            token_type=TokenType.ACCESS,
            username=user.username,
        )
