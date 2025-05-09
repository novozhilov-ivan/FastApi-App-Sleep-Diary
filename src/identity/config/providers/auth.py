from typing import ClassVar

from dishka import provide, Provider, Scope
from fastapi import Request

from src.identity.application.access_token_processor import AccessTokenProcessor
from src.identity.application.authentication import (
    IUserAuthenticationService,
    UserAuthenticationService,
)
from src.identity.application.sign_in import SignIn
from src.identity.config.settings.jwt import JWTSettings
from src.identity.config.settings.token_auth import TokenAuthSettings
from src.identity.domain.jwt_processor import IJWTProcessor, JWTProcessor
from src.identity.infrastructure.auth.token_auth import TokenAuth
from src.sleep_diary.domain.services import IUsersRepository


class AuthProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    @provide
    def get_jwt_settings(self) -> JWTSettings:
        return JWTSettings()

    @provide
    def get_token_auth_settings(self) -> TokenAuthSettings:
        return TokenAuthSettings()

    @provide
    def get_jwt_processor(self, settings: JWTSettings) -> IJWTProcessor:
        return JWTProcessor(jwt_settings=settings)

    @provide
    def get_access_token_processor(
        self,
        jwt_processor: IJWTProcessor,
    ) -> AccessTokenProcessor:
        return AccessTokenProcessor(jwt_processor=jwt_processor)

    @provide
    def get_user_authentication_service(
        self,
        repository: IUsersRepository,
    ) -> IUserAuthenticationService:
        return UserAuthenticationService(repository=repository)

    @provide
    def get_sign_in(
        self,
        settings: JWTSettings,
        service: IUserAuthenticationService,
    ) -> SignIn:
        return SignIn(
            settings=settings,
            service=service,
        )

    @provide(scope=Scope.REQUEST)
    def get_token_auth(
        self,
        request: Request,
        token_processor: AccessTokenProcessor,
        settings: TokenAuthSettings,
    ) -> TokenAuth:
        return TokenAuth(
            request=request,
            token_processor=token_processor,
            settings=settings,
        )
