from dataclasses import dataclass

from src.domain.sleep_diary.use_cases.base import IGetUserIdentityUseCase
from src.infra.identity.services.token_auth import TokenAuth


@dataclass
class GetUserIdentityUseCase(IGetUserIdentityUseCase):
    token_auth: TokenAuth

    def __call__(self) -> str:
        return self.token_auth.get_access_token().subject
