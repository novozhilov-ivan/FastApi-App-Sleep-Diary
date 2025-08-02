from functools import lru_cache

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.gateways.postresql.providers import DatabaseProvider
from src.infra.identity.providers import InfraIdentityProvider
from src.infra.sleep_diary.providers import InfraSleepDiaryProvider
from src.project.settings import Config


config = Config()


@lru_cache(1)
def get_async_container() -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        InfraIdentityProvider(),
        InfraSleepDiaryProvider(),
        DatabaseProvider(),
        context={Config: config},
    )
