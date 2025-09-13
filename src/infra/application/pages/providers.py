from typing import ClassVar

from dishka import Provider, Scope, provide

from src.infra.application.pages.about import AboutPage
from src.infra.application.pages.week import WeekPage
from src.infra.application.pages.weeks_info import WeeksInfoPage


class InfraApplicationPagesProvider(Provider):
    scope: ClassVar[Scope] = Scope.REQUEST

    weeks_info_page = provide(WeeksInfoPage)
    about_page = provide(AboutPage)
    week_page = provide(WeekPage)
