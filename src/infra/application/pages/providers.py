from typing import ClassVar

from dishka import Provider, Scope, provide

from src.infra.application.pages.about import AboutPage
from src.infra.application.pages.me import MePage
from src.infra.application.pages.sign_in import FetchSignInPage
from src.infra.application.pages.sign_up import FetchSignUpPage
from src.infra.application.pages.week import WeekPage
from src.infra.application.pages.weeks_info import WeeksInfoPage


class InfraApplicationPagesProvider(Provider):
    scope: ClassVar[Scope] = Scope.REQUEST

    weeks_info_page = provide(WeeksInfoPage)
    about_page = provide(AboutPage)
    week_page = provide(WeekPage)
    fetch_sign_up_page = provide(FetchSignUpPage)
    fetch_sign_in_page = provide(FetchSignInPage)
    me_page = provide(MePage)
