from typing import ClassVar

from dishka import Provider, Scope, from_context, provide
from starlette.templating import Jinja2Templates

from src.project.settings import (
    AuthorizationTokenSettings,
    Config,
    JWTSettings,
    PostgreSQLSettings,
    UISettings,
)


class SettingsProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    config = from_context(Config)

    @provide
    def postgresql(self, config: Config) -> PostgreSQLSettings:
        return config.postgresql

    @provide
    def jwt(self, config: Config) -> JWTSettings:
        return config.jwt

    @provide
    def authorization_token(self, config: Config) -> AuthorizationTokenSettings:
        return config.authorization_token

    @provide
    def ui(self, config: Config) -> UISettings:
        return config.ui

    @provide
    def jinja_2_templates(self, settings: UISettings) -> Jinja2Templates:
        return settings.templates
