from dataclasses import dataclass

from src.domain.identity.entities import AccessTokenClaims
from src.infra.identity.services.authentication import IUserAuthenticationService
from src.infra.identity.use_cases.commands import SignUpInputData
from src.infra.identity.use_cases.sign_in import SignIn


@dataclass
class SignUp:
    service: IUserAuthenticationService
    sign_in: SignIn

    def __call__(self, command: SignUpInputData) -> AccessTokenClaims:
        self.service.register(command.username, command.plain_password_first)
        return self.sign_in(command.to_sign_in_command())
