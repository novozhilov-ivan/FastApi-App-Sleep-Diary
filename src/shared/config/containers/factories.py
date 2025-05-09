from functools import lru_cache

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.identity.config.providers.auth import AuthProvider
from src.sleep_diary.config.providers.database import DatabaseProvider
from src.sleep_diary.config.providers.sleep_diary import SleepDiaryProvider


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        AuthProvider(),
        SleepDiaryProvider(),
        DatabaseProvider(),
        FastapiProvider(),
    )
