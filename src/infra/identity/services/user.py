from dataclasses import dataclass

from src.infra.identity.services.token_auth import TokenAuth


@dataclass
class GetUserIdentity:
    token_auth: TokenAuth

    def __call__(self) -> str:
        return self.token_auth.get_access_token().subject
