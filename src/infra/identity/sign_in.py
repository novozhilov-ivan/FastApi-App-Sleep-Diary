from dataclasses import dataclass

from src.domain.identity.entities import AccessTokenClaims
from src.domain.identity.types import TokenType
from src.infra.identity.authentication import IUserAuthenticationService
from src.infra.identity.commands import SignInInputData
from src.project.settings.jwt import JWTSettings


@dataclass
class SignIn:
    settings: JWTSettings
    service: IUserAuthenticationService

    def __call__(self, command: SignInInputData) -> AccessTokenClaims:
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
