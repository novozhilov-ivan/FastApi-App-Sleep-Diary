from typing import ClassVar

from dishka import Provider, Scope, provide

from src.domain.sleep_diary.dtos import AboutInfo
from src.domain.sleep_diary.use_cases.get_user_week_notes import GetUserWeekNotesUseCase
from src.domain.sleep_diary.use_cases.get_user_weeks_info import GetUserWeeksInfoUseCase


class DomainSleepDiaryProvider(Provider):
    scope: ClassVar[Scope] = Scope.REQUEST

    get_user_weeks_info_use_case = provide(GetUserWeeksInfoUseCase)
    get_user_week_notes_use_case = provide(GetUserWeekNotesUseCase)
    about_info = provide(AboutInfo)
