from dataclasses import dataclass

from fastapi import Request, Response

from src.domain.identity.entities import AccessTokenClaims
from src.infra.identity.exceptions.base import NotAuthenticatedError
from src.infra.identity.services.access_token_processor import AccessTokenProcessor
from src.project.settings.token_auth import AuthorizationTokenSettings


@dataclass
class TokenAuth:
    request: Request
    token_processor: AccessTokenProcessor
    settings: AuthorizationTokenSettings

    def set_session(self, token: AccessTokenClaims, response: Response) -> Response:
        jwt_token = self.token_processor.encode(token)

        response.set_cookie(
            key=self.settings.cookies_key,
            value=jwt_token,
            httponly=True,
        )

        return response

    def get_session_token(self) -> str:
        token_key = self.settings.cookies_key
        return self.request.cookies.get(token_key)

    def get_access_token(self) -> AccessTokenClaims:
        cookies_token = self.get_session_token()

        if not cookies_token:
            raise NotAuthenticatedError()

        return self.token_processor.decode(cookies_token)

    def get_subject(self) -> str:
        token_claims = self.get_access_token()
        return token_claims.subject
