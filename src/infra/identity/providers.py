from typing import ClassVar

from dishka import Provider, Scope, WithParents, provide, provide_all

from src.domain.identity.jwt_processor import JWTProcessor
from src.infra.identity.services.access_token_processor import AccessTokenProcessor
from src.infra.identity.services.authentication import (
    UserAuthenticationService,
)
from src.infra.identity.services.token_auth import TokenAuth
from src.infra.identity.use_cases.sign_in import SignIn
from src.infra.identity.use_cases.sign_up import SignUp


class InfraIdentityProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    interactors = provide_all(
        SignIn,
        SignUp,
        AccessTokenProcessor,
    )
    jwt_processor = provide(JWTProcessor, provides=WithParents[JWTProcessor])
    user_auth_service = provide(
        UserAuthenticationService,
        provides=WithParents[UserAuthenticationService],
    )
    token_auth = provide(TokenAuth, scope=Scope.REQUEST)
