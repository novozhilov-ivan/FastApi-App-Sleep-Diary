from typing import ClassVar

from dishka import Provider, Scope, from_context, provide
from fastapi import Request

from src.application.api.identity.auth.token_auth import TokenAuth
from src.domain.identity.jwt_processor import IJWTProcessor, JWTProcessor
from src.domain.sleep_diary.services.base import IUsersRepository
from src.infra.identity.access_token_processor import AccessTokenProcessor
from src.infra.identity.authentication import (
    IUserAuthenticationService,
    UserAuthenticationService,
)
from src.infra.identity.sign_in import SignIn
from src.project.settings import AuthorizationTokenSettings, Config


class InfraIdentityProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    config = from_context(provides=Config, scope=Scope.APP)

    @provide
    def get_token_auth_settings(self) -> AuthorizationTokenSettings:
        return AuthorizationTokenSettings()

    @provide
    def get_jwt_processor(self, config: Config) -> IJWTProcessor:
        return JWTProcessor(jwt_settings=config.jwt)

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
        config: Config,
        service: IUserAuthenticationService,
    ) -> SignIn:
        return SignIn(
            settings=config.jwt,
            service=service,
        )

    @provide(scope=Scope.REQUEST)
    def get_token_auth(
        self,
        request: Request,
        token_processor: AccessTokenProcessor,
        settings: AuthorizationTokenSettings,
    ) -> TokenAuth:
        return TokenAuth(
            request=request,
            token_processor=token_processor,
            settings=settings,
        )
