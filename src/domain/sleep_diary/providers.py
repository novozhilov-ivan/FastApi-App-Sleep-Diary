from typing import ClassVar

from dishka import Provider, Scope, provide

from src.domain.sleep_diary.use_cases.get_user_weeks_info import GetUserWeeksInfoUseCase


class DomainSleepDiaryProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    get_user_weeks_info_use_case = provide(
        GetUserWeeksInfoUseCase,
        scope=Scope.REQUEST,
    )
