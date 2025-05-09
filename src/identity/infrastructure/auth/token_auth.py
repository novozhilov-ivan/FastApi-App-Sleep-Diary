from dataclasses import dataclass

from fastapi import Request, Response

from src.identity.application.access_token_processor import AccessTokenProcessor
from src.identity.config.settings.token_auth import TokenAuthSettings
from src.identity.domain.entities import AccessTokenClaims
from src.identity.domain.exceptions import UnauthorizedError


@dataclass
class TokenAuth:
    request: Request
    token_processor: AccessTokenProcessor
    settings: TokenAuthSettings

    def set_session(self, token: AccessTokenClaims, response: Response) -> Response:
        jwt_token = self.token_processor.encode(token)

        response.set_cookie(
            self.settings.token_cookies_key,
            jwt_token,
            httponly=True,
        )

        return response

    def get_access_token(self) -> AccessTokenClaims:
        token_key = self.settings.token_cookies_key
        cookies_token = self.request.cookies.get(token_key)

        if not cookies_token:
            raise UnauthorizedError()

        return self.token_processor.decode(cookies_token)
